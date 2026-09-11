"""
Curated Intervention Library & Contextual Scoring Engine — Stage 5
Darukaa.Earth AI Biodiversity Intelligence Platform

Loads interventions.json and dynamically evaluates and ranks candidates against:
- Context Relevance (Ecosystem & Biome congruence)
- Limiting Factor & Constraint Resolution
- Multi-Metric Ecological Impact
- Evidence Strength & Scientific Verification
- Site-Specific Feasibility vs Trade-Off Risks

Also generates dynamic, condition-based "Why this was selected" justifications.
"""

import json
import os
from typing import List, Dict, Any, Optional


class InterventionLibrary:
    """Curated intervention lookup, scoring, and ranking engine."""

    _INTERVENTIONS: List[Dict[str, Any]] = []

    @classmethod
    def load(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "data", "interventions.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                cls._INTERVENTIONS = json.load(f)
        else:
            cls._INTERVENTIONS = []

    @classmethod
    def get_all_curated_interventions(cls) -> List[Dict[str, Any]]:
        cls.load()
        return list(cls._INTERVENTIONS)

    @classmethod
    def get_matching_interventions(
        cls,
        biome: Optional[str] = None,
        viable_classes: Optional[List[str]] = None,
        prohibited_classes: Optional[List[str]] = None,
        ecosystem_type: Optional[str] = None,
        environmental_profile: Optional[Dict[str, Any]] = None,
        limiting_factors: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        cls.load()
        biome_lower = (biome or "").lower().replace(" ", "-")
        eco_type = (ecosystem_type or "").lower()
        viable = viable_classes or []
        prohibited = prohibited_classes or []
        lim_factors = limiting_factors or []

        scored_candidates = []

        for item in cls._INTERVENTIONS:
            intervention = dict(item)
            category = intervention.get("category", "")

            # Hard gate: Check prohibited classes
            if any(p in category for p in prohibited):
                continue

            # -------------------------------------------------------------
            # 1. Context Relevance Score (0 to 40)
            # -------------------------------------------------------------
            context_score = 0.0

            # Ecosystem congruence
            applicable_ecos = [e.lower() for e in intervention.get("applicable_ecosystems", [])]
            if eco_type:
                if eco_type in applicable_ecos:
                    context_score += 20.0
                elif not applicable_ecos:
                    context_score += 8.0
                else:
                    # Incompatible ecosystem
                    context_score -= 25.0

            # Biome congruence
            applicable_biomes = [b.lower().replace(" ", "-") for b in intervention.get("applicable_biomes", [])]
            if biome_lower:
                if any(b in biome_lower or biome_lower in b for b in applicable_biomes):
                    context_score += 15.0
                elif not applicable_biomes:
                    context_score += 5.0

            # Viable category priority
            if category in viable:
                rank_idx = viable.index(category)
                context_score += max(2.0, 10.0 - rank_idx * 2.0)

            # -------------------------------------------------------------
            # 2. Target Constraint Resolution Score (0 to 30)
            # -------------------------------------------------------------
            constraint_score = 0.0
            target_constraints = intervention.get("target_constraints", [])
            lim_text = " ".join(lim_factors).lower()

            for tc in target_constraints:
                tc_clean = tc.replace("_", " ")
                if tc in lim_text or tc_clean in lim_text:
                    constraint_score += 8.0
                # Check against environmental profile values
                if environmental_profile:
                    soil_status = environmental_profile.get("soil_condition", {}).get("status", "")
                    water_status = environmental_profile.get("water_condition", {}).get("status", "")
                    water_qual = environmental_profile.get("water_condition", {}).get("water_quality", "")
                    if tc == "low_soc" and "depleted" in soil_status:
                        constraint_score += 6.0
                    if tc in ["low_rainfall", "high_evaporative_loss"] and "water_limited" in water_status:
                        constraint_score += 6.0
                    if tc in ["urban_runoff", "water_quality_decline"] and water_qual in ["polluted", "poor"]:
                        constraint_score += 8.0
                    if tc in ["eutrophication", "excess_nitrogen_phosphorus"] and water_qual == "eutrophic":
                        constraint_score += 8.0
                    if tc in ["habitat_fragmentation", "deforestation"] and eco_type == "forest":
                        constraint_score += 8.0
                    if tc in ["nutrient_leaching", "steep_slope_erosion"] and "excess" in water_status:
                        constraint_score += 8.0

            constraint_score = min(30.0, constraint_score)

            # -------------------------------------------------------------
            # 3. Multi-Metric Impact (0 to 15)
            # -------------------------------------------------------------
            metrics_count = len(intervention.get("impacted_metrics", []))
            metric_score = min(15.0, metrics_count * 3.5)

            # -------------------------------------------------------------
            # 4. Evidence Strength (0 to 15)
            # -------------------------------------------------------------
            conf_data = intervention.get("confidence", {})
            conf_val = conf_data.get("score", 0.90)
            evidence_score = round(conf_val * 15.0, 1)

            # -------------------------------------------------------------
            # 5. Feasibility / Risk Penalty (-10 to 0)
            # -------------------------------------------------------------
            risk_penalty = 0.0
            trade_offs = intervention.get("trade_offs", [])
            if eco_type == "agricultural" and biome_lower in ["semi-arid", "arid"]:
                # Check for moisture penalty
                if "water" in " ".join(trade_offs).lower() and "cover crop" in intervention.get("name", "").lower():
                    # If rainfall < 350mm, slight penalty unless terminated early
                    rf = environmental_profile.get("water_condition", {}).get("rainfall_mm") if environmental_profile else None
                    if rf and rf < 350:
                        risk_penalty += 3.0

            # Total Recommendation Score
            total_score = round(context_score + constraint_score + metric_score + evidence_score - risk_penalty, 2)

            # -------------------------------------------------------------
            # 6. Generate Dynamic "Why This Recommendation Was Selected"
            # -------------------------------------------------------------
            why_text = cls._generate_why_selected(
                rec=intervention,
                profile=environmental_profile,
                limiting_factors=lim_factors,
                ecosystem_type=eco_type
            )
            intervention["why_selected"] = why_text
            intervention["recommendation_score"] = total_score

            scored_candidates.append({
                "intervention": intervention,
                "score": total_score
            })

        # Sort descending by contextual recommendation score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)

        results = [item["intervention"] for item in scored_candidates if item["score"] > 15.0]

        # Fallback guarantee if no high scorers passed
        if len(results) < 2:
            results = [item["intervention"] for item in scored_candidates[:3]]

        # Return top 3 contextually ranked interventions
        return results[:3]

    @classmethod
    def _generate_why_selected(
        cls,
        rec: Dict[str, Any],
        profile: Optional[Dict[str, Any]],
        limiting_factors: List[str],
        ecosystem_type: str
    ) -> str:
        """Generates dynamic, condition-based explanation tailored to user's parameters without inventing metrics."""
        cat = rec.get("category", "")

        if not profile:
            return f"Selected based on peer-reviewed evidence ({rec.get('confidence', {}).get('score', 0.9):.0%}) and applicability to {ecosystem_type} systems."

        soil = profile.get("soil_condition", {})
        water = profile.get("water_condition", {})
        land = profile.get("land_condition", {})

        soc_val = soil.get("organic_carbon")
        rain_val = water.get("rainfall_mm")
        crop_val = land.get("land_use")

        context_clauses = []
        if soc_val is not None:
            context_clauses.append(f"SOC of {soc_val}%")
        if rain_val is not None:
            context_clauses.append(f"annual rainfall of {rain_val} mm")
        if crop_val:
            context_clauses.append(f"cropping system ({crop_val})")
        site_ctx = f" For your reported conditions ({', '.join(context_clauses)}):" if context_clauses else ""

        if cat == "cover_crops":
            return f"{site_ctx} Cover crops maintain continuous living root exudation, mitigating erosion and rebuilding organic matter pools during fallow periods."
        elif cat == "field_margins":
            return f"{site_ctx} Field margins provide non-crop vegetative buffers and continuous floral resources, restoring natural beneficial arthropods and wild pollinator habitat."
        elif cat == "crop_rotation":
            return f"{site_ctx} Crop rotation disrupts single-crop pathogen cycles and balances soil nutrient extraction across distinct root zones."
        elif cat == "residue_retention":
            return f"{site_ctx} Surface residue retention provides an evaporative barrier and thermal buffer against topsoil drying and wind erosion."
        elif cat == "agroforestry":
            return f"{site_ctx} Agroforestry incorporates perennial woody structures to reduce wind speeds, cycle deep nutrients, and enhance microclimatic buffering."
        elif cat == "reduced_tillage":
            return f"{site_ctx} Reduced tillage preserves soil macroaggregate structure and mycorrhizal hyphal networks by minimizing mechanical inversion."
        else:
            return f"{site_ctx} Selected to address primary identified constraints: {'; '.join(limiting_factors[:2]) if limiting_factors else 'ecological degradation'}."
