"""
Case File Session Management
Darukaa.Earth AI Biodiversity Intelligence Platform

STAGE 1 SCIENTIST IMPLEMENTATION:
- Maintains accumulating environmental profile across 8 environmental dimensions.
- Tags every measurement with {value, unit, source, date, confidence}.
- Detects multi-turn contradictions and logs them.
- Updates compressed clinical running_assessment summary (rewritten each turn).
- Enriches profile with spatial context when coordinates are available.
"""

from typing import Dict, Any, Optional, List
import datetime
import uuid
from backend.pipeline.spatial_context import SpatialContextEngine


class CaseFileSession:
    """In-memory accumulating environmental case file per user session."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())[:8]
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.created_at = now_iso
        self.updated_at = now_iso

        # 8-Dimension Environmental Parameter Profile
        self.profile: Dict[str, Any] = {
            # 1. Climate & Weather
            "biome": None,
            "rainfall_mm": None,
            "rainfall_pattern": None,
            "temperature_range": None,
            "humidity_pct": None,
            "pet_mm": None,
            "drought_index_spi": None,
            "wind_pattern": None,

            # 2. Soil Parameters
            "soc_percent": None,
            "ph": None,
            "soil_moisture_pct": None,
            "soil_texture": None,
            "npk_levels": None,
            "soil_microbial_biomass": None,
            "soil_erosion_rate": None,
            "soil_compaction": None,
            "water_runoff": None,
            "water_infiltration": None,
            "tillage_practice": None,

            # 3. Carbon & Vegetation Parameters
            "carbon_stock_tha": None,
            "carbon_sequestration_rate": None,
            "ndvi": None,
            "evi": None,
            "lai": None,
            "canopy_cover_pct": None,
            "vegetation_cover_pct": None,

            # 4. Land Use / Land Cover
            "current_crop": None,
            "land_use_type": None,
            "land_use_change_rate": None,
            "fragmentation_index": None,
            "urbanization_rate": None,
            "agricultural_intensity": None,
            "deforestation_rate": None,

            # 5. Water Parameters
            "irrigation_status": None,
            "water_table_depth_m": None,
            "surface_water_availability": None,
            "water_stress_index": None,
            "water_quality": None,

            # 6. Air Quality Parameters
            "aqi": None,
            "pm25_ugm3": None,
            "co2_ppm": None,

            # 7. Topographic Parameters
            "elevation_m": None,
            "slope_degrees": None,
            "terrain_ruggedness": None,

            # 8. Anthropogenic Pressure
            "population_density": None,
            "infrastructure_density": None,
            "nighttime_light_intensity": None,
            "land_degradation_index": None,

            # Ecosystem Classification & Cross-Domain Metrics
            "ecosystem_type": "agricultural",
            "pollution_level": None,
            "water_level": None,
            "green_space_ratio": None,
            "biodiversity_status": None,

            # Spatial coordinates
            "latitude": None,
            "longitude": None,
            "spatial_context": None
        }

        self.provenance: Dict[str, Dict[str, Any]] = {}
        self.diagnostic_history: List[Dict[str, Any]] = []
        self.contradiction_history: List[Dict[str, Any]] = []
        self.running_assessment: str = "Awaiting initial field telemetry across environmental dimensions."
        self.turn_count: int = 0

    def update_profile(
        self,
        new_data: Dict[str, Any],
        contradictions: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Merges newly extracted fields with provenance tracking and updates running assessment."""
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        updated_fields = []

        units_map = {
            "soc_percent": "%",
            "rainfall_mm": "mm/yr",
            "pet_mm": "mm/yr",
            "ph": "pH units",
            "soil_moisture_pct": "% volumetric",
            "vegetation_cover_pct": "%",
            "canopy_cover_pct": "%",
            "elevation_m": "m a.s.l.",
            "latitude": "deg N",
            "longitude": "deg E",
            "water_table_depth_m": "m depth",
            "ndvi": "unitless (-1 to 1)",
            "drought_index_spi": "SPI index"
        }

        # Handle user retractions/corrections
        retracted_list = new_data.get("_retracted_fields", [])
        if retracted_list:
            current_retracted = set(self.profile.get("_retracted_fields", []))
            current_retracted.update(retracted_list)
            self.profile["_retracted_fields"] = list(current_retracted)

        for field in retracted_list:
            if field in self.profile and self.profile[field] is not None:
                self.profile[field] = None
                updated_fields.append(f"retracted_{field}")
                if field in self.provenance:
                    del self.provenance[field]

        for k, v in new_data.items():
            if k.startswith("_"):
                continue
            if v is not None and k in self.profile:
                if self.profile[k] != v:
                    self.profile[k] = v
                    updated_fields.append(k)

                    # Build provenance tag
                    source_tag = new_data.get(f"{k}_source") or (
                        "json_input" if "source" not in k else "user_reported"
                    )
                    self.provenance[k] = {
                        "value": v,
                        "unit": units_map.get(k, "categorical/index"),
                        "source": source_tag,
                        "date": now_iso[:10],
                        "confidence": (
                            0.90 if "json" in str(source_tag) or "spatial" in str(source_tag) else 0.75
                        )
                    }

        # Spatial enrichment if coordinates provided
        SpatialContextEngine.enrich_profile(self.profile)

        if contradictions:
            self.contradiction_history.extend(contradictions)

        self._regenerate_running_assessment()
        self.updated_at = now_iso
        self.turn_count += 1
        return {"updated_fields": updated_fields, "profile": self.profile}

    def _regenerate_running_assessment(self):
        """Rewrites (does not append) a crisp clinical environmental summary of the parcel."""
        soc = self.profile.get("soc_percent")
        rain = self.profile.get("rainfall_mm")
        crop = self.profile.get("current_crop") or "cereal crop"
        biome = self.profile.get("biome") or "semi-arid dryland"
        irr = self.profile.get("irrigation_status") or "rainfed"
        frag = self.profile.get("fragmentation_index")
        ndvi = self.profile.get("ndvi")

        parts = []

        # Soil Carbon & Biological Status
        if soc is not None:
            if float(soc) < 0.5:
                parts.append(f"Land displays critical topsoil organic carbon depletion ({soc}% SOC), indicative of collapsed microbial biomass, glomalin loss, and impaired water-holding capacity.")
            elif float(soc) < 1.0:
                parts.append(f"Topsoil exhibits sub-optimal organic carbon ({soc}% SOC) with moderate biological vulnerability.")
            else:
                parts.append(f"Soil organic carbon is relatively stable ({soc}% SOC).")
        else:
            parts.append("Soil organic carbon status remains unverified.")

        # Climatic Regime & Water Availability
        if rain is not None:
            if float(rain) < 350.0:
                parts.append(f"Precipitation regime ({rain} mm/yr, {biome}) imposes acute evaporative vapor pressure deficit under {irr} management.")
            else:
                parts.append(f"Precipitation baseline ({rain} mm/yr, {biome}) provides viable moisture for targeted agroecological diversification.")
        else:
            parts.append(f"Climatic baseline is categorized under {biome} conditions.")

        # Cropping System & Biodiversity
        if "monoculture" in str(crop).lower() or "wheat" in str(crop).lower():
            parts.append(f"Continuous {crop} cultivation exacerbates rhizosphere pathogen concentration and eliminates native pollinator floral corridors.")
        else:
            parts.append(f"Cropping matrix: {crop}.")

        if frag or ndvi:
            parts.append(f"Earth observation indicates canopy/vegetative cover index at NDVI {ndvi or 'low'}.")

        self.running_assessment = " ".join(parts)

    def count_established_variables(self) -> int:
        """Counts how many core environmental variables are currently established."""
        core_keys = [
            "soc_percent", "rainfall_mm", "biome", "current_crop", "ph",
            "soil_texture", "irrigation_status", "tillage_practice",
            "canopy_cover_pct", "fragmentation_index", "elevation_m",
            "water_table_depth_m", "ndvi", "drought_index_spi"
        ]
        return sum(1 for k in core_keys if self.profile.get(k) is not None and self.profile.get(k) != "")

    def record_turn(self, message: str, rule_eval: Dict[str, Any], recommendations: List[Any]):
        """Logs turn details for multi-turn conversational intelligence."""
        rec_ids = []
        for r in recommendations:
            if isinstance(r, dict):
                rec_ids.append(r.get("id"))
            elif hasattr(r, "id"):
                rec_ids.append(r.id)

        self.diagnostic_history.append({
            "turn": self.turn_count,
            "message": message,
            "diagnostic_hypothesis": rule_eval.get("diagnostic_hypothesis"),
            "system_health_index": rule_eval.get("system_health_index"),
            "recommendation_ids": rec_ids
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "profile": self.profile,
            "provenance": self.provenance,
            "running_assessment": self.running_assessment,
            "turn_count": self.turn_count,
            "contradiction_count": len(self.contradiction_history),
            "contradiction_history": self.contradiction_history,
            "established_variables_count": self.count_established_variables(),
            "diagnostic_history": self.diagnostic_history
        }


# Global session registry
_SESSION_STORE: Dict[str, CaseFileSession] = {}


def get_or_create_case_file(session_id: str) -> CaseFileSession:
    if session_id not in _SESSION_STORE:
        _SESSION_STORE[session_id] = CaseFileSession(session_id)
    return _SESSION_STORE[session_id]


def reset_case_file(session_id: str) -> CaseFileSession:
    _SESSION_STORE[session_id] = CaseFileSession(session_id)
    return _SESSION_STORE[session_id]
