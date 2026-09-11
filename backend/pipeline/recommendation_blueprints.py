"""
Technical Visual Blueprints & Step-by-Step Field Instructions Module
Darukaa.Earth AI Biodiversity Intelligence Platform

Provides:
1. Technical SVG Blueprint Diagrams illustrating structural cross-sections,
   spacing, root profiles, and biophysical flows for each intervention.
2. Step-by-Step Actionable Implementation Guides (Phase 1, 2, 3 + Pitfalls).
"""

from typing import Dict, Any


BLUEPRINT_INSTRUCTIONS: Dict[str, Dict[str, Any]] = {
    "INT-LEGUME-INTERCROPPING": {
        "title": "Legume-Based Cover Cropping & Strip Intercropping",
        "diagram_title": " Cross-Section: Cereal-Legume Strip Intercropping & AMF Hyphae Grid",
        "svg": """
<svg viewBox="0 0 700 230" width="100%" height="210" style="background:#091410;border-radius:8px">
  <defs>
    <linearGradient id="legSoil" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3d2817"/>
      <stop offset="100%" stop-color="#1f140b"/>
    </linearGradient>
    <pattern id="amfNet" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 0 10 L 20 10 M 10 0 L 10 20" fill="none" stroke="rgba(52,211,153,0.15)" stroke-width="0.7"/>
    </pattern>
  </defs>
  <!-- Sky -->
  <rect x="0" y="0" width="700" height="90" fill="#0c1d18"/>
  <!-- Soil layer -->
  <rect x="0" y="90" width="700" height="140" fill="url(#legSoil)"/>
  <rect x="0" y="90" width="700" height="140" fill="url(#amfNet)"/>
  <line x1="0" y1="90" x2="700" y2="90" stroke="#52796f" stroke-width="2"/>

  <!-- Row Markers -->
  <text x="110" y="25" fill="#facc15" font-size="11" font-weight="700" text-anchor="middle">4 CEREAL ROWS</text>
  <text x="110" y="40" fill="#9dbfb8" font-size="9" text-anchor="middle">(Wheat / Sorghum)</text>
  <text x="350" y="25" fill="#34d399" font-weight="700" font-size="11" text-anchor="middle">2 LEGUME ROWS</text>
  <text x="350" y="40" fill="#a7f3d0" font-size="9" text-anchor="middle">(Chickpea / Cowpea)</text>
  <text x="590" y="25" fill="#facc15" font-size="11" font-weight="700" text-anchor="middle">4 CEREAL ROWS</text>
  <text x="590" y="40" fill="#9dbfb8" font-size="9" text-anchor="middle">(Wheat / Sorghum)</text>

  <!-- Plants Cereal 1 -->
  <path d="M 70 90 L 70 50 M 60 70 Q 70 55 80 70 M 65 60 Q 70 45 75 60" stroke="#eab308" stroke-width="2.2" fill="none"/>
  <path d="M 110 90 L 110 46 M 100 68 Q 110 52 120 68 M 105 58 Q 110 42 115 58" stroke="#eab308" stroke-width="2.2" fill="none"/>
  <path d="M 150 90 L 150 50 M 140 70 Q 150 55 160 70" stroke="#eab308" stroke-width="2.2" fill="none"/>

  <!-- Legume Plants with Nodules -->
  <path d="M 320 90 Q 325 65 315 52 M 310 65 Q 325 60 330 70" stroke="#34d399" stroke-width="2.5" fill="none"/>
  <circle cx="316" cy="50" r="3.5" fill="#ec4899"/>
  <circle cx="330" cy="54" r="3.5" fill="#ec4899"/>
  <path d="M 370 90 Q 365 65 375 52 M 360 65 Q 375 60 380 70" stroke="#34d399" stroke-width="2.5" fill="none"/>
  <circle cx="376" cy="50" r="3.5" fill="#ec4899"/>

  <!-- Cereal Plants 2 -->
  <path d="M 550 90 L 550 50 M 540 70 Q 550 55 560 70" stroke="#eab308" stroke-width="2.2" fill="none"/>
  <path d="M 590 90 L 590 46 M 580 68 Q 590 52 600 68 M 585 58 Q 590 42 595 58" stroke="#eab308" stroke-width="2.2" fill="none"/>
  <path d="M 630 90 L 630 50 M 620 70 Q 630 55 640 70" stroke="#eab308" stroke-width="2.2" fill="none"/>

  <!-- Roots & Nodules -->
  <path d="M 110 90 Q 90 120 70 145 M 110 90 Q 130 130 140 160" stroke="#92400e" stroke-width="1.8" fill="none"/>
  <path d="M 345 90 Q 330 125 320 165 M 345 90 Q 365 130 380 170" stroke="#10b981" stroke-width="2.2" fill="none"/>
  <circle cx="335" cy="115" r="4" fill="#f43f5e"/>
  <circle cx="355" cy="125" r="3.5" fill="#f43f5e"/>
  <circle cx="340" cy="140" r="4" fill="#f43f5e"/>
  <circle cx="365" cy="150" r="3.5" fill="#f43f5e"/>
  <path d="M 590 90 Q 570 120 550 150 M 590 90 Q 610 130 620 160" stroke="#92400e" stroke-width="1.8" fill="none"/>

  <!-- AMF Hyphal Bridges between rows -->
  <path d="M 140 140 Q 230 165 320 145" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>
  <path d="M 380 145 Q 470 165 550 140" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>

  <!-- Annotations -->
  <rect x="250" y="185" width="200" height="32" rx="6" fill="#132a22" stroke="#34d399" stroke-width="1"/>
  <text x="350" y="200" fill="#34d399" font-size="10" font-weight="700" text-anchor="middle">RHIZOBIAL N-NODULES ()</text>
  <text x="350" y="212" fill="#38bdf8" font-size="9" text-anchor="middle">AMF Hyphal Bridges Share P &amp; Water (---)</text>
</svg>
""",
        "phase1": "**Site Preparation & Seed Inoculation (Months 0–1)**: Select local drought-adapted pulse seeds (Chickpea, Cowpea, or Pigeonpea). Coat seeds with species-specific *Rhizobium* liquid inoculant (5 g/kg seed) mixed with 10% jaggery/sugar solution in shade 2 hours before drilling. Ensure topsoil moisture is at least 12%.",
        "phase2": "**Planting Layout & Strip Calibration (Month 1–2)**: Configure seed drill for a 4:2 strip configuration (4 rows cereal spaced at 25cm, followed by 2 rows pulse spaced at 35cm). Drill pulses at 4–5cm depth and cereals at 3cm depth. Maintain row orientation North-to-South to maximize solar capture on both crops.",
        "phase3": "**Termination & Biomass Cycling (Month 3–5)**: At 10–20% pulse flowering, roller-crimp or lightly mow the cover crop rows in dryland zones to stop transpiration before moisture stress occurs (CSIRO warning). In grain pulse systems, harvest pods and immediately mulch crop residue across cereal stubble.",
        "pitfalls": " **Critical Mistake to Avoid**: Do not apply heavy synthetic nitrogen (>30 kg N/ha) at planting, as excess inorganic nitrogen inhibits Rhizobium nodulation and suppresses AMF mycorrhizal colonization. In dryland zones (<350mm rain), do not let pulse cover crops mature past first pod fill.",
        "species": "Cicer arietinum (Chickpea), Vigna unguiculata (Cowpea), Cajanus cajan (Pigeonpea), Trifolium alexandrinum (Berseem Clover)."
    },

    "INT-AGROFORESTRY-DRYLAND": {
        "title": "Dryland Parkland Agroforestry with Faidherbia albida",
        "diagram_title": " Parkland Architecture: Reverse Phenology & Hydraulic Lift Profiles",
        "svg": """
<svg viewBox="0 0 700 230" width="100%" height="210" style="background:#091410;border-radius:8px">
  <!-- Sky -->
  <rect x="0" y="0" width="700" height="85" fill="#0e231d"/>
  <!-- Soil -->
  <rect x="0" y="85" width="700" height="145" fill="#2d1c10"/>
  <line x1="0" y1="85" x2="700" y2="85" stroke="#714528" stroke-width="2"/>

  <!-- Deep Aquifer -->
  <rect x="0" y="195" width="700" height="35" fill="#0d2836"/>
  <text x="350" y="217" fill="#38bdf8" font-size="10" font-weight="700" text-anchor="middle">SUBTERRANEAN MOISTURE RESERVOIR (>10m Depth)</text>

  <!-- Faidherbia Tree Center -->
  <rect x="342" y="35" width="16" height="50" fill="#5c381e"/>
  <ellipse cx="350" cy="30" rx="65" ry="25" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2"/>
  <text x="350" y="34" fill="#e2f0ec" font-size="10" font-weight="700" text-anchor="middle">Faidherbia albida</text>

  <!-- Deep Taproot -->
  <path d="M 350 85 L 350 200" stroke="#10b981" stroke-width="4"/>
  <!-- Hydraulic Lift Arrows -->
  <path d="M 345 160 L 345 110 M 341 125 L 345 115 L 349 125" stroke="#38bdf8" stroke-width="2" fill="none"/>
  <path d="M 355 160 L 355 110 M 351 125 L 355 115 L 359 125" stroke="#38bdf8" stroke-width="2" fill="none"/>

  <!-- Shallow Lateral Roots pumping water to crops -->
  <path d="M 350 100 Q 230 105 130 115" stroke="#34d399" stroke-width="2.5" fill="none"/>
  <path d="M 350 100 Q 470 105 570 115" stroke="#34d399" stroke-width="2.5" fill="none"/>

  <!-- Intercropped Wheat Under Tree -->
  <path d="M 180 85 L 180 62 M 175 75 Q 180 67 185 75" stroke="#eab308" stroke-width="2" fill="none"/>
  <path d="M 230 85 L 230 58 M 225 72 Q 230 63 235 72" stroke="#34d399" stroke-width="2.2" fill="none"/>
  <path d="M 280 85 L 280 55 M 275 70 Q 280 60 285 70" stroke="#34d399" stroke-width="2.2" fill="none"/>
  <path d="M 420 85 L 420 55 M 415 70 Q 420 60 425 70" stroke="#34d399" stroke-width="2.2" fill="none"/>
  <path d="M 470 85 L 470 58 M 465 72 Q 470 63 475 72" stroke="#34d399" stroke-width="2.2" fill="none"/>
  <path d="M 520 85 L 520 62 M 515 75 Q 520 67 525 75" stroke="#eab308" stroke-width="2" fill="none"/>

  <!-- Callouts -->
  <rect x="20" y="10" width="160" height="42" rx="6" fill="#132a22" stroke="#38bdf8" stroke-width="1"/>
  <text x="100" y="26" fill="#38bdf8" font-size="9.5" font-weight="700" text-anchor="middle">HYDRAULIC LIFT</text>
  <text x="100" y="42" fill="#cbd5e1" font-size="8.5" text-anchor="middle">Subsoil water pumped to crop roots</text>

  <rect x="520" y="10" width="160" height="42" rx="6" fill="#132a22" stroke="#34d399" stroke-width="1"/>
  <text x="600" y="26" fill="#34d399" font-size="9.5" font-weight="700" text-anchor="middle">LEAF LITTER ENRICHMENT</text>
  <text x="600" y="42" fill="#cbd5e1" font-size="8.5" text-anchor="middle">+0.4% SOC in canopy drip-line</text>
</svg>
""",
        "phase1": "**Nursery Propagation & Pit Excavation (Months 0–2)**: Source healthy, mycorrhiza-inoculated *Faidherbia albida* and *Ziziphus mauritiana* seedlings (30–45cm tall). Dig planting pits (60cm x 60cm x 60cm) spaced at 8m x 12m grid (approx. 100 trees/ha) across cropland. Incorporate 5 kg aged compost and 100g biochar into pit base.",
        "phase2": "**Monsoon Outplanting & Water Catchment (Month 2–4)**: Plant out at onset of primary rains. Form micro-catchment crescent earthen berms (half-moons / negarms) upslope of each pit to channel episodic sheet runoff directly into seedling root zones. Install wire tree guards to prevent browsing by goats and hares.",
        "phase3": "**Formative Pruning & Litter Management (Years 1–3)**: During the first 2 years, prune lower lateral branches up to 1.5m to encourage a single dominant leader taproot. In year 3+, allow the reverse phenology canopy to develop fully; mulch fallen nitrogen-rich dry-season pods and leaflets directly into cereal furrows.",
        "pitfalls": " **Critical Mistake to Avoid**: Do not plant high water-demanding trees (such as Eucalyptus or unmanaged Leucaena) in dryland fields, which transpire aggressively during the crop season and desiccate shallow topsoil moisture reserves.",
        "species": "Faidherbia albida (Winter Thorn), Prosopis cineraria (Khejri), Ziziphus mauritiana (Ber), Acacia senegal."
    },

    "INT-URBAN-BIOSWALE-FILTER": {
        "title": "Vegetated Bio-Retention Swale & Stormwater Filter",
        "diagram_title": " Structural Blueprint: Engineered Bio-Retention Filter Bed Cross-Section",
        "svg": """
<svg viewBox="0 0 700 230" width="100%" height="210" style="background:#091410;border-radius:8px">
  <!-- Concrete Inflow Left -->
  <path d="M 0 60 L 110 60 L 140 100 L 560 100 L 590 60 L 700 60 L 700 230 L 0 230 Z" fill="#1c2b26"/>
  <!-- Engineered Filter Layers -->
  <rect x="140" y="95" width="420" height="20" fill="#3d2918" stroke="#523924"/>
  <text x="350" y="108" fill="#facc15" font-size="9" font-weight="700" text-anchor="middle">ORGANIC HARDWOOD MULCH LAYER (50mm)</text>
  <rect x="140" y="115" width="420" height="45" fill="#473e35" stroke="#5e5347"/>
  <text x="350" y="140" fill="#38bdf8" font-size="9.5" font-weight="700" text-anchor="middle">BIO-RETENTION MEDIA (85% Sand, 10% Fines, 5% Organic Matter)</text>
  <rect x="140" y="160" width="420" height="22" fill="#2d3748"/>
  <text x="350" y="175" fill="#94a3b8" font-size="9" text-anchor="middle">PEA GRAVEL CHOKE LAYER (5mm Aggregate)</text>
  <rect x="140" y="182" width="420" height="38" fill="#1e293b"/>
  <circle cx="350" cy="201" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="350" y="205" fill="#38bdf8" font-size="8" font-weight="700" text-anchor="middle">DRAIN</text>
  <text x="460" y="205" fill="#94a3b8" font-size="8.5">PERFORATED PVC OUTFLOW TO LAKE</text>

  <!-- Wetland Plants on Top -->
  <path d="M 200 95 L 200 50 M 190 75 Q 200 60 210 75" stroke="#34d399" stroke-width="2.2" fill="none"/>
  <circle cx="200" cy="48" r="4" fill="#a7f3d0"/>
  <path d="M 270 95 L 270 42 M 260 68 Q 270 54 280 68" stroke="#34d399" stroke-width="2.5" fill="none"/>
  <circle cx="270" cy="40" r="4" fill="#f43f5e"/>
  <path d="M 350 95 L 350 35 M 340 65 Q 350 50 360 65" stroke="#34d399" stroke-width="3" fill="none"/>
  <circle cx="350" cy="33" r="5" fill="#38bdf8"/>
  <path d="M 430 95 L 430 45 M 420 70 Q 430 55 440 70" stroke="#34d399" stroke-width="2.5" fill="none"/>
  <circle cx="430" cy="43" r="4" fill="#f43f5e"/>
  <path d="M 500 95 L 500 52 M 490 75 Q 500 62 510 75" stroke="#34d399" stroke-width="2.2" fill="none"/>

  <!-- Stormwater Inflow Arrow -->
  <path d="M 30 45 L 120 45 M 105 38 L 120 45 L 105 52" stroke="#f87171" stroke-width="3" fill="none"/>
  <text x="65" y="35" fill="#f87171" font-size="9" font-weight="700">DIRTY RUNOFF</text>
  <path d="M 364 201 L 430 201" stroke="#38bdf8" stroke-width="2" stroke-dasharray="2,2"/>
</svg>
""",
        "phase1": "**Hydraulic Sizing & Excavation (Months 0–1)**: Determine catchment impervious area. Size swale top surface to 5–8% of contributing runoff area. Excavate 0.8–1.0m deep channel with 3:1 side slopes. Install a rock energy dissipater (rip-rap) at the curb-cut inflow to arrest kinetic velocity and capture coarse gravel.",
        "phase2": "**Media Placement & Underdrain Installation (Month 1–2)**: Lay 100mm perforated slotted PVC pipe enveloped in 150mm clean pea gravel at trench bottom. Backfill with 600mm engineered filter media (85% coarse sand, 10% silt/clay fines, 5% mature organic compost). Top with 50mm shredded hardwood bark mulch.",
        "phase3": "**Deep-Rooting Native Hydrophytes Planting (Month 2–4)**: Plant deep-rooting native sedges (*Carex*), rushes (*Juncus*), and wetland iris at 30cm triangular spacing across ponding zone. Plant drought-tolerant native pollinator shrubs along upper side slopes. Irrigate weekly during initial 8-week root establishment.",
        "pitfalls": " **Critical Mistake to Avoid**: Never construct or plant swales while upslope construction is active without silt fences; fine clay and construction sediment will blind the engineered sand media within hours, causing permanent standing water and mosquito breeding.",
        "species": "Carex stricta, Juncus effusus (Soft Rush), Iris versicolor, Cornus sericea (Red Osier Dogwood), Lobelia cardinalis."
    },

    "INT-WETLAND-RIPARIAN-FILTER": {
        "title": "Multi-Tier Wetland Riparian Buffer & Macrophyte Biofiltration Strip",
        "diagram_title": " Riparian Biofilter: 3-Zone Denitrification & Sediment Trapping Corridor",
        "svg": """
<svg viewBox="0 0 700 230" width="100%" height="210" style="background:#091410;border-radius:8px">
  <!-- Sky -->
  <rect x="0" y="0" width="700" height="70" fill="#0b201a"/>
  <!-- Topography -->
  <path d="M 0 70 L 220 85 L 440 120 L 700 150 L 700 230 L 0 230 Z" fill="#2d1c10"/>
  <path d="M 440 125 L 700 150 L 700 230 L 440 230 Z" fill="#0d2836"/>
  <rect x="440" y="125" width="260" height="105" fill="rgba(56,189,248,0.2)"/>
  <line x1="440" y1="125" x2="700" y2="125" stroke="#38bdf8" stroke-width="2"/>

  <!-- Zone 1: Fast Grass Filter -->
  <text x="100" y="20" fill="#facc15" font-size="10" font-weight="700" text-anchor="middle">ZONE 1: GRASS BUFFER</text>
  <text x="100" y="35" fill="#9dbfb8" font-size="8.5" text-anchor="middle">Sediment &amp; Nitrate Trapping (10m)</text>
  <path d="M 40 75 L 40 50 M 60 77 L 60 48 M 90 80 L 90 52 M 130 82 L 130 50 M 170 85 L 170 54" stroke="#eab308" stroke-width="2.5"/>

  <!-- Zone 2: Riparian Trees & Shrubs -->
  <text x="330" y="20" fill="#34d399" font-size="10" font-weight="700" text-anchor="middle">ZONE 2: DEEP-ROOT TREES</text>
  <text x="330" y="35" fill="#a7f3d0" font-size="8.5" text-anchor="middle">Anaerobic Denitrification (15m)</text>
  <rect x="275" y="55" width="10" height="35" fill="#5c381e"/>
  <circle cx="280" cy="45" r="22" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2"/>
  <rect x="375" y="75" width="10" height="38" fill="#5c381e"/>
  <circle cx="380" cy="62" r="25" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2"/>
  <path d="M 280 90 L 280 180 M 380 110 L 380 190" stroke="#10b981" stroke-width="3"/>

  <!-- Zone 3: Emergent Macrophytes -->
  <text x="560" y="20" fill="#38bdf8" font-size="10" font-weight="700" text-anchor="middle">ZONE 3: EMERGENT REEDS</text>
  <text x="560" y="35" fill="#bae6fd" font-size="8.5" text-anchor="middle">Phosphate Bio-Uptake &amp; Oxygenation</text>
  <path d="M 470 140 L 470 95 M 465 115 L 475 115" stroke="#34d399" stroke-width="3"/>
  <circle cx="470" cy="92" r="3.5" fill="#854d0e"/>
  <path d="M 520 142 L 520 90 M 515 110 L 525 110" stroke="#34d399" stroke-width="3"/>
  <circle cx="520" cy="87" r="3.5" fill="#854d0e"/>
  <path d="M 580 145 L 580 98" stroke="#34d399" stroke-width="3"/>
  <circle cx="580" cy="95" r="3.5" fill="#854d0e"/>

  <!-- Callout -->
  <rect x="250" y="190" width="200" height="30" rx="6" fill="#132a22" stroke="#38bdf8" stroke-width="1"/>
  <text x="350" y="205" fill="#38bdf8" font-size="9" font-weight="700" text-anchor="middle">MICROBIAL DENITRIFICATION ZONE</text>
  <text x="350" y="215" fill="#cbd5e1" font-size="8" text-anchor="middle">NO3- converted to harmless N2 gas (88%)</text>
</svg>
""",
        "phase1": "**Perimeter Delineation & Zone Demarcation (Months 0–1)**: Mark a minimum 25–30m wide riparian setback from normal high-water lake mark. Divide into 3 zones: Zone 1 (10m dense perennial grass upslope), Zone 2 (10–15m native riparian forest/shrub intermediate), and Zone 3 (5m littoral emergent wetland macrophyte fringe).",
        "phase2": "**Earth Grading & Hydrophyte Rhizome Installation (Month 1–3)**: Shape shorelines to gentle 5:1 or 8:1 slope to eliminate wave undercutting. Plant rhizomes of emergent reeds (*Typha latifolia*, *Phragmites mauritianus*, *Scirpus lacustris*) at 40cm intervals in water depths of 10–50cm. Anchor with coconut coir geotextile bio-logs along the splash zone.",
        "phase3": "**Woody Revegetation & Weed Suppression (Month 3–6)**: Plant deep-rooting flood-tolerant native trees (*Salix*, *Populus*, *Alnus*) in Zone 2 to facilitate microbial denitrification in saturated root zones. Hand-weed invasive aquatic weeds (*Eichhornia*) until native reeds form a closed canopy.",
        "pitfalls": " **Critical Mistake to Avoid**: Do not allow cattle or heavy machinery access into the riparian buffer; hoof action shears macrophyte roots, accelerates bank slumping, and creates direct fecal nitrogen bypass channels directly into the lake basin.",
        "species": "Typha domingensis (Cattail), Scirpus validus (Softstem Bulrush), Phragmites australis, Salix caroliniana, Alnus glutinosa."
    },

    "INT-FOREST-CORRIDOR-LINK": {
        "title": "Structural Forest Biodiversity Corridors & Canopy Stepping Bridges",
        "diagram_title": " Forest Landscape Ecology: Stepping-Stone Corridor Linking Fragmented Cores",
        "svg": """
<svg viewBox="0 0 700 230" width="100%" height="210" style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.25);border-radius:8px">
  <rect x="0" y="0" width="700" height="60" fill="#FEF3C7"/>
  <rect x="0" y="60" width="700" height="170" fill="#78350F"/>
  <line x1="0" y1="60" x2="700" y2="60" stroke="#92400E" stroke-width="2"/>

  <!-- Core A & B -->
  <rect x="0" y="10" width="140" height="50" fill="#ECFDF5" stroke="#059669" stroke-width="2"/>
  <text x="70" y="38" fill="#065F46" font-size="11" font-weight="800" text-anchor="middle">FOREST CORE A</text>
  <rect x="560" y="10" width="140" height="50" fill="#ECFDF5" stroke="#059669" stroke-width="2"/>
  <text x="630" y="38" fill="#065F46" font-size="11" font-weight="800" text-anchor="middle">FOREST CORE B</text>

  <!-- Trees in corridor -->
  <circle cx="200" cy="30" r="18" fill="#047857"/>
  <circle cx="281" cy="22" r="22" fill="#059669"/>
  <circle cx="362" cy="18" r="25" fill="#10b981"/>
  <circle cx="441" cy="22" r="22" fill="#059669"/>
  <circle cx="510" cy="30" r="18" fill="#047857"/>

  <!-- Flight Path -->
  <path d="M 120 25 Q 350 -10 580 25" stroke="#D9A441" stroke-width="2.5" stroke-dasharray="6,4" fill="none"/>
  <text x="350" y="14" fill="#92400E" font-size="9.5" font-weight="700" text-anchor="middle">CANOPY BIRD &amp; MAMMAL GENE FLOW</text>

  <rect x="140" y="60" width="420" height="15" fill="#92400E"/>
  <text x="350" y="72" fill="#FEF3C7" font-size="8.5" font-weight="700" text-anchor="middle">DENSE PERIMETER SHRUB SHIELD (Arrests Wind &amp; Edge Desiccation)</text>

  <rect x="180" y="150" width="340" height="42" rx="6" fill="#FFFDF8" stroke="#059669" stroke-width="1.5"/>
  <text x="350" y="167" fill="#065F46" font-size="10" font-weight="700" text-anchor="middle">50–100m CONTINUOUS CANOPY CORRIDOR</text>
  <text x="350" y="182" fill="#4A3324" font-size="9" text-anchor="middle">Reduces edge mortality by 60%, enables interior species recolonization</text>
</svg>
""",
        "phase1": "**Corridor Survey & Landowner Alignment (Months 0–2)**: Map shortest straight-line distance between isolated forest patches (target width: minimum 50–100m to maintain interior microclimate). Mark existing stepping-stone remnant trees. Soil test for compaction and eradicate aggressive exotic vines/lianas.",
        "phase2": "**Dense Framework Species Planting (Months 2–5)**: Implement the Framework Species Method (3,000 trees/ha at 1.8m x 1.8m spacing). Plant 60% fast-growing pioneer trees with fleshy fruits to attract seed-dispersing frugivorous birds, and 40% slow-growing climax framework canopy trees. Mulch each stem with 10cm wood chips.",
        "phase3": "**Assisted Natural Regeneration & Canopy Closure (Years 1–3)**: Conduct bi-monthly ring-weeding around saplings. Bird perches installed at 25m intervals will drop diverse native wild seeds into the shaded understory, multiplying native species richness automatically.",
        "pitfalls": " **Critical Mistake to Avoid**: Avoid establishing narrow single-row tree lines (<15m wide); narrow strips are dominated entirely by edge-adapted predator species and hot desiccating winds, failing to support sensitive interior forest specialists.",
        "species": "Ficus microcarpa (Strangler Fig), Trema orientalis (Pioneer Charcoal Tree), Shorea robusta, Dipterocarpus, Syzygium cumini."
    },

    "INT-TROPICAL-SHADED-AGROFORESTRY": {
        "title": "Multi-Strata Shaded Polyculture & Nutrient Leaching Interception",
        "diagram_title": " Multi-Strata Vertical Layering & Deep Nutrient Safety Net Architecture",
        "svg": """
<svg viewBox="0 0 700 230" width="100%" height="210" style="background:#091410;border-radius:8px">
  <rect x="0" y="0" width="700" height="80" fill="#0d241d"/>
  <rect x="0" y="80" width="700" height="40" fill="#382110"/>
  <rect x="0" y="120" width="700" height="110" fill="#201309"/>

  <!-- Stratum 3 Overstory -->
  <ellipse cx="187" cy="25" rx="55" ry="20" fill="rgba(52,211,153,0.25)" stroke="#34d399" stroke-width="2"/>
  <text x="187" y="25" fill="#e2f0ec" font-size="9" font-weight="700" text-anchor="middle">OVERSTORY (20-25m) Inga edulis</text>
  <ellipse cx="527" cy="25" rx="55" ry="20" fill="rgba(52,211,153,0.25)" stroke="#34d399" stroke-width="2"/>
  <text x="527" y="25" fill="#e2f0ec" font-size="9" font-weight="700" text-anchor="middle">OVERSTORY Grevillea / Cordia</text>

  <!-- Stratum 2 Midstory -->
  <circle cx="85" cy="45" r="16" fill="rgba(245,158,11,0.3)" stroke="#f59e0b" stroke-width="1.8"/>
  <text x="85" y="48" fill="#fde68a" font-size="8" font-weight="700" text-anchor="middle">Banana</text>
  <circle cx="355" cy="42" r="18" fill="rgba(245,158,11,0.3)" stroke="#f59e0b" stroke-width="1.8"/>
  <text x="355" y="45" fill="#fde68a" font-size="8" font-weight="700" text-anchor="middle">Citrus</text>

  <!-- Understory Coffee -->
  <circle cx="130" cy="58" r="4" fill="#ef4444"/>
  <circle cx="270" cy="56" r="4" fill="#ef4444"/>
  <circle cx="430" cy="58" r="4" fill="#ef4444"/>

  <!-- Roots: Deep Safety Net -->
  <path d="M 187 80 L 187 205 M 187 140 Q 240 180 300 200" stroke="#10b981" stroke-width="3"/>
  <path d="M 527 80 L 527 205 M 527 140 Q 460 180 400 200" stroke="#10b981" stroke-width="3"/>

  <!-- Box -->
  <rect x="230" y="175" width="240" height="35" rx="6" fill="#132a22" stroke="#34d399" stroke-width="1"/>
  <text x="350" y="190" fill="#34d399" font-size="9.5" font-weight="700" text-anchor="middle">DEEP ROOT NUTRIENT SAFETY NET</text>
  <text x="350" y="202" fill="#cbd5e1" font-size="8.5" text-anchor="middle">Pumps deep minerals back to topsoil leaf litter</text>
</svg>
""",
        "phase1": "**Canopy Shade Assessment & Species Sourcing (Months 0–2)**: Gauge existing canopy cover (target 35–45% filtered shade). Procure nitrogen-fixing legume canopy shade trees (*Inga edulis*, *Erythrina*, *Gliricidia*) and commercial understory crops (Arabica Coffee or Cacao).",
        "phase2": "**Stratified Interplanting on Slopes (Months 2–4)**: Plant overstory shade trees on 10m x 10m grid. Plant intermediate economic fruit/timber trees (Banana, Citrus, Avocado) in mid-strata. Plant cash crop (Coffee/Cacao) at 2.5m x 2.5m spacing along contour lines.",
        "phase3": "**Periodic Crown Pruning & Biomass Mulching (Months 6–12+)**: Twice annually before peak rains, pollard and prune upper legume branches by 30–50%. Chop and drop all pruned green biomass directly across coffee root zones to provide a living organic mulch that prevents soil erosion on steep slopes.",
        "pitfalls": " **Critical Mistake to Avoid**: Do not allow overstory shade canopy to exceed 60% closure; dense shade promotes fungal pathogens (*Hemileia vastatrix* / coffee rust and black pod) and suppresses understory flowering.",
        "species": "Inga edulis (Ice Cream Bean), Erythrina poeppigiana, Coffea arabica, Theobroma cacao, Musa acuminata."
    }
}


def get_blueprint_for_intervention(intervention_id: str) -> Dict[str, Any]:
    """Retrieves technical SVG blueprint and step-by-step field guide for any intervention."""
    if intervention_id in BLUEPRINT_INSTRUCTIONS:
        return BLUEPRINT_INSTRUCTIONS[intervention_id]

    # Fallback generic blueprint if ID not explicitly mapped
    return {
        "title": "Ecological Restoration Intervention",
        "diagram_title": " Technical Implementation Schematic",
        "svg": """
<svg viewBox="0 0 700 200" width="100%" height="180" style="background:#091410;border-radius:8px">
  <rect x="20" y="20" width="660" height="160" rx="8" fill="#132a22" stroke="#34d399" stroke-width="1.5"/>
  <circle cx="120" cy="100" r="45" fill="rgba(52,211,153,0.2)" stroke="#34d399" stroke-width="2"/>
  <text x="120" y="105" fill="#34d399" font-size="28" text-anchor="middle"></text>
  <text x="200" y="85" fill="#34d399" font-size="14" font-weight="700">Multi-Tier Biophysical Practice</text>
  <text x="200" y="105" fill="#cbd5e1" font-size="12">Structured spacing, biological inoculation, and soil aggregate restoration.</text>
  <text x="200" y="125" fill="#38bdf8" font-size="11">Grounded in peer-reviewed ecological engineering field protocols.</text>
</svg>
""",
        "phase1": "**Site Preparation & Baseline Audit (Months 0–2)**: Audit topsoil compaction, hydrology, and native seed bank. Clear invasive species and source certified native germplasm.",
        "phase2": "**Structural Installation & Planting (Months 2–4)**: Follow contour lines and appropriate spatial spacing grids. Mulch planted beds with native organic biomass.",
        "phase3": "**Adaptive Management & Monitoring (Months 4–12+)**: Monitor seedling survival and soil moisture monthly. Supplement with restorative organic amendments as needed.",
        "pitfalls": " **Critical Mistake to Avoid**: Avoid unverified chemical applications or mechanical deep soil disturbance that disrupts emerging fungal mycorrhizal networks.",
        "species": "Native regional species adapted to prevailing hydrological and thermal regimes."
    }
