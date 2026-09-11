"""
Automated Personalization & Dynamic Environmental Reasoning Test Suite
Darukaa.Earth AI Biodiversity Intelligence Platform

Verifies that:
1. Different environmental conditions produce different profiles and limiting factors.
2. Contextual RAG retrieves different, relevant peer-reviewed evidence for each ecosystem.
3. Recommendations are dynamically scored and ranked according to actual site conditions.
4. Explanations answer "Why this recommendation was selected" using actual user variables.
5. Incomplete inputs generate ecosystem-appropriate clarifying questions.
6. Multi-turn memory accumulates context across conversation turns.
7. No hardcoded or generic fallback recommendations are returned.
"""

import pytest
from backend.pipeline.input_parser import InputParser
from backend.pipeline.completeness_check import CompletenessChecker
from backend.pipeline.rule_engine import EnvironmentalRuleEngine
from backend.pipeline.retrieval import KnowledgeRetriever
from backend.pipeline.intervention_library import InterventionLibrary
from backend.pipeline.reasoning_graph import MultiMetricReasoningGraph
from backend.models.case_file import get_or_create_case_file, reset_case_file


@pytest.fixture(scope="module", autouse=True)
def init_retriever():
    KnowledgeRetriever.load_chunks()
    InterventionLibrary.load()


class TestDynamicPersonalization:

    def test_scenario_a_vs_b_distinct_reasoning(self):
        """Principle: Same question + different conditions MUST produce different recommendations."""
        q = "What interventions do you recommend to restore biodiversity and improve resilience on my land?"

        user_a_input = f"""
        {q}
        Region: semi-arid
        Rainfall: low
        Soil organic carbon: 0.3%
        Land use: monoculture wheat
        Biodiversity: low
        """

        user_b_input = f"""
        {q}
        Region: high rainfall
        Rainfall: high
        Soil organic carbon: 2.8%
        Land use: mixed agroforestry
        Biodiversity: moderate
        """

        # User A pipeline
        p_a, _, _ = InputParser.parse_input(user_a_input)
        eval_a = EnvironmentalRuleEngine.evaluate_profile(p_a)
        recs_a = InterventionLibrary.get_matching_interventions(
            biome=p_a.get("biome"),
            viable_classes=eval_a.get("viable_intervention_classes"),
            prohibited_classes=eval_a.get("prohibited_intervention_classes"),
            ecosystem_type=eval_a.get("ecosystem_type"),
            environmental_profile=eval_a.get("environmental_profile"),
            limiting_factors=eval_a.get("primary_limiting_factors")
        )

        # User B pipeline
        p_b, _, _ = InputParser.parse_input(user_b_input)
        eval_b = EnvironmentalRuleEngine.evaluate_profile(p_b)
        recs_b = InterventionLibrary.get_matching_interventions(
            biome=p_b.get("biome"),
            viable_classes=eval_b.get("viable_intervention_classes"),
            prohibited_classes=eval_b.get("prohibited_intervention_classes"),
            ecosystem_type=eval_b.get("ecosystem_type"),
            environmental_profile=eval_b.get("environmental_profile"),
            limiting_factors=eval_b.get("primary_limiting_factors")
        )

        # 1. Profiles must be distinct
        assert p_a.get("soc_percent") == 0.3
        assert p_b.get("soc_percent") == 2.8
        assert p_a.get("rainfall_mm") == 320.0
        assert p_b.get("rainfall_mm") == 1250.0

        # 2. Limiting factors must be distinct
        lim_a = " ".join(eval_a["primary_limiting_factors"]).lower()
        lim_b = " ".join(eval_b["primary_limiting_factors"]).lower()
        assert "carbon" in lim_a or "aridity" in lim_a
        assert "leaching" in lim_b or "runoff" in lim_b

        # 3. Recommendations must be distinct (non-identical)
        ids_a = [r["id"] for r in recs_a]
        ids_b = [r["id"] for r in recs_b]
        assert ids_a != ids_b, f"User A and User B received identical recommendations: {ids_a}"

        # 4. User A must get dryland interventions
        assert any(x in ids_a for x in ["INT-AGROFORESTRY-DRYLAND", "INT-LEGUME-INTERCROPPING", "INT-CONSERVATION-TILLAGE-MULCH"])

        # 5. User B must get high-rainfall / agroforestry interventions
        assert any(x in ids_b for x in ["INT-TROPICAL-SHADED-AGROFORESTRY", "INT-CONTOUR-VETIVER-BUFFER"])

    def test_scenario_c_urban_lake(self):
        """Urban ecosystem: recognizes urban context, retrieves urban literature, recommends bioswales/pocket forests."""
        user_c_input = "Bird diversity around my urban lake has decreased. High pollution and low green space."

        p_c, _, amb = InputParser.parse_input(user_c_input)
        assert p_c.get("ecosystem_type") == "urban"
        assert p_c.get("pollution_level") == "high"
        assert p_c.get("green_space_ratio") == "low"

        eval_c = EnvironmentalRuleEngine.evaluate_profile(p_c)
        assert eval_c["ecosystem_type"] == "urban"

        # Check limiting factors
        lim_text = " ".join(eval_c["primary_limiting_factors"]).lower()
        assert "urban" in lim_text or "runoff" in lim_text or "pollution" in lim_text

        # Check RAG retrieval
        retrieved, _, _ = KnowledgeRetriever.retrieve_evidence(
            query=user_c_input,
            biome=p_c.get("biome"),
            steer_terms=eval_c.get("query_steer_terms"),
            top_k=4
        )
        retrieved_ids = [r["id"] for r in retrieved]
        assert any(x in retrieved_ids for x in ["EPA-URBAN-STORMWATER-2021", "NATURE-SUSTAINABILITY-URBAN-2022"])

        # Check recommendations
        recs_c = InterventionLibrary.get_matching_interventions(
            biome=p_c.get("biome"),
            viable_classes=eval_c.get("viable_intervention_classes"),
            prohibited_classes=eval_c.get("prohibited_intervention_classes"),
            ecosystem_type=eval_c.get("ecosystem_type"),
            environmental_profile=eval_c.get("environmental_profile"),
            limiting_factors=eval_c.get("primary_limiting_factors")
        )
        rec_ids = [r["id"] for r in recs_c]
        assert "INT-URBAN-BIOSWALE-FILTER" in rec_ids or "INT-URBAN-POCKET-FOREST" in rec_ids
        assert "INT-LEGUME-INTERCROPPING" not in rec_ids

    def test_scenario_d_wetland(self):
        """Wetland ecosystem: recognizes eutrophication and drawdown, recommends buffer strips / sills."""
        user_d_input = "Wetland with high agricultural pollution, declining water level, and eutrophic algal blooms."

        p_d, _, _ = InputParser.parse_input(user_d_input)
        assert p_d.get("ecosystem_type") == "wetland"
        assert p_d.get("water_quality") == "eutrophic"
        assert p_d.get("water_level") == "declining"

        eval_d = EnvironmentalRuleEngine.evaluate_profile(p_d)
        lim_text = " ".join(eval_d["primary_limiting_factors"]).lower()
        assert "eutrophication" in lim_text or "nutrient" in lim_text or "drawdown" in lim_text

        # RAG retrieval
        retrieved, _, _ = KnowledgeRetriever.retrieve_evidence(
            query=user_d_input,
            biome=p_d.get("biome"),
            steer_terms=eval_d.get("query_steer_terms"),
            top_k=4
        )
        retrieved_ids = [r["id"] for r in retrieved]
        assert "RAMSAR-WETLAND-RESTORATION-2021" in retrieved_ids

        # Recommendations
        recs_d = InterventionLibrary.get_matching_interventions(
            biome=p_d.get("biome"),
            viable_classes=eval_d.get("viable_intervention_classes"),
            prohibited_classes=eval_d.get("prohibited_intervention_classes"),
            ecosystem_type=eval_d.get("ecosystem_type"),
            environmental_profile=eval_d.get("environmental_profile"),
            limiting_factors=eval_d.get("primary_limiting_factors")
        )
        rec_ids = [r["id"] for r in recs_d]
        assert "INT-WETLAND-RIPARIAN-FILTER" in rec_ids or "INT-WETLAND-HYDRO-RESTORE" in rec_ids
        assert "INT-CONSERVATION-TILLAGE-MULCH" not in rec_ids

    def test_scenario_e_forest(self):
        """Forest ecosystem: recognizes fragmentation and deforestation, recommends corridors and ANR."""
        user_e_input = "Forest with severe habitat fragmentation, high deforestation, and canopy cover down to 25%."

        p_e, _, _ = InputParser.parse_input(user_e_input)
        assert p_e.get("ecosystem_type") == "forest"
        assert p_e.get("fragmentation_index") == "high"
        assert p_e.get("canopy_cover_pct") == 25.0

        eval_e = EnvironmentalRuleEngine.evaluate_profile(p_e)
        lim_text = " ".join(eval_e["primary_limiting_factors"]).lower()
        assert "fragmentation" in lim_text or "canopy" in lim_text or "deforestation" in lim_text

        # RAG retrieval
        retrieved, _, _ = KnowledgeRetriever.retrieve_evidence(
            query=user_e_input,
            biome=p_e.get("biome"),
            steer_terms=eval_e.get("query_steer_terms"),
            top_k=4
        )
        retrieved_ids = [r["id"] for r in retrieved]
        assert "SCIENCE-FOREST-FRAGMENTATION-2020" in retrieved_ids

        # Recommendations
        recs_e = InterventionLibrary.get_matching_interventions(
            biome=p_e.get("biome"),
            viable_classes=eval_e.get("viable_intervention_classes"),
            prohibited_classes=eval_e.get("prohibited_intervention_classes"),
            ecosystem_type=eval_e.get("ecosystem_type"),
            environmental_profile=eval_e.get("environmental_profile"),
            limiting_factors=eval_e.get("primary_limiting_factors")
        )
        rec_ids = [r["id"] for r in recs_e]
        assert "INT-FOREST-CORRIDOR-LINK" in rec_ids or "INT-FOREST-ANR-ENRICHMENT" in rec_ids
        assert "INT-LEGUME-INTERCROPPING" not in rec_ids

    def test_adaptive_clarifying_questions(self):
        """Never ask an urban or forest user for agricultural soil carbon."""
        # 1. Urban lake without water/green space data
        p_u, _, amb_u = InputParser.parse_input("Bird diversity around my urban lake has decreased.")
        comp_u = CompletenessChecker.evaluate_completeness(p_u, amb_u)
        assert comp_u["requires_clarification"] is True
        q_u = comp_u["primary_question"]["question_text"].lower()
        assert "water quality" in q_u or "pollution" in q_u or "green space" in q_u
        assert "soil organic carbon" not in q_u

        # 2. Forest without canopy/fragmentation data
        p_f, _, amb_f = InputParser.parse_input("Forest is degraded with illegal logging.")
        comp_f = CompletenessChecker.evaluate_completeness(p_f, amb_f)
        assert comp_f["requires_clarification"] is True
        q_f = comp_f["primary_question"]["question_text"].lower()
        assert "canopy" in q_f or "isolation" in q_f or "deforestation" in q_f
        assert "soil organic carbon" not in q_f

        # 3. Agricultural without soil/rainfall data
        p_a, _, amb_a = InputParser.parse_input("Biodiversity is declining on my farm land.")
        comp_a = CompletenessChecker.evaluate_completeness(p_a, amb_a)
        assert comp_a["requires_clarification"] is True
        q_a = comp_a["primary_question"]["question_text"].lower()
        assert "soil organic carbon" in q_a

    def test_multi_turn_memory_accumulation(self):
        """Multi-turn session accumulates variables across turns without restarting from scratch."""
        sid = "pytest_multiturn_session"
        reset_case_file(sid)
        session = get_or_create_case_file(sid)

        # Turn 1
        t1 = "My soil carbon is 0.3%."
        d1, _, a1 = InputParser.parse_input(t1)
        session.update_profile(d1)
        c1 = CompletenessChecker.evaluate_completeness(session.profile, a1)
        assert c1["requires_clarification"] is True

        # Turn 2
        t2 = "Rainfall is low (320mm) and I grow wheat continuously in semi-arid region."
        d2, _, a2 = InputParser.parse_input(t2)
        session.update_profile(d2)
        c2 = CompletenessChecker.evaluate_completeness(session.profile, a2)

        # Must remember turn 1
        assert session.profile.get("soc_percent") == 0.3
        # Must have turn 2
        assert session.profile.get("rainfall_mm") == 320.0
        assert session.profile.get("current_crop") == "wheat"
        # Must be actionable
        assert c2["is_actionable"] is True
        assert session.turn_count == 2
