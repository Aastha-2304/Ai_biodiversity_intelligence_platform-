"""
Completeness & Domain-Probe Check — Stage 2
Darukaa.Earth AI Biodiversity Intelligence Platform

Evaluates environmental field completeness across multiple ecosystems:
- Agricultural, Urban, Wetland, Forest, and Grassland domains.
- Hard requirement: Must establish at least 3 environmental variables before generating recommendations.
- Context-aware clarifying questions: NEVER asks an urban or wetland user for agricultural soil carbon.
- Proactive domain-probing when critical site factors alter scientific diagnosis.
"""

from typing import Any, Dict, List, Optional


class CompletenessChecker:
    """Evaluates field completeness, enforces the 3-variable gate, and generates precision clarifying questions."""

    ECOSYSTEM_FIELDS = {
        "urban": [
            {"field": "pollution_level", "label": "Pollution & Urban Runoff", "impact_rank": 1, "weight": 0.25},
            {"field": "green_space_ratio", "label": "Surrounding Green Space / Canopy", "impact_rank": 2, "weight": 0.25},
            {"field": "water_quality", "label": "Water Quality & Aquatic Health", "impact_rank": 3, "weight": 0.20},
            {"field": "water_level", "label": "Water Level Fluctuations", "impact_rank": 4, "weight": 0.15},
            {"field": "species_richness", "label": "Observed Avian / Wildlife Status", "impact_rank": 5, "weight": 0.15}
        ],
        "wetland": [
            {"field": "water_quality", "label": "Water Quality / Eutrophication", "impact_rank": 1, "weight": 0.25},
            {"field": "water_level", "label": "Water Depth & Hydroperiod Stability", "impact_rank": 2, "weight": 0.25},
            {"field": "pollution_level", "label": "Agricultural / Urban Inflow Runoff", "impact_rank": 3, "weight": 0.20},
            {"field": "canopy_cover_pct", "label": "Riparian Buffer & Reed Cover", "impact_rank": 4, "weight": 0.15},
            {"field": "rainfall_mm", "label": "Precipitation Regime", "impact_rank": 5, "weight": 0.15}
        ],
        "forest": [
            {"field": "canopy_cover_pct", "label": "Canopy Cover (%)", "impact_rank": 1, "weight": 0.25},
            {"field": "fragmentation_index", "label": "Habitat Fragmentation & Patch Isolation", "impact_rank": 2, "weight": 0.25},
            {"field": "deforestation_rate", "label": "Deforestation & Clearing Pressure", "impact_rank": 3, "weight": 0.20},
            {"field": "biodiversity_status", "label": "Biodiversity & Interior Species Status", "impact_rank": 4, "weight": 0.15},
            {"field": "rainfall_mm", "label": "Annual Rainfall", "impact_rank": 5, "weight": 0.15}
        ],
        "agricultural": [
            {"field": "soc_percent", "label": "Soil Organic Carbon (SOC %)", "impact_rank": 1, "weight": 0.20},
            {"field": "rainfall_mm", "label": "Annual Rainfall (mm)", "impact_rank": 2, "weight": 0.20},
            {"field": "biome", "label": "Eco-Region / Biome", "impact_rank": 3, "weight": 0.15},
            {"field": "current_crop", "label": "Cropping System / Land Use", "impact_rank": 4, "weight": 0.15},
            {"field": "irrigation_status", "label": "Water Regime / Irrigation", "impact_rank": 5, "weight": 0.10},
            {"field": "soil_texture", "label": "Topsoil Texture", "impact_rank": 6, "weight": 0.08},
            {"field": "ph", "label": "Soil pH", "impact_rank": 7, "weight": 0.06},
            {"field": "tillage_practice", "label": "Tillage Practice", "impact_rank": 8, "weight": 0.06},
            {"field": "soil_compaction", "label": "Soil Compaction", "impact_rank": 9, "weight": 0.06},
            {"field": "soil_erosion_rate", "label": "Soil Erosion & Runoff", "impact_rank": 10, "weight": 0.06}
        ]
    }

    ALL_ECOLOGICAL_METRICS = [
        "soc_percent", "rainfall_mm", "rainfall_pattern", "biome", "current_crop",
        "land_use_type", "irrigation_status", "soil_texture", "ph", "tillage_practice",
        "soil_compaction", "water_runoff", "water_infiltration", "soil_erosion_rate",
        "pollution_level", "water_quality", "water_level", "green_space_ratio",
        "canopy_cover_pct", "fragmentation_index", "deforestation_rate",
        "biodiversity_status", "species_richness", "latitude", "longitude"
    ]

    @classmethod
    def evaluate_completeness(
        cls,
        profile: Dict[str, Any],
        detected_ambiguities: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        eco_type = (profile.get("ecosystem_type") or "agricultural").lower()
        if eco_type not in cls.ECOSYSTEM_FIELDS:
            eco_type = "agricultural"

        core_specs = cls.ECOSYSTEM_FIELDS[eco_type]

        present_core = []
        missing_core = []
        total_weight_present = 0.0

        for spec in core_specs:
            val = profile.get(spec["field"])
            if val is not None and val != "":
                present_core.append(spec)
                total_weight_present += spec["weight"]
            else:
                missing_core.append(spec)

        # Count all established valid environmental metrics across the profile
        established_metrics = []
        for m in cls.ALL_ECOLOGICAL_METRICS:
            val = profile.get(m)
            if val is not None and val != "":
                established_metrics.append(m)

        established_count = len(established_metrics)
        completeness_score = round(min(1.0, total_weight_present + (established_count - len(present_core)) * 0.1), 2)
        ratio_str = f"{established_count} environmental parameters established ({eco_type.title()} domain)"

        # Domain Probing Logic
        domain_probes: List[str] = []
        crop = str(profile.get("current_crop") or "").lower()
        biome = str(profile.get("biome") or "").lower()
        rain = profile.get("rainfall_mm")
        soc = profile.get("soc_percent")
        irr = profile.get("irrigation_status")
        till = profile.get("tillage_practice")
        tex = profile.get("soil_texture")

        if ("wheat" in crop or "monoculture" in crop or "cereal" in crop) and not irr:
            domain_probes.append(
                "Monoculture cropping detected without water regime specified: "
                "Is this dryland/rainfed or does it utilize supplementary irrigation?"
            )

        if soc is not None and float(soc) < 0.8 and not till:
            domain_probes.append(
                f"Severe topsoil carbon deficit observed ({soc}% SOC): "
                "Is the land under conventional deep inversion tillage or conservation zero-till?"
            )

        # Hard requirement check: Must establish at least 2 domain-specific core variables
        # plus contextual baseline (minimum 3 established variables overall)
        domain_core_count = len(present_core)
        is_actionable = established_count >= 3 and domain_core_count >= 2
        requires_clarification = not is_actionable
        is_preliminary = established_count < 4

        # Generate prioritized clarifying questions
        clarifying_questions: List[Dict[str, Any]] = []

        if requires_clarification:
            bio_status = profile.get("biodiversity_status")
            compaction_or_soil = any(k in str(detected_ambiguities).lower() for k in ["compact", "bulk density", "soil is weak"]) or profile.get("soil_compaction")
            erosion_reported = profile.get("soil_erosion_rate") or any("erosion" in str(a).lower() for a in (detected_ambiguities or []))

            if bio_status == "declining" or any("biodiversity" in str(a).lower() for a in (detected_ambiguities or [])):
                bio_q = {
                    "missing_parameter": "biodiversity_context",
                    "missing_parameters": ["location", "current_crop", "observed_symptoms", "management_practices"],
                    "question_text": "To identify appropriate restoration practices for your declining biodiversity, could you specify your location/biome, current cropping system, observed symptoms (e.g. loss of wild pollinators or natural predators), and existing field management practices?",
                    "scientific_rationale": "Ecological restoration pathways depend on landscape context, cropping regime, and functional ecological groups experiencing decline.",
                    "suggested_inputs": [
                        "Semi-arid cereal farm, noticeable decline in native pollinators, conventional tillage",
                        "Temperate mixed farming, loss of insectivorous birds and pest predators, annual monocropping",
                        "Sub-humid pasture/crop matrix, depleted soil biological activity, lack of non-crop vegetation"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Provide field details"
                }
                clarifying_questions.append(bio_q)
            elif compaction_or_soil:
                comp_q = {
                    "missing_parameter": "compaction_context",
                    "missing_parameters": ["soil_texture", "tillage_practice", "machinery_depth"],
                    "question_text": "Could you provide your soil texture (e.g. clay, loam, sandy), current tillage practice, and observed compaction depth or surface ponding?",
                    "scientific_rationale": "Mitigating soil compaction requires determining whether crusting is surface-level (requiring residue retention or cover crops) or subsoil plow-pan (requiring deep non-inversion aeration).",
                    "suggested_inputs": [
                        "Silty clay loam, intensive deep plowing, slow water infiltration after rains",
                        "Sandy loam, conventional disc harrowing, surface crusting preventing seedling emergence",
                        "Clay soil, continuous wheel traffic, severe subsoil compaction"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Provide soil details"
                }
                clarifying_questions.append(comp_q)
            elif erosion_reported:
                eros_q = {
                    "missing_parameter": "erosion_context",
                    "missing_parameters": ["slope_degrees", "rainfall_intensity", "ground_cover"],
                    "question_text": "Could you share your field slope, whether erosion is caused by water or wind, and your current ground cover between seasons?",
                    "scientific_rationale": "Erosion control mechanisms differ fundamentally between kinetic water runoff (requiring contour barriers and vegetative cover) and wind saltation (requiring shelterbelts and residue cover).",
                    "suggested_inputs": [
                        "Moderate slope (3-6%), heavy rainfall runoff rills, bare soil between crops",
                        "Flat plains, severe dry-season wind erosion, post-harvest residue removed",
                        "Undulating terrain, topsoil wash during monsoon downpours"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Provide erosion details"
                }
                clarifying_questions.append(eros_q)
            elif eco_type == "urban":
                urban_q = {
                    "missing_parameter": "urban_context",
                    "missing_parameters": ["water_quality", "pollution_level", "green_space_ratio"],
                    "question_text": "Could you provide details on the water quality/pollution level, surrounding green space cover, and water level changes?",
                    "scientific_rationale": "Urban ecological interventions require baseline data on runoff volumes, contaminants, and existing canopy cover.",
                    "suggested_inputs": [
                        "High urban runoff pollution, low surrounding green space, seasonal drawdown",
                        "Moderate stormwater pollution, 15% park shoreline canopy, stable water level"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Type field values"
                }
                clarifying_questions.append(urban_q)
            elif eco_type == "wetland":
                wetland_q = {
                    "missing_parameter": "wetland_context",
                    "missing_parameters": ["water_quality", "water_level", "pollution_level"],
                    "question_text": "Could you provide details on incoming water quality, water depth stability, and surrounding land-use buffer?",
                    "scientific_rationale": "Wetland interventions depend on nutrient inflows and hydrological hydroperiod stability.",
                    "suggested_inputs": [
                        "Eutrophic algal blooms, agricultural runoff, dry-season drawdown",
                        "Moderate nutrient loading, partial intact reed beds"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Type field values"
                }
                clarifying_questions.append(wetland_q)
            elif eco_type == "forest":
                forest_q = {
                    "missing_parameter": "forest_context",
                    "missing_parameters": ["canopy_cover_pct", "fragmentation_index"],
                    "question_text": "Could you provide estimated canopy cover (%), patch isolation distance, and disturbances?",
                    "scientific_rationale": "Forest biodiversity recovery depends on structural canopy continuity and edge microclimate buffering.",
                    "suggested_inputs": [
                        "Canopy cover 25%, severe patch isolation, high disturbance",
                        "Canopy cover 45%, moderate fragmentation across farmland"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Type field values"
                }
                clarifying_questions.append(forest_q)
            else:
                ag_q = {
                    "missing_parameter": "agricultural_context",
                    "missing_parameters": ["location", "current_crop", "soil_type", "management_practices"],
                    "question_text": "Could you provide your location/biome, current cropping system, and observed soil or vegetation conditions?",
                    "scientific_rationale": "Responsible ecological recommendations require knowing the baseline agroecosystem and climate context.",
                    "suggested_inputs": [
                        "Semi-arid grain farm, low organic matter, continuous cereal cropping",
                        "Temperate mixed farm, moderate rainfall, rotating cereals and oilseeds",
                        "Sub-humid cropland, seasonal moisture stress, conventional tillage"
                    ],
                    "allow_custom_input": True,
                    "custom_option_label": "Type field values"
                }
                clarifying_questions.append(ag_q)

        primary_q = clarifying_questions[0] if clarifying_questions else None

        preliminary_note = ""
        if requires_clarification:
            preliminary_note = (
                f"Preliminary diagnostic assessment: Established {established_count} variable(s) for this {eco_type.title()} system. "
                "Per ecological scientific rigor constraints, minimum 3 environmental variables are required "
                "to synthesize definitive peer-reviewed recommendations. Please provide the key parameters below."
            )

        return {
            "completeness_score": completeness_score,
            "completeness_ratio": ratio_str,
            "established_count": established_count,
            "present_fields": established_metrics,
            "missing_fields": [m["label"] for m in missing_core],
            "clarifying_questions": clarifying_questions,
            "primary_question": primary_q,
            "domain_probes": domain_probes,
            "is_actionable": is_actionable,
            "requires_clarification": requires_clarification,
            "is_preliminary": is_preliminary,
            "preliminary_note": preliminary_note,
            "ambiguity_translations": detected_ambiguities or []
        }
