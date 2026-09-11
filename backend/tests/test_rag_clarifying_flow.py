"""
Test Suite: RAG Knowledge Layer, Multi-Turn Memory & Adaptive Clarifying Questions
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.pipeline.input_parser import InputParser
from backend.pipeline.completeness_check import CompletenessChecker
from backend.pipeline.retrieval import KnowledgeRetriever
from backend.pipeline.rule_engine import EnvironmentalRuleEngine
from backend.models.case_file import get_or_create_case_file, reset_case_file
from backend.pipeline.intervention_library import InterventionLibrary
from backend.pipeline.reasoning_graph import MultiMetricReasoningGraph
from backend.pipeline.verifier import EvidenceVerifier


def test_knowledge_base_catalog_and_rag():
    print("--- 1. Testing RAG Knowledge Base & Catalog ---")
    catalog = KnowledgeRetriever.get_knowledge_catalog()
    assert catalog["total_papers_indexed"] >= 10, f"Expected >= 10 papers, got {catalog['total_papers_indexed']}"
    assert catalog["vocab_dimensions"] > 50, f"Expected vocab > 50, got {catalog['vocab_dimensions']}"
    assert "benchmarks_dataset" in catalog
    print(f"[OK] Indexed {catalog['total_papers_indexed']} papers, vocab size: {catalog['vocab_dimensions']}")

    # Test retrieval with dryland query
    chunks, dissenting, trace = KnowledgeRetriever.retrieve_evidence(
        query="cover crop moisture competition and soil carbon",
        biome="semi-arid",
        top_k=5
    )
    assert len(chunks) > 0, "Expected retrieved chunks"
    assert len(dissenting) > 0, "Expected CSIRO dissenting evidence surfaced"
    print(f"[OK] Retrieved {len(chunks)} evidence chunks; Dissenting surfaced: {dissenting[0]['chunk_id']}")


def test_incomplete_input_clarifying_triad():
    print("\n--- 2. Testing Incomplete Input & Proactive Clarifying Question ---")
    session_id = "test_multi_turn_session"
    reset_case_file(session_id)
    case_session = get_or_create_case_file(session_id)

    # Turn 1: User gives vague input
    user_input_1 = "Biodiversity is declining on my land"
    data, mode, ambiguities = InputParser.parse_input(user_input_1)
    case_session.update_profile(data)

    eval_res = CompletenessChecker.evaluate_completeness(case_session.profile, ambiguities)
    assert eval_res["requires_clarification"] is True, "Expected requires_clarification to be True"
    assert eval_res["is_actionable"] is False, "Expected is_actionable to be False"

    cq = eval_res["primary_question"]
    assert cq is not None, "Expected primary clarifying question"
    assert "Soil Organic Carbon" in cq["question_text"]
    assert "rainfall pattern" in cq["question_text"].lower()
    assert "land use type" in cq["question_text"].lower()
    assert len(cq["suggested_inputs"]) >= 4, "Expected >= 4 suggested preset options"
    assert cq["allow_custom_input"] is True, "Expected allow_custom_input to be True"
    assert len(cq["custom_input_fields"]) >= 3, "Expected custom input fields for triad"

    print("[OK] Clarifying question successfully generated:")
    print(f"  Question: {cq['question_text']}")
    print(f"  Preset options: {len(cq['suggested_inputs'])} options")
    print(f"  Custom input enabled: {cq['allow_custom_input']}")


def test_multi_turn_memory_and_adaptation():
    print("\n--- 3. Testing Multi-Turn Memory & Adaptation ---")
    session_id = "test_multi_turn_session"
    case_session = get_or_create_case_file(session_id)

    # Turn 2: User supplies custom telemetry
    user_input_2 = "Supplemental Field Telemetry: SOC 0.35%, rainfall 340mm unimodal, land use continuous wheat monoculture"
    data_2, mode_2, amb_2 = InputParser.parse_input(user_input_2)

    case_session.update_profile(data_2)
    profile = case_session.profile

    assert profile["soc_percent"] == 0.35, f"Expected SOC 0.35, got {profile.get('soc_percent')}"
    assert profile["rainfall_mm"] == 340.0, f"Expected rainfall 340.0, got {profile.get('rainfall_mm')}"
    assert "wheat" in (profile["current_crop"] or ""), f"Expected wheat crop, got {profile.get('current_crop')}"

    # Re-evaluate completeness
    eval_res_2 = CompletenessChecker.evaluate_completeness(profile)
    assert eval_res_2["is_actionable"] is True, "Expected is_actionable to be True on Turn 2"
    assert eval_res_2["requires_clarification"] is False, "Expected requires_clarification to be False"

    # Rule Engine + RAG Pipeline execution
    rule_eval = EnvironmentalRuleEngine.evaluate_profile(profile)
    assert rule_eval["soc_metrics"]["deficit_percent"] > 0, "Expected positive SOC deficit percentage (depleted)"

    chunks, dissenting, trace = KnowledgeRetriever.retrieve_evidence(
        query="wheat monoculture soil organic carbon restoration",
        biome=profile.get("biome") or "semi-arid",
        top_k=6
    )
    assert len(chunks) > 0

    chains = MultiMetricReasoningGraph.generate_causal_chains(profile, rule_eval)
    assert len(chains) > 0, "Expected multi-metric causal chains generated"

    interventions = InterventionLibrary.get_matching_interventions(
        biome="semi-arid",
        viable_classes=rule_eval.get("viable_intervention_classes", []),
        prohibited_classes=rule_eval.get("prohibited_intervention_classes", [])
    )
    assert len(interventions) > 0

    gated_recs = []
    chunk_ids = {c["id"] for c in chunks}
    for item in interventions[:3]:
        r = EvidenceVerifier.verify_and_gate_recommendation(item, profile, chunk_ids, rule_eval)
        gated_recs.append(r)

    assert len(gated_recs) >= 2, "Expected at least 2 verified recommendations"
    print(f"[OK] Turn 2 successfully adapted: System actionable, {len(gated_recs)} interventions verified with citations.")
    for r in gated_recs:
        print(f"  - Intervention: {r['name']} | Confidence: {r.get('confidence', {}).get('score')}")

    print("\n[SUCCESS] ALL MULTI-TURN RAG AND CLARIFYING TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_knowledge_base_catalog_and_rag()
    test_incomplete_input_clarifying_triad()
    test_multi_turn_memory_and_adaptation()
