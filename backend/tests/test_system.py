"""
Comprehensive Automated Verification Suite
Darukaa.Earth AI Biodiversity Intelligence Platform
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.pipeline.input_parser import InputParser
from backend.pipeline.completeness_check import CompletenessChecker
from backend.pipeline.rule_engine import EnvironmentalRuleEngine
from backend.pipeline.retrieval import KnowledgeRetriever
from backend.pipeline.intervention_library import InterventionLibrary
from backend.pipeline.reasoning_graph import MultiMetricReasoningGraph
from backend.pipeline.verifier import InputValidator, EvidenceVerifier
from backend.pipeline.llm_writer import ScientificWriter
from backend.pipeline.spatial_context import SpatialContextEngine
from backend.models.case_file import CaseFileSession


class TestBiodiversityIntelligenceSystem(unittest.TestCase):

    def setUp(self):
        KnowledgeRetriever.load_chunks()

    def test_canonical_semi_arid_wheat(self):
        """Test Case 1: Canonical Reference: SOC 0.3%, 320mm rain, wheat monoculture, semi-arid."""
        text = "Soil organic carbon is 0.3%, rainfall low (320mm), crop monoculture wheat, region semi-arid."
        parsed, mode, ambiguities = InputParser.parse_input(text=text)

        self.assertEqual(parsed.get("soc_percent"), 0.3)
        self.assertEqual(parsed.get("rainfall_mm"), 320.0)
        self.assertIn("wheat", parsed.get("current_crop", "").lower())
        self.assertEqual(parsed.get("biome"), "semi-arid")

        session = CaseFileSession("test_canonical")
        session.update_profile(parsed)

        # Completeness Check
        comp = CompletenessChecker.evaluate_completeness(session.profile)
        self.assertTrue(comp["is_actionable"])
        self.assertFalse(comp["requires_clarification"])
        self.assertGreaterEqual(comp["established_count"], 3)

        # Rule Engine & Hypothesis
        rule_eval = EnvironmentalRuleEngine.evaluate_profile(session.profile)
        self.assertIn("carbon", rule_eval["diagnostic_hypothesis"].lower())
        self.assertIn("dryland_agroforestry_shelterbelts", rule_eval["viable_intervention_classes"])
        self.assertIn("drought_tolerant_legume_intercropping", rule_eval["viable_intervention_classes"])

        # Vector RAG Retrieval
        retrieved, dissenting, trace = KnowledgeRetriever.retrieve_evidence(
            query="dryland wheat soil carbon restoration",
            biome=session.profile["biome"],
            steer_terms=rule_eval["query_steer_terms"]
        )
        self.assertGreaterEqual(len(retrieved), 3)
        retrieved_ids = [r["id"] for r in retrieved]
        self.assertTrue(any("FAO" in rid or "IPCC" in rid for rid in retrieved_ids))

        # Surfaced Dissenting Evidence
        self.assertGreaterEqual(len(dissenting), 1)
        self.assertTrue(any("CSIRO" in d["chunk_id"] for d in dissenting))

        # Multi-Metric Causal Chains
        chains = MultiMetricReasoningGraph.generate_causal_chains(session.profile, rule_eval)
        self.assertGreaterEqual(len(chains), 2)
        for chain in chains:
            self.assertEqual(chain["hop_count"], 3)
            for hop in chain["hops"]:
                self.assertTrue("evidence_ref" in hop or "evidence_citation" in hop)
                self.assertTrue(len(hop["scientific_principle"]) > 10)

        # Synthesis
        recs = InterventionLibrary.get_matching_interventions(
            biome="semi-arid",
            viable_classes=rule_eval["viable_intervention_classes"],
            prohibited_classes=rule_eval["prohibited_intervention_classes"]
        )
        writeup = ScientificWriter.synthesize_response(
            query=text,
            profile=session.profile,
            rule_eval=rule_eval,
            recommendations=recs,
            retrieved_evidence=retrieved,
            causal_chains=chains,
            completeness_eval=comp
        )
        self.assertIn("Soil Organic Carbon", writeup)
        self.assertIn("FAO", writeup)

    def test_incomplete_input_gate(self):
        """Test Case 2: Incomplete input (< 3 variables) must trigger clarifying questions."""
        text = "Biodiversity is declining on my land with continuous monoculture wheat."
        parsed, mode, ambiguities = InputParser.parse_input(text=text)

        session = CaseFileSession("test_incomplete")
        session.update_profile(parsed)

        comp = CompletenessChecker.evaluate_completeness(session.profile, detected_ambiguities=ambiguities)
        self.assertFalse(comp["is_actionable"])
        self.assertTrue(comp["requires_clarification"])
        self.assertLess(comp["established_count"], 3)
        self.assertIsNotNone(comp["primary_question"])

        rule_eval = EnvironmentalRuleEngine.evaluate_profile(session.profile)
        writeup = ScientificWriter.synthesize_response(
            query=text,
            profile=session.profile,
            rule_eval=rule_eval,
            recommendations=[],
            retrieved_evidence=[],
            causal_chains=[],
            clarifying_question=comp["primary_question"],
            completeness_eval=comp
        )
        self.assertIn("Preliminary Environmental Assessment", writeup)
        self.assertIn("minimum of 3 environmental dimensions", writeup)

    def test_geo_spatial_lookup(self):
        """Test Case 3: Geo-coordinates resolution to agro-climatic zone and satellite telemetry."""
        lat = 26.915
        lon = 70.908
        spatial = SpatialContextEngine.lookup_coordinates(lat, lon)

        self.assertTrue(spatial["matched"])
        self.assertIn("Thar", spatial["zone_name"])
        self.assertEqual(spatial["biome"], "semi-arid")
        self.assertEqual(spatial["annual_rainfall_mm"], 310.0)
        self.assertIn("ISRO Bhuvan", spatial["telemetry_source"])
        self.assertIsNotNone(spatial["satellite_ndvi"])

        profile = {"latitude": lat, "longitude": lon}
        enriched = SpatialContextEngine.enrich_profile(profile)
        self.assertEqual(enriched["biome"], "semi-arid")
        self.assertEqual(enriched["rainfall_mm"], 310.0)

    def test_bounds_and_contradictions(self):
        """Test Case 4: Physical bounds sanitization and multi-turn contradiction detection."""
        # Suspicious unit
        data_suspicious = {"soc_percent": 30.0, "rainfall_mm": 350.0}
        valid, errs, alerts = InputValidator.validate_bounds_and_units(data_suspicious)
        self.assertTrue(valid)
        self.assertEqual(len(alerts), 1)
        self.assertIn("unusually high", alerts[0]["message"])

        # Hard physical bound error
        data_impossible = {"soc_percent": -5.0, "ph": 16.0}
        valid2, errs2, alerts2 = InputValidator.validate_bounds_and_units(data_impossible)
        self.assertFalse(valid2)
        self.assertGreaterEqual(len(errs2), 2)

        # Multi-turn contradiction: 1200mm in semi-arid wheat
        prior = {"rainfall_mm": 320.0, "biome": "semi-arid"}
        incoming = {"rainfall_mm": 1200.0}
        contradictions = InputValidator.detect_multi_turn_contradictions(prior, incoming)
        self.assertGreaterEqual(len(contradictions), 1)
        self.assertEqual(contradictions[0]["field"], "rainfall_mm")


if __name__ == "__main__":
    unittest.main()
