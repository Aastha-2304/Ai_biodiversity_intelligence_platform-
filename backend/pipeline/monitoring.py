"""
On-Farm Monitoring Plan Generator — Stage 8
Darukaa.Earth AI Biodiversity Intelligence Platform
"""

from typing import List, Dict, Any


MONITORING_PROTOCOLS: Dict[str, Dict[str, str]] = {
    "soil_organic_carbon": {
        "parameter": "Soil Organic Carbon (SOC %)",
        "baseline_method": "Collect 10 composite core samples at 0-15cm and 15-30cm depths for dry-combustion elemental analysis.",
        "frequency": "Annually post-harvest under consistent soil moisture.",
        "short_term_indicator": "Darkening of topsoil surface, visible root exudation, and reduced surface crusting/slaking.",
        "long_term_indicator": "Lab-verified +0.2% to +0.4% absolute increase in stable mineral-associated organic carbon over 3-5 years."
    },
    "soil_moisture_infiltration": {
        "parameter": "Water Infiltration Rate & Available Moisture",
        "baseline_method": "Conduct single-ring cylinder infiltration test (mm/hr) and log top 30cm volumetric water content.",
        "frequency": "Monthly during vegetative growth and within 24h of rainfall events.",
        "short_term_indicator": "Elimination of surface runoff ponding; rain penetration depth increased by >40mm after convective storms.",
        "long_term_indicator": "Cereal crop maintains leaf turgor and delayed drought-induced flag leaf senescence during seasonal dry spells."
    },
    "microbial_activity": {
        "parameter": "Soil Microbial Biomass & Mycorrhizal Colonization",
        "baseline_method": "Microbial Biomass Carbon (SMBC) substrate-induced respiration assay or root AMF staining transect.",
        "frequency": "Biennially during spring root flush.",
        "short_term_indicator": "Proliferation of fungal hyphal threading in root rhizosphere and increased earthworm burrows.",
        "long_term_indicator": "50-80% increase in active microbial biomass carbon, accelerating organic nutrient mineralization."
    },
    "pollinator_habitat": {
        "parameter": "Wild Pollinator & Beneficial Insect Richness",
        "baseline_method": "15-minute standardized visual transect survey (50m x 2m) along field boundary and intercrop rows.",
        "frequency": "Twice monthly during crop anthesis and tree flowering.",
        "short_term_indicator": "Observation of solitary native bees, hoverflies (Syrphidae), and parasitoid wasps on boundary vegetation.",
        "long_term_indicator": "Permanent native bee nesting colonies and measurable biological aphid/caterpillar pest suppression without broad-spectrum insecticides."
    }
}


def generate_monitoring_plan(recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generates an actionable on-farm monitoring protocol tailored to active interventions."""
    selected_keys = ["soil_organic_carbon", "soil_moisture_infiltration"]

    for rec in recommendations:
        action_lower = rec.get("action", "").lower()
        if "legume" in action_lower or "intercrop" in action_lower:
            selected_keys.append("microbial_activity")
        if "shelterbelt" in action_lower or "agroforestry" in action_lower:
            selected_keys.append("pollinator_habitat")

    # Deduplicate while preserving order
    seen = set()
    unique_keys = []
    for k in selected_keys:
        if k not in seen and k in MONITORING_PROTOCOLS:
            seen.add(k)
            unique_keys.append(k)

    return [MONITORING_PROTOCOLS[k] for k in unique_keys[:4]]
