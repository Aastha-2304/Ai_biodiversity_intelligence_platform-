"""
Deterministic Rule Engine & Environmental Profile Builder — Stage 3
Darukaa.Earth AI Biodiversity Intelligence Platform

Transforms user input into a rigorous, condition-based Environmental Profile across
all ecosystems (Agricultural, Urban, Wetland, Forest, Grassland), dynamically identifies
the primary limiting factors and variable interactions, and constructs context-specific
retrieval queries and biophysical intervention gates.
"""

from typing import Any, Dict, List, Optional


class EnvironmentalRuleEngine:
    """Deterministic biophysical rule engine and multi-ecosystem profiler."""

    # -----------------------------------------------------------------------
    # SOC Targets by Biome / Ecosystem
    # -----------------------------------------------------------------------
    SOC_TARGETS = {
        "semi-arid":          1.50,
        "arid":               0.80,
        "mediterranean":      2.00,
        "temperate-grassland": 2.50,
        "humid-subtropical":  2.80,
        "high-rainfall":      3.50,
        "tropical-rainforest": 4.00,
        "tropical-savanna":   1.20,
        "freshwater-wetland": 5.00,
        "urban":              1.80,
        "default":            1.50
    }

    # -----------------------------------------------------------------------
    # 1. Soil Organic Carbon Evaluation
    # -----------------------------------------------------------------------
    @classmethod
    def calculate_soc_deficit(cls, soc: Optional[float], biome: Optional[str]) -> Dict[str, Any]:
        biome_key = (biome or "default").lower().replace(" ", "-")
        target = cls.SOC_TARGETS.get(biome_key, cls.SOC_TARGETS["default"])

        if soc is None:
            return {
                "soc_provided": False,
                "target_soc": target,
                "deficit_percent": None,
                "severity": "Unknown",
                "status": "unspecified",
                "awc_loss_pct": None,
                "microbial_activity_collapse": None
            }

        deficit_percent = round(max(0.0, (target - soc) / target * 100), 1)

        if soc < 0.35:
            severity = "Critical"
            status = "critically_depleted"
        elif soc < 0.60:
            severity = "Severe"
            status = "low"
        elif soc < target * 0.7:
            severity = "Moderate"
            status = "suboptimal"
        elif soc < target:
            severity = "Low"
            status = "moderate"
        else:
            severity = "Adequate"
            status = "adequate_to_high"

        awc_loss_pct = round(min(95.0, deficit_percent * 0.60), 1)
        microbial_collapse = soc < 0.45

        return {
            "soc_provided": True,
            "measured_soc": soc,
            "target_soc": target,
            "deficit_percent": deficit_percent,
            "severity": severity,
            "status": status,
            "awc_loss_pct": awc_loss_pct,
            "microbial_activity_collapse": microbial_collapse
        }

    # -----------------------------------------------------------------------
    # 2. Aridity & Moisture Evaluation
    # -----------------------------------------------------------------------
    @classmethod
    def calculate_aridity_index(
        cls,
        rainfall: Optional[float],
        pet: Optional[float],
        biome: Optional[str]
    ) -> Dict[str, Any]:
        biome_lower = (biome or "").lower()

        PET_DEFAULTS = {
            "semi-arid": 1200.0,
            "arid": 2000.0,
            "mediterranean": 900.0,
            "temperate-grassland": 700.0,
            "high-rainfall": 950.0,
            "tropical-rainforest": 1100.0,
            "urban": 900.0,
            "freshwater-wetland": 800.0,
            "default": 850.0
        }

        effective_pet = pet
        if effective_pet is None:
            for b, v in PET_DEFAULTS.items():
                if b in biome_lower:
                    effective_pet = v
                    break
            if effective_pet is None:
                effective_pet = PET_DEFAULTS["default"]

        if rainfall is None:
            return {
                "rainfall_provided": False,
                "annual_rainfall_mm": None,
                "pet_mm": effective_pet,
                "aridity_index": None,
                "classification": "Unrecorded precipitation",
                "deficit_status": "Unrecorded",
                "status": "unrecorded",
                "is_dryland": "arid" in biome_lower or "semi-arid" in biome_lower
            }

        ai = round(rainfall / effective_pet, 3)

        if ai < 0.05:
            classification = "Hyper-arid"
            deficit_status = "Extreme Aridity — Severe moisture limitation"
            status = "extreme_water_deficit"
        elif ai < 0.20:
            classification = "Arid"
            deficit_status = "Severe Aridity — Acute moisture constraint"
            status = "acute_water_stress"
        elif ai < 0.50:
            classification = "Semi-arid"
            deficit_status = "Significant Moisture Deficit"
            status = "water_limited"
        elif ai < 0.65:
            classification = "Dry Sub-humid"
            deficit_status = "Seasonal Moisture Stress"
            status = "seasonal_stress"
        elif ai < 1.00:
            classification = "Sub-humid"
            deficit_status = "Adequate Moisture"
            status = "adequate_moisture"
        elif ai < 1.50:
            classification = "Humid"
            deficit_status = "Plentiful Moisture / High Leaching Potential"
            status = "humid_leaching_risk"
        else:
            classification = "Hyper-humid / High Rainfall"
            deficit_status = "Excess Rainfall / Runoff & Leaching Vulnerability"
            status = "excess_runoff_leaching"

        return {
            "rainfall_provided": True,
            "annual_rainfall_mm": rainfall,
            "pet_mm": effective_pet,
            "aridity_index": ai,
            "classification": classification,
            "deficit_status": deficit_status,
            "status": status,
            "is_dryland": ai < 0.50
        }

    # -----------------------------------------------------------------------
    # 3. Biodiversity & Habitat Evaluation
    # -----------------------------------------------------------------------
    @classmethod
    def calculate_biodiversity_deficit(
        cls,
        land_use: Optional[str],
        ecosystem_type: str = "agricultural",
        biodiversity_status: Optional[str] = None
    ) -> Dict[str, Any]:
        lu = (land_use or "").lower()
        bio_stat = (biodiversity_status or "").lower()

        # Check explicit user biodiversity status first
        if bio_stat in ["low", "poor", "at_risk", "declining", "depleted"]:
            fbi = 0.25
            status = "Critical — Documented Biodiversity Decline"
            richness = "Low / Severely Depleted"
        elif bio_stat in ["moderate", "medium", "suboptimal"]:
            fbi = 0.55
            status = "Moderate — Biodiversity Under Stress"
            richness = "Moderate"
        elif bio_stat in ["high", "good", "rich", "intact"]:
            fbi = 0.85
            status = "High — Functional Biodiversity Intact"
            richness = "High"
        elif "monoculture" in lu or ("wheat" in lu and "intercrop" not in lu and "agroforestry" not in lu):
            fbi = 0.22
            status = "Critical — Monoculture Biological Homogenization"
            richness = "Very Low (<10 plant species/ha)"
        elif "fallow" in lu:
            fbi = 0.35
            status = "Low — Bare Fallow Lack of Refugia"
            richness = "Low (10-20 plant species/ha)"
        elif "urban lake" in lu or "urban park" in lu or ecosystem_type == "urban":
            fbi = 0.30
            status = "Suboptimal — Fragmented Urban Habitat Matrix"
            richness = "Low (Synanthropic taxa dominance)"
        elif "wetland" in lu or ecosystem_type == "wetland":
            fbi = 0.38
            status = "At Risk — Impaired Aquatic / Littoral Habitat"
            richness = "Depressed Aquatic Taxa"
        elif "forest" in lu or ecosystem_type == "forest":
            if "fragmented" in lu:
                fbi = 0.35
                status = "At Risk — Severe Canopy Fragmentation"
                richness = "Fragmented Interior Species"
            else:
                fbi = 0.65
                status = "Moderate to Good — Forest Canopy Matrix"
                richness = "Moderate to High"
        elif "intercrop" in lu or "pulse" in lu or "legume" in lu:
            fbi = 0.58
            status = "Moderate — Functional Cropping Diversity"
            richness = "Moderate (20-40 species/ha)"
        elif "agroforestry" in lu or "shelterbelt" in lu:
            fbi = 0.75
            status = "Good — Multi-Tier Structural Complexity"
            richness = "High (40+ species/ha)"
        else:
            fbi = 0.45
            status = "Sub-optimal Mixed Habitat"
            richness = "Moderate"

        return {
            "functional_biodiversity_index": fbi,
            "diversity_status": status,
            "species_richness_estimate": richness
        }

    # -----------------------------------------------------------------------
    # 4. Erosion & Runoff Susceptibility
    # -----------------------------------------------------------------------
    @classmethod
    def calculate_erosion_susceptibility(
        cls,
        soc: Optional[float],
        veg_cover: Optional[float],
        rainfall: Optional[float]
    ) -> Dict[str, Any]:
        score = 0
        factors = []

        if soc is not None and soc < 0.5:
            score += 3
            factors.append(f"Low SOC ({soc}%) — poor aggregate cementation")
        elif soc is not None and soc < 1.0:
            score += 1
            factors.append(f"Suboptimal SOC ({soc}%) — partial aggregate stability")

        if veg_cover is not None and veg_cover < 25:
            score += 3
            factors.append(f"Sparse vegetative cover ({veg_cover}%) — unprotected surface")
        elif veg_cover is not None and veg_cover < 50:
            score += 1
            factors.append(f"Moderate vegetative cover ({veg_cover}%)")

        if rainfall is not None:
            if rainfall < 350:
                score += 2
                factors.append("Low-rainfall dryland wind erosion risk during fallow")
            elif rainfall > 900:
                score += 3
                factors.append("High-rainfall convective runoff and rill erosion risk")

        if score >= 7:
            risk_level = "High to Severe"
        elif score >= 4:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        return {
            "erosion_risk_level": risk_level,
            "risk_score_numeric": score,
            "contributing_factors": factors
        }

    # -----------------------------------------------------------------------
    # 5. Full Environmental Profile Evaluation
    # -----------------------------------------------------------------------
    @classmethod
    def evaluate_profile(cls, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Builds the structured Environmental Profile, performs multi-ecosystem deficit
        and constraint analysis, identifies variable interactions, and outputs
        contextual steer terms and biophysical gates.
        """
        print(f"DEBUG: rule_engine.evaluate_profile starting with SOC={profile.get('soc_percent', 'None')}, Rainfall={profile.get('rainfall_mm', 'None')}")
        ecosystem_type = (profile.get("ecosystem_type") or "agricultural").lower()
        biome = profile.get("biome") or profile.get("region")
        soc = profile.get("soc_percent") or profile.get("soc")
        rainfall = profile.get("rainfall_mm") or profile.get("annual_rainfall")
        pet = profile.get("pet_mm")
        ph = profile.get("ph")
        land_use = (
            profile.get("current_crop")
            or profile.get("land_use_type")
            or profile.get("cropping_system")
            or profile.get("land_use")
        )
        veg_cover = profile.get("canopy_cover_pct") or profile.get("vegetation_cover_pct")
        bio_stat = profile.get("biodiversity_status")
        pollution = str(profile.get("pollution_level") or "").lower()
        water_qual = str(profile.get("water_quality") or "").lower()
        water_lvl = str(profile.get("water_level") or "").lower()
        frag_idx = str(profile.get("fragmentation_index") or "").lower()
        defor_rate = str(profile.get("deforestation_rate") or "").lower()
        gs_raw = profile.get("green_space_ratio")
        green_space_is_low = (
            (isinstance(gs_raw, (int, float)) and gs_raw <= 0.20)
            or (isinstance(gs_raw, str) and gs_raw.lower() in ["low", "poor", "minimal", "critical"])
        )

        # 1. Deficit calculations
        soc_eval = cls.calculate_soc_deficit(soc, biome)
        aridity_eval = cls.calculate_aridity_index(rainfall, pet, biome)
        bio_eval = cls.calculate_biodiversity_deficit(land_use, ecosystem_type, bio_stat)
        erosion_eval = cls.calculate_erosion_susceptibility(soc, veg_cover, rainfall)

        # 2. Build Internal Environmental Profile Dict
        environmental_profile = {
            "ecosystem_type": ecosystem_type,
            "soil_condition": {
                "organic_carbon": soc,
                "status": soc_eval["status"],
                "target": soc_eval["target_soc"],
                "ph": ph,
                "deficit_percent": soc_eval.get("deficit_percent")
            },
            "water_condition": {
                "rainfall_mm": aridity_eval["annual_rainfall_mm"],
                "aridity_index": aridity_eval["aridity_index"],
                "status": aridity_eval["status"],
                "water_quality": water_qual or ("clean" if not pollution else "polluted"),
                "water_level": water_lvl or "stable"
            },
            "land_condition": {
                "land_use": land_use or f"{ecosystem_type} system",
                "canopy_cover_pct": veg_cover,
                "fragmentation": frag_idx or ("low" if ecosystem_type != "forest" else "high"),
                "habitat_complexity": "low" if bio_eval["functional_biodiversity_index"] < 0.4 else "moderate"
            },
            "biodiversity_condition": {
                "status": "at_risk" if bio_eval["functional_biodiversity_index"] < 0.5 else "stable",
                "intactness_index": bio_eval["functional_biodiversity_index"],
                "species_richness": bio_eval["species_richness_estimate"]
            },
            "human_pressure": {
                "pollution_level": pollution or ("high" if water_qual in ["eutrophic", "poor"] else "low"),
                "deforestation": defor_rate or ("high" if ecosystem_type == "forest" and veg_cover and veg_cover < 30 else "low"),
                "green_space": "low" if green_space_is_low else "moderate"
            },
            "climate_condition": {
                "region": biome or "temperate",
                "classification": aridity_eval["classification"]
            }
        }

        # 3. Dynamic Identification of Limiting Factors and Variable Interactions
        identified_risks: List[Dict[str, Any]] = []
        limiting_factors: List[str] = []
        hypothesis_parts: List[str] = []
        steer_terms: List[str] = []
        causal_interactions: List[Dict[str, Any]] = []

        # ── SCENARIO A: URBAN ECOSYSTEM ──
        if ecosystem_type == "urban" or "urban" in (land_use or ""):
            if pollution == "high" or water_qual in ["poor", "polluted"]:
                limiting_factors.append("Severe urban runoff and stormwater pollutant load (heavy metals and suspended solids)")
                hypothesis_parts.append("urban runoff contamination entering surface waters")
                identified_risks.append({
                    "variable": "Urban Pollutant Contamination",
                    "severity": "Critical",
                    "metric": "Elevated TSS and Heavy Metal Toxicity",
                    "mechanism": "Untreated stormwater from impervious surfaces carries hydrocarbon and metal plumes into urban water bodies.",
                    "evidence_ref": "EPA-URBAN-STORMWATER-2021"
                })
            if green_space_is_low or bio_eval["functional_biodiversity_index"] < 0.45:
                limiting_factors.append("Urban habitat fragmentation and extreme green space deficit")
                hypothesis_parts.append("severe lack of structural canopy and green stepping stones")
                identified_risks.append({
                    "variable": "Urban Habitat Loss & Heat Island",
                    "severity": "High",
                    "metric": f"Functional Diversity = {bio_eval['functional_biodiversity_index']}",
                    "mechanism": "Impervious concrete surfaces eliminate avian nesting niches and amplify daytime urban heat island effects.",
                    "evidence_ref": "NATURE-SUSTAINABILITY-URBAN-2022"
                })

            steer_terms.extend([
                "urban runoff stormwater bioswales bio-retention filtration",
                "urban pocket forest miyawaki avian biodiversity stepping stones",
                "urban lake heavy metals suspended solids remediation",
                "urban heat island microclimate native trees"
            ])

            causal_interactions.append({
                "interaction": "Impervious Runoff + Heavy Metals -> Aquatic Toxicity -> Avian Foraging Collapse",
                "description": "Urban runoff carries unbuffered heavy metals and sediment into the lake, decimating benthic food webs and reducing diving waterfowl populations."
            })

        # ── SCENARIO B: WETLAND / LAKE BASIN ECOSYSTEM ──
        elif ecosystem_type == "wetland" or "wetland" in (land_use or "") or "lake" in (land_use or ""):
            if water_qual == "eutrophic" or pollution == "high":
                limiting_factors.append("Agricultural nutrient runoff causing severe eutrophication and algal blooms")
                hypothesis_parts.append("diffuse agricultural nutrient over-enrichment")
                identified_risks.append({
                    "variable": "Wetland Eutrophication & Cyanobacterial Blooms",
                    "severity": "Critical",
                    "metric": "Excess Nitrate & Phosphate Inflow",
                    "mechanism": "Unbuffered nutrient runoff fuels cyanobacterial blooms, depleting dissolved oxygen and triggering benthic hypoxia.",
                    "evidence_ref": "RAMSAR-WETLAND-RESTORATION-2021"
                })
            if water_lvl == "declining" or (rainfall is not None and rainfall < 450):
                limiting_factors.append("Hydrological drawdown and dry-season lakebed desiccation")
                hypothesis_parts.append("water level instability and benthic desiccation")
                identified_risks.append({
                    "variable": "Hydrological Drawdown",
                    "severity": "High",
                    "metric": "Declining Water Table & Littoral Drying",
                    "mechanism": "Premature drying of littoral breeding shallows aborts amphibian metamorphosis and waterfowl nesting.",
                    "evidence_ref": "RAMSAR-WETLAND-RESTORATION-2021"
                })

            steer_terms.extend([
                "wetland riparian buffer macrophyte nitrate phosphate biofiltration",
                "lake eutrophication algal bloom dissolved oxygen restoration",
                "wetland hydrological reconnection grade control rock sills",
                "waterfowl amphibian breeding littoral wetland habitat"
            ])

            causal_interactions.append({
                "interaction": "Excess Agricultural N/P + Lake Drawdown -> Eutrophic Bloom -> Hypoxia -> Aquatic Fauna Die-Off",
                "description": "Nutrient-rich runoff paired with declining water levels concentrates phosphorus and nitrogen, fueling toxic algae and suffocating aquatic fauna."
            })

        # ── SCENARIO C: FOREST / WOODLAND ECOSYSTEM ──
        elif (ecosystem_type == "forest" or ("forest" in (land_use or "") and "agroforestry" not in (land_use or ""))):
            if frag_idx in ["high", "severe", "present"] or (land_use and "fragmented" in land_use):
                limiting_factors.append("Severe forest canopy fragmentation and patch isolation distance")
                hypothesis_parts.append("canopy fragmentation and patch isolation")
                identified_risks.append({
                    "variable": "Forest Fragmentation & Edge Desiccation",
                    "severity": "Critical",
                    "metric": "Severe Matrix Disconnection",
                    "mechanism": "Small isolated patches suffer elevated desiccating edge microclimates and genetic isolation of interior taxa.",
                    "evidence_ref": "SCIENCE-FOREST-FRAGMENTATION-2020"
                })
            if defor_rate in ["high", "severe", "present"] or (veg_cover is not None and veg_cover < 35):
                limiting_factors.append("Anthropogenic canopy deforestation and arrested natural regeneration (recruitment bottlenecks & competitive invasive weed arrest)")
                hypothesis_parts.append("deforestation and invasive competitive smothering")
                identified_risks.append({
                    "variable": "Suppressed Natural Regeneration",
                    "severity": "High",
                    "metric": f"Canopy Cover = {veg_cover or 25}%",
                    "mechanism": "Aggressive invasive weeds and lianas smother native seedling banks, halting natural forest succession.",
                    "evidence_ref": "FAO-SOFO-FORESTS-2022"
                })

            steer_terms.extend([
                "forest connectivity corridors edge desiccation patch isolation",
                "assisted natural regeneration anr invasive liana suppression",
                "native forest canopy corridors interior bird mammal dispersal",
                "tropical forest restoration seedling recruitment"
            ])

            causal_interactions.append({
                "interaction": "Deforestation + Fragmentation -> Edge Microclimate Scorching -> Seedling Mortality -> Forest Degradation",
                "description": "Clearing trees breaks canopy continuity, exposing interior trees to desiccating winds, invasive grasses, and reproductive isolation."
            })

        # ── SCENARIO D: HIGH-RAINFALL / HUMID AGRICULTURAL OR AGROFORESTRY ──
        elif (rainfall is not None and rainfall > 900) or biome in ["high-rainfall", "humid-subtropical", "tropical-rainforest"]:
            if soc is not None and soc > 2.0:
                limiting_factors.append("High-rainfall nutrient leaching (nitrate and base cations) and slope runoff vulnerability")
                hypothesis_parts.append("high-rainfall convective leaching and topsoil runoff detachment")
                identified_risks.append({
                    "variable": "Nutrient Leaching & Runoff Vulnerability",
                    "severity": "Moderate to High",
                    "metric": f"Precipitation = {rainfall or 1250} mm/yr (AI = {aridity_eval['aridity_index']})",
                    "mechanism": "Heavy precipitation rapidly percolates soluble nutrients past shallow root zones and poses slope rill erosion risks.",
                    "evidence_ref": "ICRAF-TROPICAL-AGROFORESTRY-2021"
                })
            else:
                limiting_factors.append("Excess rainfall runoff erosion and subsoil leaching")
                hypothesis_parts.append("rain-induced nutrient leaching")

            if "monoculture" in (land_use or ""):
                limiting_factors.append("Lack of multi-tier canopy architecture to dissipate raindrop kinetic energy")
                hypothesis_parts.append("unbuffered monoculture canopy")

            steer_terms.extend([
                "multi strata shaded agroforestry tropical nutrient leaching",
                "contour vetiver hedgerows slope runoff sediment control",
                "high rainfall soil organic carbon agroforestry polyculture",
                "agroforestry canopy bird pollinator biodiversity"
            ])

            causal_interactions.append({
                "interaction": "High Rainfall + Shallow Roots -> Downward Nutrient Leaching -> Topsoil Acidification",
                "description": "Convective rainfall leaches soluble cations and nitrates below crop roots; multi-strata perennial trees cycle nutrients back up."
            })
        # ── SCENARIO E: CROPLAND / GENERAL AGRICULTURAL ──
        else:
            if soc is not None and soc_eval.get("deficit_percent") and soc_eval["deficit_percent"] > 40:
                limiting_factors.append(f"Topsoil organic carbon deficit ({soc}% SOC vs {soc_eval['target_soc']}% benchmark)")
                hypothesis_parts.append("soil carbon depletion")
                identified_risks.append({
                    "variable": "Soil Organic Carbon",
                    "severity": soc_eval["severity"],
                    "metric": f"{soc}% SOC vs {soc_eval['target_soc']}% baseline ({soc_eval['deficit_percent']}% deficit)",
                    "mechanism": "Carbon depletion reduces microbial activity and degrades soil aggregate stability.",
                    "evidence_ref": "IPCC-SRCCL-2019-CH04"
                })

            if rainfall is not None and rainfall < 400:
                limiting_factors.append(f"Water limitation under low precipitation ({rainfall} mm/yr)")
                hypothesis_parts.append("hydrological moisture limitation")
                identified_risks.append({
                    "variable": "Precipitation Deficit",
                    "severity": "High",
                    "metric": f"{rainfall} mm/yr precipitation",
                    "mechanism": "Atmospheric evaporative demand outpaces seasonal precipitation, driving soil moisture deficit.",
                    "evidence_ref": "FAO-SOLAW-2021"
                })

            if land_use and ("monoculture" in land_use.lower() or "wheat" in land_use.lower()):
                limiting_factors.append("Continuous single-crop cultivation causing biodiversity and pest suppression deficit")
                hypothesis_parts.append("cropping homogenization")
                identified_risks.append({
                    "variable": "Cropping Homogenization",
                    "severity": "Moderate",
                    "metric": f"Land use: {land_use}",
                    "mechanism": "Continuous cultivation without rotation narrows biological activity and increases pest risks.",
                    "evidence_ref": "IPBES-LADA-2018"
                })

            steer_terms.extend([
                "cover crops soil organic carbon living roots",
                "field margins floral hedgerows biodiversity",
                "crop rotation diversification pulses",
                "residue retention stubble mulch moisture",
                "agroforestry boundary trees microclimate",
                "reduced tillage conservation agriculture"
            ])

        # Build diagnostic hypothesis
        if hypothesis_parts:
            diagnostic_hypothesis = "Systemic degradation driven by " + ", and ".join(hypothesis_parts) + "."
        else:
            diagnostic_hypothesis = "Awaiting site-specific field telemetry across environmental dimensions."

        # 4. Curated 6-item intervention library mapping
        viable_interventions: List[str] = [
            "cover_crops",
            "field_margins",
            "crop_rotation",
            "residue_retention",
            "agroforestry",
            "reduced_tillage"
        ]
        prohibited_interventions: List[str] = [
            "deep_inversion_plowing",
            "unbuffered_monoculture_expansion"
        ]
        if rainfall is not None and rainfall < 350:
            prohibited_interventions.append("water_intensive_cover_crops")

        # 5. Risk Ratings
        risk_ratings = {
            "primary_stressor_risk": "Critical" if identified_risks and identified_risks[0]["severity"] == "Critical" else "High",
            "biodiversity_risk": "Critical" if bio_eval["functional_biodiversity_index"] < 0.35 else "Moderate",
            "hydrological_risk": (
                "Critical" if (aridity_eval["is_dryland"] or water_qual == "eutrophic" or pollution == "high") else "Moderate"
            ),
            "soil_or_habitat_degradation": (
                "High" if (soc_eval.get("severity") in ["Critical", "Severe"] or ecosystem_type in ["urban", "wetland", "forest"]) else "Low"
            )
        }

        # 6. System Health Index (0 - 100) — only compute if field telemetry is provided
        has_telemetry = (soc is not None) or (rainfall is not None) or (land_use is not None and land_use.strip() != "")
        if not has_telemetry and not identified_risks:
            health_index = None
        elif ecosystem_type == "urban":
            base_h = 30.0 if pollution == "high" else 55.0
            if green_space_is_low:
                base_h -= 10.0
            health_index = max(15.0, min(85.0, base_h))
        elif ecosystem_type == "wetland":
            base_h = 25.0 if water_qual == "eutrophic" else 50.0
            if water_lvl == "declining":
                base_h -= 10.0
            health_index = max(15.0, min(85.0, base_h))
        elif ecosystem_type == "forest":
            cov = veg_cover or 25.0
            health_index = round(max(15.0, min(85.0, (cov / 100.0) * 50.0 + (0.2 if frag_idx == "high" else 0.5) * 50.0)), 1)
        else:
            # Agriculture
            soc_score = (1.0 - (soc_eval["deficit_percent"] or 30.0) / 100.0) * 0.45
            bio_score = bio_eval["functional_biodiversity_index"] * 0.35
            rain_score = (0.5 if aridity_eval["is_dryland"] else 0.8) * 0.20
            health_index = round(max(15.0, min(90.0, (soc_score + bio_score + rain_score) * 100.0)), 1)

        return {
            "environmental_profile": environmental_profile,
            "ecosystem_type": ecosystem_type,
            "soc_metrics": soc_eval,
            "aridity_metrics": aridity_eval,
            "biodiversity_metrics": bio_eval,
            "erosion_metrics": erosion_eval,
            "identified_risks": identified_risks,
            "primary_limiting_factors": limiting_factors,
            "causal_interactions": causal_interactions,
            "diagnostic_hypothesis": diagnostic_hypothesis,
            "risk_ratings": risk_ratings,
            "query_steer_terms": steer_terms,
            "viable_intervention_classes": viable_interventions,
            "prohibited_intervention_classes": prohibited_interventions,
            "system_health_index": health_index
        }
