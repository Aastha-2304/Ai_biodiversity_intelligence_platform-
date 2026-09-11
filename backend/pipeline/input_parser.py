"""
Input Parser — Stage 0
Darukaa.Earth AI Biodiversity Intelligence Platform

Parses free-text, structured JSON, and geographic coordinates into a normalized
environmental profile dictionary spanning all 8 environmental dimensions with
ambiguity detection, multi-ecosystem awareness, and spatial coordinate extraction.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple


class InputParser:
    """Parses text, JSON, and geo-coordinates into a normalized environmental profile."""

    AMBIGUOUS_MAP = {
        "soil is weak": [
            "Soil Organic Carbon (SOC %)",
            "Soil pH (acidity / alkalinity)",
            "Bulk Density (g/cm³)",
            "Available Water Capacity (mm/m)"
        ],
        "biodiversity is declining": [
            "Functional Biodiversity Intactness Index (BII)",
            "Species Richness Count (taxa / ha)",
            "Pollinator Visitation Frequency",
            "Landscape Patch Fragmentation Index"
        ],
        "biodiversity is bad": [
            "Functional Biodiversity Intactness Index (BII)",
            "Species Richness Count (taxa / ha)",
            "Natural Predator Arthropod Density",
            "Floral Forage Continuity"
        ],
        "land is degraded": [
            "Soil Organic Carbon (SOC %)",
            "Canopy & Residue Cover (%)",
            "Topsoil Erosion Rate (t/ha/yr)",
            "Soil Bulk Density & Compaction"
        ],
        "poor soil": [
            "Soil Organic Carbon (SOC %)",
            "Soil pH & Nutrient Bioavailability",
            "Active Microbial Biomass Carbon (mg C/kg)"
        ],
        "declining wildlife": [
            "Biodiversity Intactness Index (BII)",
            "Habitat Fragmentation & Corridor Distance",
            "Wild Pollinator & Predator Richness"
        ],
        "water is low": [
            "Annual Precipitation (mm)",
            "Soil Moisture Volumetric %",
            "Groundwater Table Depth (m)",
            "Standardized Precipitation Index (SPI)"
        ],
        "water is polluted": [
            "Dissolved Oxygen (mg/L)",
            "Total Suspended Solids (mg/L)",
            "Nitrate & Phosphate Concentration",
            "Heavy Metal Contamination Index"
        ],
        "forest is degraded": [
            "Canopy Cover Percentage (%)",
            "Deforestation Rate (ha/yr)",
            "Patch Isolation Distance (m)",
            "Invasive Liana Infestation Level"
        ]
    }

    @classmethod
    def parse_input(
        cls,
        text: Optional[str] = None,
        structured_dict: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], str, List[Dict[str, Any]]]:
        """
        Returns:
            (extracted_profile_dict, detected_mode, detected_ambiguities)
        """
        extracted: Dict[str, Any] = {}
        detected_mode = "free_text"
        detected_ambiguities: List[Dict[str, Any]] = []

        # 1. Auto-detect if incoming text is raw JSON payload
        stripped_text = (text or "").strip()
        if stripped_text.startswith("{") and stripped_text.endswith("}"):
            try:
                parsed_json = json.loads(stripped_text)
                if isinstance(parsed_json, dict):
                    structured_dict = {**(structured_dict or {}), **parsed_json}
                    detected_mode = "json"
            except Exception:
                pass

        if structured_dict and text and detected_mode != "json":
            detected_mode = "hybrid"
        elif structured_dict and not text:
            detected_mode = "json"

        # 2. Ingest structured dictionary
        if structured_dict:
            for k, v in structured_dict.items():
                norm_key = k.lower().strip().replace(" ", "_").replace("-", "_")

                # Ecosystem type
                if norm_key in ["ecosystem", "ecosystem_type", "ecosystem_category"]:
                    extracted["ecosystem_type"] = str(v).strip().lower()

                # Soil parameters
                elif norm_key in ["soc", "soc_pct", "soc_percent", "soil_organic_carbon", "organic_carbon"]:
                    extracted["soc_percent"] = cls._to_float(v)
                    extracted["soc_source"] = "json_input"
                elif norm_key in ["ph", "soil_ph"]:
                    extracted["ph"] = cls._to_float(v)
                    extracted["ph_source"] = "json_input"
                elif norm_key in ["texture", "soil_texture"]:
                    extracted["soil_texture"] = str(v).strip().lower()
                elif norm_key in ["soil_moisture", "moisture", "soil_moisture_pct"]:
                    extracted["soil_moisture_pct"] = cls._to_float(v)
                elif norm_key in ["microbial_biomass", "smbc", "soil_microbial_biomass"]:
                    extracted["soil_microbial_biomass"] = cls._to_float(v)
                elif norm_key in ["erosion_rate", "soil_erosion_rate", "soil_loss"]:
                    extracted["soil_erosion_rate"] = cls._to_float(v)

                # Climate & Weather
                elif norm_key in ["rainfall", "annual_rainfall", "precipitation", "precip_mm", "rainfall_mm"]:
                    extracted["rainfall_mm"] = cls._to_float(v)
                    extracted["rainfall_source"] = "json_input"
                elif norm_key in ["rainfall_pattern", "rain_pattern"]:
                    extracted["rainfall_pattern"] = str(v).strip().lower()
                elif norm_key in ["biome", "ecoregion", "region", "climate_zone"]:
                    extracted["biome"] = str(v).lower().strip().replace(" ", "-")
                elif norm_key in ["pet", "pet_mm", "evapotranspiration"]:
                    extracted["pet_mm"] = cls._to_float(v)
                elif norm_key in ["drought_index", "spi", "drought_index_spi"]:
                    extracted["drought_index_spi"] = cls._to_float(v)
                elif norm_key in ["temperature", "temp_range", "temperature_range"]:
                    extracted["temperature_range"] = str(v).strip()

                # Land Use / Cover
                elif norm_key in ["crop", "current_crop", "cropping_system", "land_use", "land_use_type"]:
                    extracted["current_crop"] = str(v).strip()
                    extracted["land_use_type"] = str(v).strip()
                elif norm_key in ["tillage", "tillage_practice"]:
                    extracted["tillage_practice"] = str(v).strip().lower()
                elif norm_key in ["fragmentation", "fragmentation_index", "habitat_fragmentation"]:
                    extracted["fragmentation_index"] = cls._to_float(v) if isinstance(v, (int, float)) else str(v).strip()
                elif norm_key in ["deforestation", "deforestation_rate", "afforestation_rate"]:
                    extracted["deforestation_rate"] = cls._to_float(v) if isinstance(v, (int, float)) else str(v).strip()
                elif norm_key in ["green_space", "urban_green_space", "green_space_ratio"]:
                    extracted["green_space_ratio"] = cls._to_float(v) if isinstance(v, (int, float)) else str(v).strip()

                # Vegetation & Canopy
                elif norm_key in ["veg_cover", "vegetation_cover", "canopy_cover", "canopy_cover_pct"]:
                    extracted["canopy_cover_pct"] = cls._to_float(v)
                elif norm_key in ["ndvi", "satellite_ndvi"]:
                    extracted["ndvi"] = cls._to_float(v)
                elif norm_key in ["carbon_stock", "carbon_sequestration_rate"]:
                    extracted["carbon_stock_tha"] = cls._to_float(v)

                # Water & Wetland parameters
                elif norm_key in ["water_quality", "water_condition"]:
                    extracted["water_quality"] = str(v).strip().lower()
                elif norm_key in ["water_level", "water_depth", "lake_level"]:
                    extracted["water_level"] = str(v).strip().lower()
                elif norm_key in ["pollution", "pollution_level", "pollutant"]:
                    extracted["pollution_level"] = str(v).strip().lower()
                elif norm_key in ["irrigation", "irrigation_status", "water_source"]:
                    extracted["irrigation_status"] = str(v).strip().lower()
                elif norm_key in ["water_table", "water_table_depth", "water_table_depth_m"]:
                    extracted["water_table_depth_m"] = cls._to_float(v)
                elif norm_key in ["water_stress", "water_stress_index"]:
                    extracted["water_stress_index"] = cls._to_float(v)

                # Biodiversity
                elif norm_key in ["biodiversity", "biodiversity_status", "species_diversity"]:
                    extracted["biodiversity_status"] = str(v).strip().lower()
                elif norm_key in ["species_richness", "bird_diversity", "pollinator_diversity"]:
                    extracted["species_richness"] = str(v).strip().lower()

                # Topographic & Spatial
                elif norm_key in ["lat", "latitude"]:
                    extracted["latitude"] = cls._to_float(v)
                elif norm_key in ["lon", "long", "longitude"]:
                    extracted["longitude"] = cls._to_float(v)
                elif norm_key in ["elevation", "elevation_m", "altitude"]:
                    extracted["elevation_m"] = cls._to_float(v)

                # Anthropogenic & Urban
                elif norm_key in ["aqi", "air_quality_index"]:
                    extracted["aqi"] = cls._to_float(v)
                elif norm_key in ["pm25", "pm2_5", "pm25_ugm3"]:
                    extracted["pm25_ugm3"] = cls._to_float(v)
                elif norm_key in ["population_density"]:
                    extracted["population_density"] = cls._to_float(v)

        # 3. Extract from freeform text
        if stripped_text:
            text_lower = stripped_text.lower()
            clean_nopunct = re.sub(r'[^\w\s]', '', text_lower).strip()

            # Detect Greeting & Off-Topic queries
            if clean_nopunct in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]:
                extracted["_query_intent"] = "greeting"
            elif any(clean_nopunct.startswith(x) for x in ["what is the capital", "who is the president", "tell me a joke", "write code", "who wrote", "what is 2+2"]):
                extracted["_query_intent"] = "off_topic"
            else:
                eco_keywords = [
                    "soil", "biodiversity", "erosion", "crop", "carbon", "soc", "rain", "rainfall", "water",
                    "drought", "moisture", "tillage", "till", "cover", "species", "forest", "tree", "plant",
                    "organic", "farm", "agriculture", "land", "ecosystem", "nutrient", "hedgerow", "buffer",
                    "agroforestry", "pasture", "grassland", "wetland", "urban", "canopy", "yield", "compaction",
                    "compacted", "ph", "fertilizer", "weeds", "field", "biomass", "pollinator", "pest", "decline",
                    "declining", "degraded", "salinity", "saline", "nitrogen", "phosphorus",
                    "intervention", "interventions", "recommend", "recommendation", "recommendations",
                    "practice", "practices", "what should i do", "what to do", "what do you recommend",
                    "why would this", "why does this", "how to fix", "advice", "manage", "management",
                    "runoff", "running off", "dying", "loss", "restore", "restoration", "acre", "hectare", "field"
                ]
                has_eco = any(kw in text_lower for kw in eco_keywords)
                if not has_eco and not structured_dict:
                    # If question is a short conversational advisory follow-up, keep as ecological
                    if any(phrase in clean_nopunct for phrase in ["what should i do", "what do i do", "what to do", "how to proceed", "what next", "what intervention", "what do you recommend", "how to fix"]):
                        extracted["_query_intent"] = "ecological"
                    else:
                        extracted["_query_intent"] = "off_topic"
                else:
                    extracted["_query_intent"] = "ecological"

            # Ambiguity check
            for phrase, candidates in cls.AMBIGUOUS_MAP.items():
                if phrase in text_lower:
                    detected_ambiguities.append({
                        "phrase": phrase,
                        "candidate_measurable_metrics": candidates,
                        "suggested_question": f"When you say '{phrase}', which measurable ecological metric are you observing?"
                    })

            # Ecosystem type classification
            if any(term in text_lower for term in ["urban lake", "urban park", "urban ecosystem", "city park", "urban green", "green space", "city", "built environment", "urban"]):
                extracted["ecosystem_type"] = "urban"
            elif any(term in text_lower for term in ["wetland", "lake basin", "lake", "riparian", "marsh", "swamp", "pond", "water body", "eutrophication", "water level"]):
                extracted["ecosystem_type"] = "wetland"
            elif "agroforestry" in text_lower:
                extracted["ecosystem_type"] = "agricultural"
            elif any(term in text_lower for term in ["woodland", "rainforest", "deforestation", "fragmented forest", "timber", "liana"]) or (re.search(r'\bforest\b', text_lower)):
                extracted["ecosystem_type"] = "forest"
            elif any(term in text_lower for term in ["grassland", "pasture", "savanna", "rangeland", "prairie", "silvopasture"]):
                extracted["ecosystem_type"] = "grassland"
            elif any(term in text_lower for term in ["crop", "cropland", "farm", "wheat", "maize", "cereal", "agriculture", "monoculture", "tillage", "intercrop", "agroforestry", "fallow"]):
                extracted["ecosystem_type"] = "agricultural"

            # Biodiversity status extraction (including "biodiversity loss")
            if (
                "declining biodiversity" in text_lower
                or "biodiversity decline" in text_lower
                or "biodiversity is declining" in text_lower
                or "biodiversity loss" in text_lower
                or "loss of biodiversity" in text_lower
                or "loss of species" in text_lower
            ):
                extracted["biodiversity_status"] = "declining"
            elif "bird diversity" in text_lower and ("decreased" in text_lower or "declined" in text_lower or "drop" in text_lower):
                extracted["biodiversity_status"] = "declining"
                extracted["species_richness"] = "declining_birds"
            else:
                bio_match = re.search(r'biodiversity\s+(?:is|status|level|observed)\s+([a-z_-]+)', text_lower)
                if bio_match and bio_match.group(1).strip() not in ["a", "the", "in", "on", "at", "of", "is"]:
                    extracted["biodiversity_status"] = bio_match.group(1).strip()

            # Water quality / Pollution / Eutrophication
            if re.search(r'(?:high\s+(?:agricultural\s+|urban\s+|runoff\s+)?pollution|pollution[\s:=]+high|heavily\s+polluted|heavy\s+stormwater|high\s+particulate)', text_lower):
                extracted["pollution_level"] = "high"
            elif "moderate pollution" in text_lower or "pollution: moderate" in text_lower:
                extracted["pollution_level"] = "moderate"
            elif "low pollution" in text_lower or "pollution: low" in text_lower:
                extracted["pollution_level"] = "low"

            if "eutrophic" in text_lower or "algal bloom" in text_lower or "hypoxic" in text_lower:
                extracted["water_quality"] = "eutrophic"
            elif "dissolved oxygen 2" in text_lower or "dissolved oxygen 1" in text_lower or "water quality: poor" in text_lower or "poor water quality" in text_lower or "polluted water" in text_lower:
                extracted["water_quality"] = "poor"

            if any(w in text_lower for w in ["low water level", "declining water level", "water level: declining", "water level has decreased", "water drawdown", "hydrological disruption", "fluctuating erratically"]):
                extracted["water_level"] = "declining"

            # Fragmentation & Deforestation
            if "fragmentation" in text_lower or "fragmented" in text_lower:
                extracted["fragmentation_index"] = "high" if any(w in text_lower for w in ["high", "severe", "critical"]) else "present"
            if "deforestation" in text_lower:
                extracted["deforestation_rate"] = "high" if any(w in text_lower for w in ["high", "severe", "rapid"]) else "present"

            # Green space & Canopy
            gs_match = re.search(r'([0-9.]+)\s*%\s*(?:green\s*space|park)', text_lower)
            if not gs_match:
                gs_match = re.search(r'(?:green\s*space|park\s*cover)[^\d\n]{0,15}?([0-9.]+)\s*%', text_lower)
            if gs_match:
                extracted["green_space_ratio"] = cls._to_float(gs_match.group(1)) / 100.0
            elif "low green space" in text_lower or "green space: low" in text_lower:
                extracted["green_space_ratio"] = "low"

            canopy_match = re.search(r'(?:canopy(?:\s+cover)?|tree\s+cover)(?:[^\d\n]{0,25}?)([0-9.]+)\s*%?', text_lower)
            if not canopy_match:
                canopy_match = re.search(r'([0-9.]+)\s*%\s*(?:canopy|tree\s+cover)', text_lower)
            if canopy_match and "canopy_cover_pct" not in extracted:
                extracted["canopy_cover_pct"] = cls._to_float(canopy_match.group(1))

            # Slope and erosion
            slope_match = re.search(r'([0-9.]+)\s*%\s*slope', text_lower)
            if not slope_match:
                slope_match = re.search(r'(?:slope\s*(?:angle|degrees)?)[^\d\n]{0,15}?([0-9.]+)', text_lower)
            if slope_match and "slope_degrees" not in extracted:
                extracted["slope_degrees"] = cls._to_float(slope_match.group(1))

            # Negation check for erosion
            has_negated_erosion = any(neg in text_lower for neg in [
                "don't have erosion", "do not have erosion", "no erosion", "without erosion",
                "not have erosion", "not eroded", "no sign of erosion", "erosion is not",
                "free of erosion", "zero erosion"
            ])
            if has_negated_erosion:
                extracted["soil_erosion_rate"] = None
                extracted["_retracted_fields"] = extracted.get("_retracted_fields", []) + ["soil_erosion_rate"]
            elif "erosion" in text_lower or "rill erosion" in text_lower or "topsoil loss" in text_lower:
                extracted["soil_erosion_rate"] = "severe" if any(w in text_lower for w in ["severe", "high", "active", "rill"]) else "moderate"

            # Compaction and Runoff detection
            has_negated_compaction = any(neg in text_lower for neg in [
                "don't have compaction", "do not have compaction", "don't have severe soil compaction",
                "no compaction", "without compaction", "not compacted", "no longer compacted",
                "compaction was remediated", "no soil compaction", "zero compaction"
            ])
            if has_negated_compaction:
                extracted["soil_compaction"] = None
                extracted["_retracted_fields"] = extracted.get("_retracted_fields", []) + ["soil_compaction"]
            elif any(term in text_lower for term in ["compacted", "compaction", "hardpan", "subsoil compaction", "crusting"]):
                extracted["soil_compaction"] = "severe" if any(w in text_lower for w in ["severe", "heavy", "high", "deep"]) else "moderate"
                if "tillage_practice" not in extracted:
                    extracted["tillage_practice"] = "conventional inversion tillage (crusted)"

            if any(term in text_lower for term in ["running off", "water runoff", "surface runoff", "water is running off"]):
                extracted["water_runoff"] = "high"
                extracted["water_infiltration"] = "restricted"
                if "soil_erosion_rate" not in extracted and not has_negated_erosion:
                    extracted["soil_erosion_rate"] = "moderate"

            # SOC extraction
            soc_match = re.search(
                r'(?:soc|soil\s+(?:organic\s+)?carbon|organic\s+carbon)(?:[\s:=of]+|(?:\s+(?:is|at|around|level|value|measures|of)\s+)|(?:\s*[:=]\s*))([0-9.]+)\s*%?',
                text_lower
            )
            if not soc_match:
                soc_match = re.search(
                    r'([0-9.]+)\s*%\s*(?:soc|soil\s+(?:organic\s+)?carbon|organic\s+carbon)',
                    text_lower
                )
            if soc_match and "soc_percent" not in extracted:
                extracted["soc_percent"] = cls._to_float(soc_match.group(1))
                extracted["soc_source"] = "user_reported"

            # Rainfall extraction
            # 1. Match explicit mm unit first (e.g., '280mm', '1900 mm rainfall')
            rain_match = re.search(r'([0-9.]+)\s*mm\b', text_lower)
            if not rain_match:
                # 2. Match number following rainfall without crossing commas or punctuation
                rain_match = re.search(r'(?:rainfall|precipitation|precip)[\s:=of]+([0-9.]+)', text_lower)
            if rain_match and "rainfall_mm" not in extracted:
                extracted["rainfall_mm"] = cls._to_float(rain_match.group(1))
                extracted["rainfall_source"] = "user_reported"
            elif re.search(r'(?:low\s+rainfall|rainfall[\s:=]+low)', text_lower) and "rainfall_mm" not in extracted:
                extracted["rainfall_mm"] = 320.0
                extracted["rainfall_pattern"] = "low / semi-arid"
                extracted["rainfall_source"] = "user_reported"
            elif re.search(r'(?:high\s+rainfall|rainfall[\s:=]+high)', text_lower) and "rainfall_mm" not in extracted:
                extracted["rainfall_mm"] = 1250.0
                extracted["rainfall_pattern"] = "high / humid"
                extracted["rainfall_source"] = "user_reported"

            # Rainfall pattern extraction
            rain_pat_match = re.search(r'(?:rainfall\s+pattern|rain\s+pattern)[\s:=of]+([^,\.\n]+)', text_lower)
            if rain_pat_match and "rainfall_pattern" not in extracted:
                extracted["rainfall_pattern"] = rain_pat_match.group(1).strip()

            # Biome / Region extraction
            biomes = [
                "semi-arid", "semi arid", "arid", "mediterranean",
                "temperate grassland", "temperate-grassland",
                "tropical savanna", "tropical-savanna", "humid subtropical",
                "humid-subtropical", "sub-humid", "tropical rainforest",
                "tropical-rainforest", "temperate forest", "temperate-forest",
                "freshwater wetland", "freshwater-wetland", "high rainfall", "urban"
            ]
            for b in biomes:
                if b in text_lower and "biome" not in extracted:
                    extracted["biome"] = b.replace(" ", "-")
                    break

            # Region key phrase (e.g. "Region: semi-arid", "Region: high rainfall")
            region_match = re.search(r'region[\s:=of]+([^,\.\n]+)', text_lower)
            if region_match:
                reg_val = region_match.group(1).strip().replace(" ", "-")
                if "biome" not in extracted:
                    extracted["biome"] = reg_val
                extracted["region"] = reg_val

            # Land use type extraction
            land_use_match = re.search(r'(?:land\s+use(?:\s+type)?|cropping\s+system|farming\s+system)[\s:=of]+([^,\.\n]+)', text_lower)
            if land_use_match:
                extracted["land_use_type"] = land_use_match.group(1).strip()
                if "current_crop" not in extracted:
                    extracted["current_crop"] = land_use_match.group(1).strip()

            # Current crop / cropping system / ecosystem land-use terms
            land_uses = [
                "monoculture wheat", "continuous wheat", "wheat monoculture", "monoculture",
                "wheat-fallow rotation", "wheat-pulse rotation", "cereal-pulse rotation",
                "cereal-legume intercropping", "cereal-legume intercrop", "intercropping",
                "mixed agro-pastoral", "mixed agroforestry", "agroforestry", "mixed cropping",
                "corn monoculture", "maize", "soybean", "barley", "sorghum", "cotton",
                "rice", "chickpea", "pigeonpea", "fallow-wheat", "canola", "sunflower", "wheat",
                "urban lake", "urban park", "city park", "urban green space", "constructed wetland",
                "natural wetland", "marsh", "lake", "fragmented forest", "secondary forest",
                "primary forest", "timber plantation"
            ]
            for lu in land_uses:
                if lu in text_lower and "current_crop" not in extracted:
                    extracted["current_crop"] = lu
                    if "land_use_type" not in extracted:
                        extracted["land_use_type"] = lu
                    break

            # pH extraction
            ph_match = re.search(r'(?:ph|soil\s+ph)[\s:=of]+([0-9.]+)', text_lower)
            if ph_match and "ph" not in extracted:
                extracted["ph"] = cls._to_float(ph_match.group(1))
                extracted["ph_source"] = "user_reported"

            # Soil Texture extraction
            textures = [
                "sandy loam", "clay loam", "silty clay", "loamy sand",
                "sandy clay", "silt loam", "sandy", "clay", "loam"
            ]
            for t in textures:
                if t in text_lower and "soil_texture" not in extracted:
                    extracted["soil_texture"] = t
                    break

            # Canopy cover
            canopy_match = re.search(r'(?:canopy(?:\s+cover)?|tree\s+cover)[\s:=of]+([0-9.]+)\s*%?', text_lower)
            if canopy_match and "canopy_cover_pct" not in extracted:
                extracted["canopy_cover_pct"] = cls._to_float(canopy_match.group(1))

            # Irrigation status
            if "rainfed" in text_lower or "dryland" in text_lower or "no irrigation" in text_lower:
                extracted["irrigation_status"] = "rainfed"
            elif "drip" in text_lower:
                extracted["irrigation_status"] = "drip"
            elif "pivot" in text_lower:
                extracted["irrigation_status"] = "center_pivot"
            elif "flood" in text_lower or "furrow" in text_lower:
                extracted["irrigation_status"] = "flood"

            # Tillage
            if "no-till" in text_lower or "zero tillage" in text_lower or "zero-till" in text_lower:
                extracted["tillage_practice"] = "no-till"
            elif "conventional till" in text_lower or "deep plough" in text_lower or "tillage" in text_lower:
                extracted["tillage_practice"] = "conventional"

            # Geographic coordinates extraction
            coord_match = re.search(
                r'(?:lat(?:itude)?[\s:=]+)?([+-]?[0-9]{1,2}\.[0-9]+)[,\s]+(?:lon(?:gitude)?[\s:=]+)?([+-]?[0-9]{1,3}\.[0-9]+)',
                stripped_text
            )
            if coord_match and "latitude" not in extracted:
                try:
                    lat_c = float(coord_match.group(1))
                    lon_c = float(coord_match.group(2))
                    if -90 <= lat_c <= 90 and -180 <= lon_c <= 180:
                        extracted["latitude"] = lat_c
                        extracted["longitude"] = lon_c
                        if detected_mode == "free_text":
                            detected_mode = "geo_coordinates"
                except Exception:
                    pass

            # Satellite & remote sensing terms
            if "ndvi" in text_lower:
                ndvi_m = re.search(r'ndvi[\s:=]+([0-9.]+)', text_lower)
                if ndvi_m:
                    extracted["ndvi"] = cls._to_float(ndvi_m.group(1))

            if "spi" in text_lower:
                spi_m = re.search(r'spi[\s:=]+([+-]?[0-9.]+)', text_lower)
                if spi_m:
                    extracted["drought_index_spi"] = cls._to_float(spi_m.group(1))

        # Infer default ecosystem_type if still missing
        if "ecosystem_type" not in extracted:
            biome_val = extracted.get("biome", "")
            crop_val = extracted.get("current_crop", "")
            if "urban" in biome_val or "urban" in crop_val:
                extracted["ecosystem_type"] = "urban"
            elif "wetland" in biome_val or "lake" in crop_val:
                extracted["ecosystem_type"] = "wetland"
            elif "forest" in biome_val or "forest" in crop_val:
                extracted["ecosystem_type"] = "forest"
            elif "grassland" in biome_val:
                extracted["ecosystem_type"] = "grassland"
            else:
                extracted["ecosystem_type"] = "agricultural"

        return extracted, detected_mode, detected_ambiguities

    @staticmethod
    def _to_float(val: Any) -> Optional[float]:
        try:
            return round(float(val), 2)
        except (ValueError, TypeError):
            return None
