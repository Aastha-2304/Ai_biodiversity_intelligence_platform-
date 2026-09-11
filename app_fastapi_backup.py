"""
main.py
FastAPI entrypoint — wires the full pipeline together (Stages 0-9).

Flow per request:
  0. Parse input (text or JSON)               -> input_parser.py
  1. Merge into case file, detect contradictions -> case_file.py
  2. Completeness check -> ask clarifying question if needed -> completeness_check.py
  3. Diagnostic hypothesis (deterministic)     -> rule_engine.py
  4. Evidence retrieval (biome-filtered RAG)   -> retrieval.py
  5. Multi-metric causal reasoning             -> reasoning_graph.py
  6. Intervention selection (curated library)  -> intervention_library.py
  7. LLM write-up (constrained)                -> llm_writer.py
  8. Verification (anti-hallucination gate)    -> verifier.py
  9. Structured output returned to frontend
"""

from __future__ import annotations
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.models.case_file import CaseFile, create_new_case_file
from backend.models.schemas import SystemResponse, Assessment, ConfidenceLevel
from backend.pipeline import input_parser, completeness_check, rule_engine, retrieval, reasoning_graph
from backend.pipeline import intervention_library, llm_writer, verifier

app = FastAPI(title="Darukaa.Earth Biodiversity Intelligence Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite/CRA dev servers
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store for the hackathon MVP. Swap for SQLite/Redis
# if you need persistence across server restarts.
_SESSIONS: dict[str, CaseFile] = {}


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str | None = None       # free text input
    structured_input: dict | None = None  # JSON input (mutually exclusive with message)


class ChatResponse(BaseModel):
    session_id: str
    system_response: SystemResponse
    evidence_trace: dict  # for demo transparency — shown in EvidenceTrace.jsx


def _get_or_create_case(session_id: str | None) -> tuple[str, CaseFile]:
    if session_id and session_id in _SESSIONS:
        return session_id, _SESSIONS[session_id]
    new_id = session_id or str(uuid.uuid4())
    case = create_new_case_file(new_id)
    _SESSIONS[new_id] = case
    return new_id, case


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if not request.message and not request.structured_input:
        raise HTTPException(400, "Provide either 'message' or 'structured_input'.")

    session_id, case = _get_or_create_case(request.session_id)

    # ---- Stage 0: parse input ----
    payload = request.structured_input if request.structured_input else request.message
    try:
        updates = input_parser.parse_input(payload)
    except Exception as e:
        raise HTTPException(400, f"Failed to parse input: {e}")

    # ---- Stage 1: merge into case file, detect contradictions ----
    summary_text = request.message or "structured input provided"
    contradictions = case.merge_update(updates, user_message_summary=summary_text)

    if contradictions:
        contradiction = contradictions[0]  # handle one at a time, simplest for MVP
        clarifying = (
            f"You previously described {contradiction.field_path.replace('.', ' ')} as "
            f"'{contradiction.previous_value}', but this message suggests "
            f"'{contradiction.new_value}'. Should I treat this as a change, or keep the earlier value?"
        )
        response = SystemResponse(
            assessment=Assessment(main_risks=[], missing_information=[], confidence=ConfidenceLevel.LOW),
            recommendations=[],
            monitoring_plan=[],
            clarifying_question=clarifying,
        )
        return ChatResponse(session_id=session_id, system_response=response, evidence_trace={})

    # ---- Stage 2: completeness check ----
    irrigation_probe = completeness_check.check_irrigation_probe(case)
    probe_notes = [irrigation_probe] if irrigation_probe else []
    completeness = completeness_check.check_completeness(case, domain_probe_notes=probe_notes)

    if not completeness.is_sufficient:
        response = SystemResponse(
            assessment=Assessment(
                main_risks=[],
                missing_information=completeness.missing_fields,
                confidence=ConfidenceLevel.LOW,
            ),
            recommendations=[],
            monitoring_plan=[],
            clarifying_question=completeness.clarifying_question,
        )
        case.update_running_assessment(
            f"Awaiting more information: {', '.join(completeness.missing_fields)}"
        )
        return ChatResponse(session_id=session_id, system_response=response, evidence_trace={})

    # ---- Stage 3: diagnostic hypothesis (deterministic) ----
    hypothesis = rule_engine.diagnose(case)

    # ---- Stage 4: evidence retrieval (biome-filtered RAG) ----
    query_text = " ".join(hypothesis.reasoning_notes) or "general biodiversity assessment"
    try:
        evidence_chunks = retrieval.retrieve_evidence(
            query_text=query_text,
            climate_zone=case.profile.location.climate_zone,
            hypothesis=hypothesis,
        )
    except FileNotFoundError as e:
        raise HTTPException(500, f"Knowledge base not built: {e}")

    conflicts = retrieval.find_conflicting_evidence(evidence_chunks)

    # ---- Stage 6: intervention selection (curated library, hard constraints enforced) ----
    interventions = intervention_library.select_interventions(
        hyp=hypothesis,
        climate_zone=case.profile.location.climate_zone,
    )

    # ---- Stage 5: multi-metric causal reasoning ----
    causal_paths = {}
    for iv in interventions:
        for metric in iv.impacted_metrics:
            path = reasoning_graph.get_longest_path(metric)
            if path:
                causal_paths[metric] = path

    if not interventions:
        response = SystemResponse(
            assessment=Assessment(
                main_risks=[f.value for f in hypothesis.risk_flags],
                missing_information=[],
                confidence=ConfidenceLevel.LOW,
            ),
            recommendations=[],
            monitoring_plan=[],
            clarifying_question=(
                "Based on the information provided, I don't have a suitable intervention "
                "in my curated library that fits these specific constraints. Could you "
                "share more about water availability or land size?"
            ),
        )
        return ChatResponse(session_id=session_id, system_response=response, evidence_trace={
            "hypothesis": hypothesis.reasoning_notes,
        })

    # ---- Stage 7: LLM write-up (constrained) ----
    draft_response = llm_writer.generate_response(
        case=case,
        hypothesis=hypothesis,
        evidence_chunks=evidence_chunks,
        causal_paths=causal_paths,
        interventions=interventions,
    )

    if draft_response is None:
        # Graceful degradation per the caching/resilience design: show
        # retrieved evidence directly rather than hanging or crashing.
        response = SystemResponse(
            assessment=Assessment(
                main_risks=[f.value for f in hypothesis.risk_flags],
                missing_information=[],
                confidence=ConfidenceLevel.LOW,
            ),
            recommendations=[],
            monitoring_plan=[],
            clarifying_question=(
                "Explanation generation is temporarily unavailable. Here is the retrieved "
                f"evidence directly: {[c.text[:200] for c in evidence_chunks[:3]]}"
            ),
        )
        return ChatResponse(session_id=session_id, system_response=response, evidence_trace={})

    # ---- Stage 8: verification (anti-hallucination gate) ----
    verification = verifier.verify(
        draft_response=draft_response,
        case=case,
        hypothesis=hypothesis,
        retrieved_chunks=evidence_chunks,
    )

    # ---- Stage 1 (continued): update running assessment for next turn ----
    case.update_running_assessment(
        f"Identified risks: {', '.join(f.value for f in hypothesis.risk_flags) or 'none'}. "
        f"Recommended: {', '.join(r.action for r in verification.cleaned_response.recommendations) or 'pending'}."
    )

    # ---- Stage 9: structured output + evidence trace for the demo ----
    evidence_trace = {
        "detected_issues": hypothesis.reasoning_notes,
        "retrieved_evidence": [
            {"chunk_id": c.chunk_id, "source": c.source, "text_preview": c.text[:150]}
            for c in evidence_chunks
        ],
        "conflicting_evidence": [
            {"a": a.chunk_id, "b": b.chunk_id, "metric": a.metric_affected}
            for a, b in conflicts
        ],
        "rejected_recommendations": verification.rejected_recommendations,
        "verifier_warnings": verification.warnings,
    }

    return ChatResponse(
        session_id=session_id,
        system_response=verification.cleaned_response,
        evidence_trace=evidence_trace,
    )


@app.get("/health")
def health():
    return {"status": "ok"}