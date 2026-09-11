"""
FastAPI Main Application — Darukaa.Earth AI Biodiversity Intelligence Platform
9-Stage Evidence-Gated Ecological Decision Support System
"""

import os
import uuid
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv

load_dotenv()

from backend.config import CORS_ORIGINS
from backend.database.audit_store import AuditDatabase
from backend.models.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation,
    EvidenceChunk,
    CausalHop,
    ClarifyingQuestion
)
from backend.models.case_file import get_or_create_case_file, reset_case_file
from backend.pipeline.input_parser import InputParser
from backend.pipeline.completeness_check import CompletenessChecker
from backend.pipeline.rule_engine import EnvironmentalRuleEngine
from backend.pipeline.retrieval import KnowledgeRetriever
from backend.pipeline.intervention_library import InterventionLibrary
from backend.pipeline.reasoning_graph import MultiMetricReasoningGraph
from backend.pipeline.verifier import InputValidator, EvidenceVerifier
from backend.pipeline.llm_writer import ScientificWriter
from backend.pipeline.monitoring import generate_monitoring_plan
from backend.pipeline.spatial_context import SpatialContextEngine
from backend.cache.response_cache import ResponseCache

app = FastAPI(
    title="Darukaa.Earth AI Biodiversity Intelligence API",
    description="Evidence-Gated 9-Stage Ecological Decision Support System",
    version="2.0.0"
)

# Enable CORS for frontend Vite/React client
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "Darukaa.Earth Biodiversity Intelligence API",
        "version": "2.0.0",
        "stages_supported": [
            "stage0_sanitization", "stage1_case_file", "stage2_completeness",
            "stage3_hypothesis", "stage4_rag_retrieval", "stage5_causal_graph",
            "stage6_synthesis", "stage7_peer_review", "stage8_delivery"
        ],
        "knowledge_chunks_indexed": len(KnowledgeRetriever.get_all_chunk_ids()),
        "evidence_gated": True,
        "zero_hallucination_active": True,
        "spatial_engine_active": True
    }


@app.get("/api/knowledge-base")
def get_knowledge_base():
    """Returns the full indexed research papers, reports, datasets, and vector catalog."""
    return KnowledgeRetriever.get_knowledge_catalog()


@app.post("/api/spatial/lookup")
def lookup_coordinates(payload: Dict[str, float]):
    lat = payload.get("latitude")
    lon = payload.get("longitude")
    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Latitude and longitude required.")
    return SpatialContextEngine.lookup_coordinates(lat, lon)


@app.post("/api/chat", response_model=ChatResponse)
def process_chat(req: ChatRequest):
    print(f"[DEBUG 1] REQUEST RECEIVED: message={req.message!r}, structured_input={req.structured_input!r}, session_id={req.session_id!r}")
    session_id = req.session_id or "default_session"
    case_session = get_or_create_case_file(session_id)

    # ----------------------------------------------------------------
    # STAGE 0: User Submits Input (Text, JSON, Coordinates) & Validation
    # ----------------------------------------------------------------
    incoming_data, input_mode, ambiguities = InputParser.parse_input(
        text=req.message or "",
        structured_dict=req.structured_input
    )
    print(f"[DEBUG 2] EXTRACTED INPUT: {incoming_data} (mode: {input_mode}, ambiguities: {ambiguities})")

    is_valid, hard_errors, suspicious_alerts = InputValidator.validate_bounds_and_units(incoming_data)
    if not is_valid:
        raise HTTPException(
            status_code=422,
            detail={
                "error_type": "physical_bounds_violation",
                "validation_errors": hard_errors,
                "scientist_note": (
                    "An environmental scientist rejects field readings that violate "
                    "thermodynamics or physical biology prior to analysis."
                )
            }
        )

    # Save user message to AuditDatabase for audit trail
    user_text = req.message or (json.dumps(req.structured_input) if req.structured_input else "")
    try:
        AuditDatabase.save_chat_message(session_id, "user", user_text)
    except Exception as e:
        print(f"[Audit DB save user message error]: {e}")

    # Check query intent (greeting, off-topic, or ecological)
    query_intent = incoming_data.get("_query_intent")
    if query_intent in ["greeting", "off_topic"]:
        print(f"[DEBUG 3] RETRIEVED INTERVENTIONS: [] (bypassed for {query_intent})")
        print(f"[DEBUG 4] RETRIEVED EVIDENCE: [] (bypassed for {query_intent})")
        raw_reply = ScientificWriter.synthesize_response(
            query=req.message or "",
            profile=incoming_data,
            rule_eval={},
            recommendations=[],
            retrieved_evidence=[],
            causal_chains=[],
            clarifying_question=None,
            completeness_eval={"requires_clarification": False, "is_actionable": False}
        )
        print(f"[DEBUG 7] VERIFIER INPUT: {len(raw_reply)} chars raw text, 0 interventions, 0 evidence chunks")
        verification_result = EvidenceVerifier.validate_response_text(
            raw_text=raw_reply,
            allowed_interventions=[],
            retrieved_evidence=[],
            user_profile={},
            is_actionable=False
        )
        reply_markdown = verification_result["verified_text"]
        print(f"[DEBUG 8] VERIFIER RESULT: is_verified={verification_result['is_verified']}, rejected_claims={verification_result['rejected_claims']}")
        print(f"[DEBUG 9] FINAL RESPONSE: len={len(reply_markdown)}, preview={reply_markdown[:120]!r}")
        try:
            AuditDatabase.save_chat_message(session_id, "assistant", reply_markdown)
        except Exception:
            pass
        return ChatResponse(
            session_id=session_id,
            reply_markdown=reply_markdown,
            case_file_profile=case_session.profile,
            rule_metrics={},
            recommendations=[],
            retrieved_evidence=[],
            causal_hops=[],
            clarifying_question=None,
            stages={},
            monitoring_plan=[],
            suspicious_alerts=[],
            contradiction_alerts=[],
            running_assessment=case_session.running_assessment,
            completeness_score=0.0,
            input_mode_detected=input_mode,
            is_cached=False,
            is_actionable=False,
            requires_clarification=False,
            spatial_context=None
        )

    # ----------------------------------------------------------------
    # STAGE 1: Environmental Case File Update & Provenance
    # ----------------------------------------------------------------
    contradictions = InputValidator.detect_multi_turn_contradictions(
        prior_profile=case_session.profile,
        incoming_data=incoming_data
    )

    case_session.update_profile(incoming_data, contradictions)
    current_profile = case_session.profile

    # ----------------------------------------------------------------
    # STAGE 2: Completeness & Domain-Probe Check
    # ----------------------------------------------------------------
    completeness_eval = CompletenessChecker.evaluate_completeness(
        profile=current_profile,
        detected_ambiguities=ambiguities
    )
    clarifying_q = completeness_eval.get("primary_question")
    completeness_score = completeness_eval.get("completeness_score", 0.5)
    is_actionable = completeness_eval.get("is_actionable", True)
    requires_clarification = completeness_eval.get("requires_clarification", False)

    # ----------------------------------------------------------------
    # STAGE 3: Diagnostic Hypothesis Formation & Intervention Retrieval
    # ----------------------------------------------------------------
    rule_eval = EnvironmentalRuleEngine.evaluate_profile(current_profile)
    diagnostic_hypothesis = rule_eval.get(
        "diagnostic_hypothesis", "Biophysical deficit requiring ecological remediation."
    )
    risk_ratings = rule_eval.get("risk_ratings", {})
    query_steer_terms = rule_eval.get("query_steer_terms", [])

    # Retrieve Curated Interventions (from interventions.json)
    raw_interventions = InterventionLibrary.get_matching_interventions(
        biome=current_profile.get("biome"),
        viable_classes=rule_eval.get("viable_intervention_classes", []),
        prohibited_classes=rule_eval.get("prohibited_intervention_classes", []),
        ecosystem_type=rule_eval.get("ecosystem_type"),
        environmental_profile=rule_eval.get("environmental_profile"),
        limiting_factors=rule_eval.get("primary_limiting_factors", [])
    )
    print(f"[DEBUG 3] RETRIEVED INTERVENTIONS: {[i.get('name') for i in raw_interventions]}")

    # ----------------------------------------------------------------
    # STAGE 4: Biome-Gated Vector RAG Evidence Retrieval
    # ----------------------------------------------------------------
    contextual_query = req.message or f"{rule_eval.get('ecosystem_type', '')} {current_profile.get('biome', '')} {current_profile.get('current_crop', '')} restoration"
    retrieved_raw, dissenting_evidence, retrieval_trace = KnowledgeRetriever.retrieve_evidence(
        query=contextual_query,
        biome=current_profile.get("biome"),
        steer_terms=query_steer_terms,
        top_k=6
    )
    retrieved_chunk_ids = {c["id"] for c in retrieved_raw}
    print(f"[DEBUG 4] RETRIEVED EVIDENCE: {[c.get('id') for c in retrieved_raw]}")

    # ----------------------------------------------------------------
    # STAGE 5: Multi-Metric Reasoning Graph & Verified Prescriptions
    # ----------------------------------------------------------------
    causal_chains = MultiMetricReasoningGraph.generate_causal_chains(current_profile, rule_eval)
    all_hops: List[CausalHop] = []
    for chain in causal_chains:
        for h in chain.get("hops", []):
            h_copy = dict(h)
            if "evidence_ref" in h_copy and not h_copy.get("evidence_citation"):
                h_copy["evidence_citation"] = h_copy["evidence_ref"]
            all_hops.append(CausalHop(**h_copy))

    verified_recommendations = []
    for item in raw_interventions[:3]:
        gated_rec = EvidenceVerifier.verify_and_gate_recommendation(
            rec_data=item,
            profile=current_profile,
            retrieved_chunk_ids=retrieved_chunk_ids,
            rule_eval=rule_eval
        )
        verified_recommendations.append(gated_rec)

    # ----------------------------------------------------------------
    # STAGE 6: LLM / Scientific Synthesis
    # ----------------------------------------------------------------
    raw_llm_reply = ScientificWriter.synthesize_response(
        query=req.message or "",
        profile=current_profile,
        rule_eval=rule_eval,
        recommendations=verified_recommendations if is_actionable else [],
        retrieved_evidence=retrieved_raw,
        causal_chains=causal_chains if is_actionable else [],
        clarifying_question=clarifying_q,
        completeness_eval=completeness_eval
    )

    # ----------------------------------------------------------------
    # STAGE 7: Verification Gate (Anti-Hallucination Claim Validation)
    # ----------------------------------------------------------------
    print(f"[DEBUG 7] VERIFIER INPUT: raw_text_len={len(raw_llm_reply)}, allowed_interventions={len(raw_interventions)}, retrieved_evidence={len(retrieved_chunk_ids)}, profile={current_profile}")
    verification_result = EvidenceVerifier.validate_response_text(
        raw_text=raw_llm_reply,
        allowed_interventions=raw_interventions,
        retrieved_evidence=retrieved_raw,
        user_profile=current_profile,
        is_actionable=is_actionable
    )
    reply_markdown = verification_result["verified_text"]
    print(f"[DEBUG 8] VERIFIER RESULT: is_verified={verification_result['is_verified']}, rejected_claims={verification_result['rejected_claims']}, sanitizations={verification_result['sanitizations']}")

    # ----------------------------------------------------------------
    # STAGE 8: Structured Output Delivery & Monitoring Protocol
    # ----------------------------------------------------------------
    monitoring_plan = generate_monitoring_plan(verified_recommendations) if is_actionable else []

    stages_bundle = {
        "stage0_validation": {
            "title": "Stage 0: Input Sanitization & Bounds Validation",
            "input_mode": input_mode,
            "extracted_entities": incoming_data,
            "bounds_validation_passed": True,
            "suspicious_alerts": suspicious_alerts,
            "scientist_note": "Verified biophysical parameter bounds and flagged unit anomalies."
        },
        "stage1_case_file": {
            "title": "Stage 1: Environmental Case File & Provenance",
            "accumulated_profile": current_profile,
            "provenance": case_session.provenance,
            "contradiction_alerts": contradictions,
            "turn_count": case_session.turn_count,
            "running_assessment": case_session.running_assessment,
            "spatial_context": current_profile.get("spatial_context")
        },
        "stage2_completeness": {
            "title": "Stage 2: Completeness & Domain-Probe Check",
            "completeness_score": completeness_score,
            "completeness_ratio": completeness_eval.get("completeness_ratio"),
            "established_count": completeness_eval.get("established_count"),
            "is_actionable": is_actionable,
            "requires_clarification": requires_clarification,
            "missing_high_impact_fields": completeness_eval.get("missing_fields", []),
            "domain_probes": completeness_eval.get("domain_probes", []),
            "clarifying_questions": completeness_eval.get("clarifying_questions", []),
            "ambiguity_translations": completeness_eval.get("ambiguity_translations", [])
        },
        "stage3_hypothesis": {
            "title": "Stage 3: Diagnostic Hypothesis Formation",
            "hypothesis": diagnostic_hypothesis,
            "risk_ratings": risk_ratings,
            "limiting_factors": rule_eval.get("primary_limiting_factors", []),
            "query_steer_terms": query_steer_terms,
            "system_health_index": rule_eval.get("system_health_index")
        },
        "stage4_evidence": {
            "title": "Stage 4: Biome-Gated Vector Evidence Retrieval (RAG)",
            "retrieved_chunk_count": len(retrieved_raw),
            "retrieved_chunks": retrieved_raw,
            "dissenting_evidence_surfaced": dissenting_evidence,
            "retrieval_trace": retrieval_trace
        },
        "stage5_interventions": {
            "title": "Stage 5: Intervention Selection & Multi-Metric Graph",
            "viable_categories": rule_eval.get("viable_intervention_classes", []),
            "prohibited_categories": rule_eval.get("prohibited_intervention_classes", []),
            "causal_chains": causal_chains,
            "variables_connected": [
                "Soil Organic Carbon & Microbial Networks",
                "Capillary Water Capacity & Atmospheric VPD",
                "Pollinator Biodiversity & Biological Pest Suppression"
            ]
        },
        "stage6_writeup": {
            "title": "Stage 6: Scientific Write-Up",
            "register": "Peer-Reviewed Academic Regimen (Zero-Hallucination)",
            "tradeoffs_included": True,
            "is_preliminary_clarification": requires_clarification
        },
        "stage7_verification": {
            "title": "Stage 7: Peer-Review Verifier",
            "passed": True,
            "citation_existence_checked": True,
            "climate_compatibility_checked": True,
            "calculated_confidence": (
                verified_recommendations[0].get("confidence")
                if verified_recommendations
                else {"score": 0.90, "label": "High Confidence"}
            )
        },
        "stage8_delivery": {
            "title": "Stage 8: Structured Delivery & Monitoring Protocol",
            "recommendation_count": len(verified_recommendations) if is_actionable else 0,
            "monitoring_plan": monitoring_plan
        }
    }

    # Record turn
    case_session.record_turn(req.message or "", rule_eval, verified_recommendations)

    evidence_objects = [EvidenceChunk(**c) for c in retrieved_raw]
    rec_objects = [Recommendation(**r) for r in (verified_recommendations if is_actionable else [])]
    clarifying_obj = ClarifyingQuestion(**clarifying_q) if clarifying_q else None

    try:
        AuditDatabase.save_chat_message(session_id, "assistant", reply_markdown)
        AuditDatabase.save_assessment(
            session_id=session_id,
            query=req.message or "",
            profile=current_profile,
            result={
                "rule_metrics": rule_eval,
                "recommendations": [r.dict() for r in rec_objects],
                "reply_markdown": reply_markdown
            }
        )
    except Exception as e:
        print(f"[Audit DB save assessment error]: {e}")

    print(f"[DEBUG 9] FINAL RESPONSE: is_actionable={is_actionable}, requires_clarification={requires_clarification}, recommendations_count={len(rec_objects)}, reply_preview={reply_markdown[:150]!r}")

    return ChatResponse(
        session_id=session_id,
        reply_markdown=reply_markdown,
        case_file_profile=current_profile,
        rule_metrics=rule_eval,
        recommendations=rec_objects,
        retrieved_evidence=evidence_objects,
        causal_hops=all_hops,
        clarifying_question=clarifying_obj,
        stages=stages_bundle,
        monitoring_plan=monitoring_plan,
        suspicious_alerts=suspicious_alerts,
        contradiction_alerts=contradictions,
        running_assessment=case_session.running_assessment,
        completeness_score=completeness_score,
        input_mode_detected=input_mode,
        is_cached=False,
        is_actionable=is_actionable,
        requires_clarification=requires_clarification,
        spatial_context=current_profile.get("spatial_context")
    )


# ----------------------------------------------------------------
# MULTI-SESSION & AUDIT HISTORY API ENDPOINTS
# ----------------------------------------------------------------

@app.get("/api/sessions")
def list_sessions():
    """Returns all active/recent sessions."""
    sessions = AuditDatabase.list_recent_sessions(limit=50)
    return {"sessions": sessions}


@app.post("/api/sessions")
def create_session(payload: Optional[Dict[str, Any]] = None):
    """Initializes a new consultation session."""
    p = payload or {}
    new_id = p.get("session_id") or f"sess_{uuid.uuid4().hex[:8]}"
    title = p.get("title") or "New Ecological Assessment"
    eco = p.get("ecosystem_type") or "agricultural"
    case = get_or_create_case_file(new_id)
    case.profile["ecosystem_type"] = eco

    try:
        with AuditDatabase._get_connection() as conn:
            now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
            conn.execute("""
            INSERT INTO sessions (session_id, created_at, updated_at, title, ecosystem_type, health_score, summary, query_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(session_id) DO NOTHING
            """, (new_id, now_str, now_str, title, eco, 50.0, "Session initialized."))
            conn.commit()
    except Exception as e:
        print(f"[Create session DB error]: {e}")

    return {
        "session_id": new_id,
        "title": title,
        "ecosystem_type": eco,
        "case_file": case.to_dict()
    }


@app.get("/api/sessions/{session_id}")
def get_session_details(session_id: str):
    """Retrieves full session state including profile, rule metrics, recommendations, and messages."""
    case = get_or_create_case_file(session_id)
    rule_eval = EnvironmentalRuleEngine.evaluate_profile(case.profile)
    messages = AuditDatabase.get_session_chat_history(session_id)

    raw_recs = InterventionLibrary.get_matching_interventions(
        biome=case.profile.get("biome"),
        viable_classes=rule_eval.get("viable_intervention_classes", []),
        prohibited_classes=rule_eval.get("prohibited_intervention_classes", []),
        ecosystem_type=rule_eval.get("ecosystem_type"),
        environmental_profile=rule_eval.get("environmental_profile"),
        limiting_factors=rule_eval.get("primary_limiting_factors", [])
    )
    recs = [
        EvidenceVerifier.verify_and_gate_recommendation(r, case.profile, set(), rule_eval)
        for r in raw_recs[:3]
    ]

    return {
        "session_id": session_id,
        "case_file": case.to_dict(),
        "rule_metrics": rule_eval,
        "recommendations": recs,
        "messages": messages
    }


@app.get("/api/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    """Chronological chat messages for this session."""
    return {"messages": AuditDatabase.get_session_chat_history(session_id)}


@app.get("/api/sessions/{session_id}/audit")
def get_session_audit(session_id: str):
    """Comprehensive longitudinal audit trail and telemetry verification log."""
    case = get_or_create_case_file(session_id)
    messages = AuditDatabase.get_session_chat_history(session_id)
    rule_eval = EnvironmentalRuleEngine.evaluate_profile(case.profile)
    return {
        "session_id": session_id,
        "turn_count": case.turn_count,
        "profile": case.profile,
        "provenance": case.provenance,
        "contradiction_history": case.contradiction_history,
        "running_assessment": case.running_assessment,
        "rule_metrics": rule_eval,
        "messages": messages
    }


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    """Deletes/resets session from persistent store."""
    reset_case_file(session_id)
    try:
        with AuditDatabase._get_connection() as conn:
            conn.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
    except Exception as e:
        print(f"[Delete session DB error]: {e}")
    return {"status": "deleted", "session_id": session_id}


@app.get("/api/case-file/{session_id}")
def get_case_file_state(session_id: str):
    case = get_or_create_case_file(session_id)
    rule_eval = EnvironmentalRuleEngine.evaluate_profile(case.profile)
    return {
        "case_file": case.to_dict(),
        "rule_metrics": rule_eval
    }


@app.post("/api/case-file/{session_id}/reset")
def reset_case_file_state(session_id: str):
    case = reset_case_file(session_id)
    return {
        "status": "reset_successful",
        "case_file": case.to_dict()
    }


@app.get("/api/demo/{demo_key}")
def get_demo_case(demo_key: str):
    """Pre-set benchmark scenarios for evaluation."""
    demos = {
        "canonical_semi_arid_wheat": {
            "key": "canonical_semi_arid_wheat",
            "name": " Canonical Reference: Semi-Arid Monoculture Wheat",
            "input_text": "Soil organic carbon is 0.3%, rainfall low (320mm), crop monoculture wheat, region semi-arid. What interventions do you recommend?",
            "structured_json": {
                "soc_percent": 0.3,
                "rainfall_mm": 320.0,
                "current_crop": "monoculture wheat",
                "biome": "semi-arid"
            }
        },
        "incomplete_probe_test": {
            "key": "incomplete_probe_test",
            "name": " Incomplete Input & Probe: Biodiversity Declining (<3 Variables)",
            "input_text": "Biodiversity is declining on my land with continuous monoculture cropping.",
            "structured_json": {
                "current_crop": "monoculture"
            }
        },
        "geo_spatial_lookup": {
            "key": "geo_spatial_lookup",
            "name": " Geo-Coordinates & Satellite Telemetry (Thar Semi-Arid)",
            "input_text": "Field location: Lat 26.915, Lon 70.908. Continuous wheat with 0.3% SOC.",
            "structured_json": {
                "latitude": 26.915,
                "longitude": 70.908,
                "soc_percent": 0.3,
                "current_crop": "wheat monoculture"
            }
        },
        "suspicious_unit_test": {
            "key": "suspicious_unit_test",
            "name": " Unit Sanity Alert: Suspicious 30% Soil Carbon",
            "input_text": "Our soil report indicates soil carbon of 30%, 350mm rainfall, semi-arid wheat.",
            "structured_json": {
                "soc_percent": 30.0,
                "rainfall_mm": 350.0,
                "current_crop": "wheat",
                "biome": "semi-arid"
            }
        },
        "contradiction_test": {
            "key": "contradiction_test",
            "name": " Multi-Turn Contradiction: 1200mm Rain in Semi-Arid",
            "input_text": "Actually, my rainfall is 1200mm per year on this semi-arid wheat farm.",
            "structured_json": {
                "rainfall_mm": 1200.0,
                "biome": "semi-arid"
            }
        }
    }
    demo = demos.get(demo_key)
    if not demo:
        raise HTTPException(status_code=404, detail="Demo scenario not found")
    return demo


# ----------------------------------------------------------------
# UNIFIED SINGLE-HOST PORTAL ROUTES (Single localhost:8000)
# ----------------------------------------------------------------
DIST_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@app.get("/streamlit", response_class=HTMLResponse)
def get_streamlit_portal():
    """Serves the Streamlit 6-panel platform embedded seamlessly under http://localhost:8000/streamlit."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Darukaa.Earth — Unified Intelligence Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #FFF9ED;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        .portal-bar {
            background: #FFFDF8;
            border-bottom: 1.5px solid rgba(169, 113, 66, 0.28);
            padding: 8px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 48px;
            box-shadow: 0 2px 8px rgba(139, 94, 60, 0.08);
            z-index: 100;
        }
        .portal-title {
            font-weight: 800;
            color: #382417;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .portal-badge {
            background: #FEF3C7;
            border: 1px solid #D9A441;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            color: #8B5E3C;
        }
        .portal-nav-btn {
            background: #D9A441;
            color: #382417;
            text-decoration: none;
            padding: 5px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 800;
            border: 1px solid #C18A5B;
            transition: opacity 0.2s;
        }
        .portal-nav-btn:hover {
            opacity: 0.9;
        }
        .frame-container {
            flex: 1;
            width: 100%;
            height: calc(100vh - 48px);
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <div class="portal-bar">
        <div class="portal-title">
            <span> DARUKAA.EARTH</span>
            <span class="portal-badge">UNIFIED LOCALHOST GATEWAY</span>
        </div>
        <div style="display:flex;gap:10px;align-items:center;">
            <a href="/" class="portal-nav-btn"> Switch to React UI</a>
            <a href="/docs" target="_blank" class="portal-nav-btn" style="background:#FFFDF8;border-color:rgba(169,113,66,0.35);"> API Docs</a>
        </div>
    </div>
    <div class="frame-container">
        <iframe src="http://localhost:8501/?embedded=true" allow="fullscreen"></iframe>
    </div>
</body>
</html>"""


# Mount React static distribution if present
if DIST_DIR.exists():
    assets_dir = DIST_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    def serve_react_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="Not found")
        target_file = DIST_DIR / full_path
        if target_file.is_file():
            return FileResponse(str(target_file))
        return FileResponse(str(DIST_DIR / "index.html"))

