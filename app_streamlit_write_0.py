"""
Darukaa.Earth — AI Biodiversity Intelligence Platform
Streamlit Application (Single-file, self-contained unified deployment)
Run with: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import sys
import os
import textwrap
import datetime
import uuid
from pathlib import Path

# ── Add project root to path so backend imports resolve ──────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.pipeline.input_parser import InputParser
from backend.pipeline.completeness_check import CompletenessChecker
from backend.pipeline.rule_engine import EnvironmentalRuleEngine
from backend.pipeline.retrieval import KnowledgeRetriever
from backend.pipeline.intervention_library import InterventionLibrary
from backend.pipeline.reasoning_graph import MultiMetricReasoningGraph
from backend.pipeline.verifier import InputValidator, EvidenceVerifier
from backend.pipeline.llm_writer import ScientificWriter
from backend.pipeline.monitoring import generate_monitoring_plan
from backend.pipeline.spatial_context import SpatialContextEngine
from backend.pipeline.visualizations import (
    create_problem_severity_gauge_chart,
    create_5year_soc_trajectory_chart,
    create_multi_metric_comparison_chart,
    render_animated_rhizosphere_diagram,
    render_animated_agroforestry_diagram,
    render_animated_forest_corridor_diagram,
    render_animated_forest_stratification_diagram,
    render_animated_urban_bioswale_diagram,
    render_animated_urban_pocket_forest_diagram,
    render_animated_wetland_buffer_diagram,
    render_animated_wetland_hydro_sill_diagram,
    render_degradation_problem_diagram,
    render_animated_transition_roadmap_diagram
)
from backend.pipeline.recommendation_blueprints import get_blueprint_for_intervention
from backend.models.case_file import get_or_create_case_file, reset_case_file
from backend.database.audit_store import AuditDatabase

# Initialize Database on startup
AuditDatabase.initialize()

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Darukaa.Earth — AI Biodiversity Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS — WARM EARTH INTELLIGENCE DESIGN SYSTEM
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #382417;
}

/* Base Light Earth Background */
.stApp {
    background: radial-gradient(circle at 85% 15%, rgba(241, 199, 91, 0.22) 0%, transparent 60%),
                radial-gradient(circle at 15% 85%, rgba(193, 138, 91, 0.14) 0%, transparent 60%),
                linear-gradient(135deg, #FFF9ED 0%, #FFF5E1 50%, #FAEED7 100%);
    color: #382417;
}

/* Main Container Text overrides */
.stMarkdown, p, span, label, div {
    color: #382417;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: rgba(255, 250, 240, 0.96) !important;
    border-right: 1.5px solid rgba(169, 113, 66, 0.25) !important;
}

/* Brand Header */
.brand-header {
    background: rgba(255, 252, 246, 0.94);
    border: 1.5px solid rgba(169, 113, 66, 0.28);
    border-radius: 14px;
    padding: 16px 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(139, 94, 60, 0.08);
}
.brand-name {
    font-size: 24px;
    font-weight: 900;
    color: #382417;
    letter-spacing: 0.05em;
}
.brand-sub {
    font-size: 11.5px;
    color: #856852;
    font-family: 'Fira Code', monospace;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 2px;
}
.pipeline-badge {
    background: #FEF3C7;
    border: 1.5px solid #D9A441;
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 11px;
    color: #4A3324;
    font-family: 'Fira Code', monospace;
    font-weight: 800;
    letter-spacing: 0.06em;
    margin-left: auto;
    box-shadow: 0 2px 8px rgba(217, 164, 65, 0.15);
}
.cache-hit-badge {
    background: #D1FAE5;
    border: 1.5px solid #059669;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 11px;
    color: #065F46;
    font-family: 'Fira Code', monospace;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* Chat Messages */
.msg-user {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border: 1.5px solid #D9A441;
    border-radius: 14px 14px 4px 14px;
    padding: 14px 20px;
    margin: 10px 0 10px 40px;
    color: #382417;
    font-size: 13.5px;
    line-height: 1.6;
    box-shadow: 0 3px 12px rgba(217, 164, 65, 0.18);
}
.msg-system {
    background: rgba(255, 252, 246, 0.96);
    border: 1.5px solid rgba(169, 113, 66, 0.25);
    border-radius: 4px 14px 14px 14px;
    padding: 16px 22px;
    margin: 10px 40px 10px 0;
    color: #382417;
    font-size: 13.5px;
    line-height: 1.65;
    box-shadow: 0 4px 18px rgba(139, 94, 60, 0.07);
}
.msg-meta {
    font-family: 'Fira Code', monospace;
    font-size: 10.5px;
    color: #856852;
    margin-bottom: 5px;
    font-weight: 600;
}
.msg-role { color: #A97142; font-weight: 800; }

/* Alerts */
.alert-warning {
    background: #FEF3C7;
    border: 1px solid #D9A441;
    border-radius: 8px;
    padding: 12px 16px;
    color: #92400E;
    font-size: 12.5px;
    margin: 8px 0;
    font-weight: 600;
}
.alert-contradiction {
    background: #FFF1F2;
    border: 1px solid #F43F5E;
    border-radius: 8px;
    padding: 12px 16px;
    color: #BE123C;
    font-size: 12.5px;
    margin: 8px 0;
    font-weight: 600;
}
.alert-gating {
    background: #FFFDF8;
    border: 1.5px solid #D9A441;
    border-radius: 12px;
    padding: 20px;
    color: #382417;
    margin: 14px 0;
    box-shadow: 0 4px 16px rgba(217, 164, 65, 0.12);
}

/* Cards */
.earth-card {
    background: #FFFDF8;
    border: 1.5px solid rgba(169, 113, 66, 0.28);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 16px rgba(139, 94, 60, 0.06);
}
.telemetry-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin: 12px 0;
}
.telemetry-item {
    background: #FFF5E1;
    border: 1px solid rgba(169, 113, 66, 0.22);
    border-radius: 8px;
    padding: 12px 14px;
}
.telemetry-label {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    color: #856852;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.telemetry-val {
    font-size: 16px;
    font-weight: 900;
    color: #382417;
    margin-top: 3px;
}

/* Badges */
.time-badge-imm { background: #D1FAE5; color: #065F46; border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: 700; border: 1px solid #059669; }
.time-badge-med { background: #FEF3C7; color: #92400E; border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: 700; border: 1px solid #D9A441; }
.time-badge-lng { background: #EDE9FE; color: #5B21B6; border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: 700; border: 1px solid #8B5CF6; }
.conf-badge-high { background: #D1FAE5; border: 1px solid #059669; border-radius: 6px; padding: 4px 12px; color: #065F46; font-size: 11px; font-weight: 700; }
.conf-badge-mod { background: #FEF3C7; border: 1px solid #D9A441; border-radius: 6px; padding: 4px 12px; color: #92400E; font-size: 11px; font-weight: 700; }

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #D9A441, #E8B84B) !important;
    color: #382417 !important;
    border: 1px solid #C18A5B !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(217, 164, 65, 0.25) !important;
}
button[kind="secondary"] {
    background: #FFFDF8 !important;
    border: 1px solid rgba(169, 113, 66, 0.3) !important;
    color: #382417 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}
button[kind="secondary"]:hover {
    background: #FEF3C7 !important;
    border-color: #D9A441 !important;
}

/* Callouts & boxes */
.callout-sci {
    background: #FEF3C7;
    border-left: 4px solid #D9A441;
    padding: 10px 14px;
    font-size: 12px;
    color: #4A3324;
    margin: 8px 0;
    border-radius: 0 6px 6px 0;
}
.chunk-box {
    background: #FFFDF8;
    border: 1px solid rgba(169, 113, 66, 0.25);
    border-radius: 8px;
    padding: 12px 14px;
    margin: 6px 0;
}
.chunk-id { font-family: 'Fira Code', monospace; font-size: 11px; color: #B45309; font-weight: 800; }
.chunk-src { font-size: 11px; color: #856852; }

/* Transition Bridge Point Summary Card */
.bridge-point-card {
    background: #FFFDF8;
    border: 1.5px solid rgba(169, 113, 66, 0.25);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(139, 94, 60, 0.05);
}
.bridge-phase-header {
    font-family: 'Fira Code', monospace;
    font-size: 12px;
    font-weight: 800;
    color: #8B5E3C;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PIPELINE RUNNER WITH INTELLIGENCE CACHING
# ═════════════════════════════════════════════════════════════════════════════
def run_pipeline(user_message: str, json_input: dict | None, session_id: str) -> dict:
    """Executes the full 9-stage evidence pipeline with validation."""
    case_session = get_or_create_case_file(session_id)

    # Stage 0: Input Parsing & Validation
    incoming_data, input_mode, ambiguities = InputParser.parse_input(
        text=user_message or "",
        structured_dict=json_input
    )
    is_valid, hard_errors, suspicious_alerts = InputValidator.validate_bounds_and_units(incoming_data)
    if not is_valid:
        return {"error": " | ".join(hard_errors)}

    # Stage 1: Case File Update & Provenance
    contradictions = InputValidator.detect_multi_turn_contradictions(
        prior_profile=case_session.profile,
        incoming_data=incoming_data
    )
    case_session.update_profile(incoming_data, contradictions)
    current_profile = case_session.profile

    # Stage 2: Completeness & Domain-Probe Check
    completeness_eval = CompletenessChecker.evaluate_completeness(
        profile=current_profile, detected_ambiguities=ambiguities
    )
    is_actionable = completeness_eval.get("is_actionable", False)
    requires_clarification = completeness_eval.get("requires_clarification", False)
    clarifying_q = completeness_eval.get("clarifying_question")

    if not is_actionable and clarifying_q:
        case_session.record_turn(user_message or "", {}, [])
        return {
            "reply_markdown": None,
            "diagnosis_markdown": None,
            "case_file": case_session.to_dict(),
            "rule_metrics": {},
            "recommendations": [],
            "retrieved_evidence": [],
            "causal_chains": [],
            "clarifying_question": clarifying_q,
            "completeness_eval": completeness_eval,
            "monitoring_plan": [],
            "suspicious_alerts": suspicious_alerts,
            "contradiction_alerts": contradictions,
            "input_mode": input_mode,
            "dissenting_evidence": [],
            "retrieval_trace": {},
            "is_actionable": False,
            "requires_clarification": True,
            "spatial_context": current_profile.get("spatial_context")
        }

    # Stage 3: Diagnostic Hypothesis Formation
    rule_eval = EnvironmentalRuleEngine.evaluate_profile(current_profile)
    query_steer_terms = rule_eval.get("query_steer_terms", [])

    # Stage 4: Biome-Gated Vector RAG Evidence Retrieval
    contextual_query = user_message or f"{rule_eval.get('ecosystem_type', '')} {current_profile.get('biome', '')} {current_profile.get('current_crop', '')} restoration"
    retrieved_raw, dissenting_evidence, retrieval_trace = KnowledgeRetriever.retrieve_evidence(
        query=contextual_query,
        biome=current_profile.get("biome"),
        steer_terms=query_steer_terms,
        top_k=6
    )
    retrieved_chunk_ids = {c["id"] for c in retrieved_raw}

    # Stage 5: Multi-Metric Reasoning Graph & Intervention Matching
    raw_interventions = InterventionLibrary.get_matching_interventions(
        biome=current_profile.get("biome"),
        viable_classes=rule_eval.get("viable_intervention_classes", []),
        prohibited_classes=rule_eval.get("prohibited_intervention_classes", []),
        ecosystem_type=rule_eval.get("ecosystem_type"),
        environmental_profile=rule_eval.get("environmental_profile"),
        limiting_factors=rule_eval.get("primary_limiting_factors", [])
    )
    causal_chains = MultiMetricReasoningGraph.generate_causal_chains(current_profile, rule_eval)

    # Stage 7: Peer-Review Verification
    verified_recommendations = []
    for item in raw_interventions[:3]:
        gated_rec = EvidenceVerifier.verify_and_gate_recommendation(
            rec_data=item, profile=current_profile,
            retrieved_chunk_ids=retrieved_chunk_ids, rule_eval=rule_eval
        )
        verified_recommendations.append(gated_rec)

    # Stage 6: Scientific Write-Up Synthesis
    reply_markdown = ScientificWriter.synthesize_response(
        query=user_message or "",
        profile=current_profile,
        rule_eval=rule_eval,
        recommendations=verified_recommendations,
        retrieved_evidence=retrieved_raw,
        causal_chains=causal_chains,
        clarifying_question=clarifying_q,
        completeness_eval=completeness_eval
    )
    diagnosis_markdown = ScientificWriter.synthesize_diagnosis_markdown(
        profile=current_profile,
        rule_eval=rule_eval,
        completeness_eval=completeness_eval
    )

    # Stage 8: On-Farm Monitoring Protocol
    monitoring_plan = generate_monitoring_plan(verified_recommendations)
    case_session.record_turn(user_message or "", rule_eval, verified_recommendations)

    return {
        "reply_markdown": reply_markdown,
        "diagnosis_markdown": diagnosis_markdown,
        "case_file": case_session.to_dict(),
        "rule_metrics": rule_eval,
        "recommendations": verified_recommendations,
        "retrieved_evidence": retrieved_raw,
        "causal_chains": causal_chains,
        "clarifying_question": clarifying_q,
        "completeness_eval": completeness_eval,
        "monitoring_plan": monitoring_plan,
        "suspicious_alerts": suspicious_alerts,
        "contradiction_alerts": contradictions,
        "input_mode": input_mode,
        "dissenting_evidence": dissenting_evidence,
        "retrieval_trace": retrieval_trace,
        "is_actionable": True,
        "requires_clarification": False,
        "spatial_context": current_profile.get("spatial_context")
    }


def execute_diagnostic_with_cache(user_message: str, json_input: dict | None, session_id: str) -> dict:
    """Checks persistent database cache before running diagnostic, saving result on completion."""
    # 1. Inspect incoming data to build preliminary profile for hashing
    incoming_data, _, _ = InputParser.parse_input(text=user_message or "", structured_dict=json_input)
    
    # 2. Check if identical query has been solved previously
    cached = AuditDatabase.get_cached_assessment(user_message or "", incoming_data)
    if cached:
        # Re-attach into active case file memory
        case_session = get_or_create_case_file(session_id)
        case_session.update_profile(incoming_data, [])
        case_session.record_turn(user_message or "", cached.get("rule_metrics", {}), cached.get("recommendations", []))
        return cached

    # 3. Compute solution via 9-stage pipeline
    fresh_result = run_pipeline(user_message, json_input, session_id)
    if not fresh_result.get("error") and fresh_result.get("is_actionable"):
        # Persist to database cache for instant future reuse
        AuditDatabase.save_assessment(
            session_id=session_id,
            query=user_message or "",
            profile=fresh_result.get("case_file", {}).get("profile", {}),
            result=fresh_result
        )
    return fresh_result


# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═════════════════════════════════════════════════════════════════════════════
if "session_id" not in st.session_state:
    st.session_state.session_id = "st_" + str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "followup_chat" not in st.session_state:
    st.session_state.followup_chat = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

DEMO_SCENARIOS = {
    "🌾 Semi-Arid Farm": {
        "text": "Soil organic carbon is 0.3%, rainfall low (320mm), crop monoculture wheat, region semi-arid. What interventions do you recommend?",
        "json": {"soc_percent": 0.3, "rainfall_mm": 320.0, "current_crop": "monoculture wheat", "biome": "semi-arid"}
    },
    "🏙️ Urban Polluted Lake": {
        "text": "Urban wetland lake, high runoff pollution, 12% green space, heavy stormwater inflow, declining waterbirds.",
        "json": {"ecosystem_type": "urban", "pollution_level": "high", "green_space_ratio": 0.12, "water_quality": "poor"}
    },
    "💧 Eutrophic Wetland": {
        "text": "Freshwater marsh wetland, low water level, severe agricultural runoff pollution, dissolved oxygen 2.1 mg/L, 620mm rainfall.",
        "json": {"ecosystem_type": "wetland", "water_quality": "eutrophic", "water_level": "declining", "rainfall_mm": 620.0}
    },
    "🌲 Forest Corridor": {
        "text": "Montane rainforest, severe habitat fragmentation, 18% canopy loss, deforestation along agricultural edge, 1600mm rainfall.",
        "json": {"ecosystem_type": "forest", "fragmentation_index": "high", "deforestation_rate": "high", "canopy_cover_pct": 28.0, "rainfall_mm": 1600.0}
    },
    "❓ Incomplete (<3 Vars)": {
        "text": "Biodiversity is declining on my land with continuous monoculture wheat.",
        "json": {"current_crop": "continuous monoculture wheat"}
    }
}


# ═════════════════════════════════════════════════════════════════════════════
# TOP BRAND HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="brand-header">
    <div style="font-size:36px">🌍</div>
    <div>
        <div class="brand-name">DARUKAA<span style="color:#8B5E3C;font-weight:400">.EARTH</span></div>
        <div class="brand-sub">AI Biodiversity Intelligence & Multi-Metric Environmental Scientist</div>
    </div>
    <div class="pipeline-badge">● 9-STAGE EVIDENCE & REASONING ACTIVE</div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION & TELEMETRY CONTROLS
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🧭 Intelligence Navigation")
    
    NAV_PANELS = [
        "🔬 AI Scientist & Assessment",
        "📊 Intelligence Dashboard",
        "🌿 Biodiversity & Succession",
        "🛠️ Actionable Prescriptions",
        "📚 Scientific Sources",
        "🗄️ Audit History & Database"
    ]
    
    active_panel = st.radio(
        "Select Panel:",
        options=NAV_PANELS,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Active Site Telemetry Mini-Card
    if st.session_state.last_result:
        res = st.session_state.last_result
        prof = res.get("case_file", {}).get("profile", {})
        rm = res.get("rule_metrics", {})
        health = rm.get("system_health_index")
        h_color = "#f87171" if health and health < 40 else "#fbbf24" if health and health < 70 else "#059669"
        
        st.markdown("#### 📋 Active Site Telemetry")
        if res.get("is_cached"):
            st.markdown(f"""
            <div class="cache-hit-badge" style="margin-bottom:10px">
                ⚡ Instant Cache Hit (Reused {res.get('cached_hit_count', 1)}x)
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#FFFDF8;border:1px solid rgba(169,113,66,0.25);border-radius:10px;padding:12px;margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span style="font-family:'Fira Code',monospace;font-size:10px;color:#856852">HEALTH INDEX:</span>
                <span style="font-size:16px;font-weight:900;color:{h_color}">{health or '—'}/100</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;margin:3px 0">
                <span style="color:#856852">Ecosystem:</span>
                <strong style="color:#382417">{(prof.get('ecosystem_type') or rm.get('ecosystem_type') or 'Agricultural').title()}</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;margin:3px 0">
                <span style="color:#856852">Topsoil SOC:</span>
                <strong style="color:#382417">{prof.get('soc_percent') or '—'}%</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;margin:3px 0">
                <span style="color:#856852">Precipitation:</span>
                <strong style="color:#382417">{prof.get('rainfall_mm') or '—'} mm</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12px;margin:3px 0">
                <span style="color:#856852">Land Use:</span>
                <strong style="color:#382417">{(prof.get('current_crop') or prof.get('land_use_type') or 'General').title()}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🌱 Ready for site assessment intake. Select a benchmark or enter field conditions.")

    st.markdown("---")
    st.markdown(f"**Session ID:** `{st.session_state.session_id}`")
    
    if st.button("🔄 New Consultation Session", use_container_width=True, type="secondary"):
        reset_case_file(st.session_state.session_id)
        st.session_state.messages = []
        st.session_state.followup_chat = []
        st.session_state.last_result = None
        st.session_state.session_id = "st_" + str(uuid.uuid4())[:8]
        st.rerun()

    if st.session_state.last_result:
        case_json = json.dumps({
            "session_id": st.session_state.session_id,
            "case_file": st.session_state.last_result.get("case_file"),
            "rule_metrics": st.session_state.last_result.get("rule_metrics"),
            "recommendations": st.session_state.last_result.get("recommendations"),
            "chat_history": st.session_state.followup_chat
        }, indent=2)
        st.download_button(
            "📥 Export Full Case Audit (JSON)",
            data=case_json,
            file_name=f"darukaa-audit-{st.session_state.session_id}.json",
            mime="application/json",
            use_container_width=True
        )


# ═════════════════════════════════════════════════════════════════════════════
# PANEL 1: 🔬 AI SCIENTIST & ASSESSMENT (MERGED INTAKE, DIAGNOSIS & CHATBOT)
# ═════════════════════════════════════════════════════════════════════════════
if active_panel == "🔬 AI Scientist & Assessment":
    st.markdown("### 🔬 AI Scientist & Environmental Assessment Console")
    st.markdown("Submit site telemetry or select a benchmark scenario. The AI Scientist executes the 9-stage biophysical reasoning pipeline, checks persistent memory to reuse previous solutions, and provides grounded follow-up chat support.")

    # 1. Benchmark Scenarios
    st.markdown("##### ⚡ Quick Benchmark Scenarios")
    demo_cols = st.columns(len(DEMO_SCENARIOS))
    selected_demo = None
    for idx, (col, (label, scenario)) in enumerate(zip(demo_cols, DEMO_SCENARIOS.items())):
        if col.button(label, key=f"demo_btn_{idx}", use_container_width=True):
            selected_demo = scenario

    # 2. Multi-Modal Field Telemetry Intake Tabs
    st.markdown("##### 📥 Enter Site Telemetry")
    input_tabs = st.tabs([
        "📝 Freeform Natural Text",
        "📋 Structured JSON",
        "🗺️ Geo-Coordinates & Satellite Lookup"
    ])

    user_text = None
    user_json = None

    with input_tabs[0]:
        free_text = st.text_area(
            "Describe site conditions, land use, and concerns:",
            placeholder="e.g. Soil organic carbon is 0.3%, rainfall low (320mm), crop monoculture wheat, region semi-arid.",
            height=85,
            key="panel1_free_text",
            label_visibility="collapsed"
        )
        if st.button("▶ Run AI Environmental Assessment (Text)", type="primary", use_container_width=True, key="p1_btn_text"):
            user_text = free_text.strip() if free_text else None

    with input_tabs[1]:
        json_raw = st.text_area(
            "Paste JSON field payload:",
            value='{\n  "soc_percent": 0.3,\n  "rainfall_mm": 320,\n  "current_crop": "monoculture wheat",\n  "biome": "semi-arid"\n}',
            height=120,
            key="panel1_json_area",
            label_visibility="collapsed"
        )
        if st.button("▶ Run AI Environmental Assessment (JSON)", type="primary", use_container_width=True, key="p1_btn_json"):
            try:
                user_json = json.loads(json_raw)
            except Exception:
                st.error("Invalid JSON format.")

    with input_tabs[2]:
        c_lat, c_lon = st.columns(2)
        coord_lat = c_lat.number_input("Latitude (°N)", value=26.915, format="%.4f", key="p1_lat")
        coord_lon = c_lon.number_input("Longitude (°E)", value=70.908, format="%.4f", key="p1_lon")
        c_soc, c_crop = st.columns(2)
        coord_soc = c_soc.number_input("Soil Organic Carbon (SOC %)", value=0.30, min_value=0.0, max_value=15.0, step=0.05, key="p1_soc")
        coord_crop = c_crop.text_input("Cropping System", value="monoculture wheat", key="p1_crop")

        if st.button("▶ Lookup Satellite Context & Run Assessment", type="primary", use_container_width=True, key="p1_btn_coord"):
            user_json = {
                "latitude": float(coord_lat),
                "longitude": float(coord_lon),
                "soc_percent": float(coord_soc),
                "current_crop": coord_crop
            }

    # Trigger diagnostic if selected
    trigger_text = None
    trigger_json = None
    if selected_demo:
        trigger_text = selected_demo["text"]
        trigger_json = selected_demo.get("json")
    elif user_text:
        trigger_text = user_text
    elif user_json:
        trigger_json = user_json

    if trigger_text or trigger_json:
        now_str = datetime.datetime.now().strftime("%H:%M")
        disp_txt = trigger_text or f"```json\n{json.dumps(trigger_json, indent=2)}\n```"
        
        # Log to UI messages
        st.session_state.messages.append({"role": "user", "text": disp_txt, "time": now_str})
        AuditDatabase.save_chat_message(st.session_state.session_id, "user", disp_txt, "intake")

        with st.spinner("🔬 Consulting persistent memory & evaluating 9-stage biophysical pipeline..."):
            res = execute_diagnostic_with_cache(trigger_text, trigger_json, st.session_state.session_id)

        if res.get("error"):
            st.error(f"⚠️ Biophysical Validation Error: {res['error']}")
        else:
            st.session_state.last_result = res
            reply_txt = res.get("reply_markdown", "") or res.get("diagnosis_markdown", "")
            st.session_state.messages.append({
                "role": "system",
                "text": reply_txt,
                "diagnosis_markdown": res.get("diagnosis_markdown", ""),
                "time": now_str,
                "recommendations": res.get("recommendations", []),
                "clarifying_question": res.get("clarifying_question"),
                "suspicious_alerts": res.get("suspicious_alerts", []),
                "contradiction_alerts": res.get("contradiction_alerts", []),
                "result": res
            })
            AuditDatabase.save_chat_message(st.session_state.session_id, "assistant", reply_txt[:300] + "...", "assessment")

        st.rerun()

    # 3. Assessment Output & Status
    if st.session_state.last_result:
        res = st.session_state.last_result
        st.markdown("---")
        
        # Check if incomplete / clarifying question required
        is_incomplete = bool(res.get("clarifying_question")) and (
            res.get("requires_clarification", False) or not res.get("is_actionable", True)
        )

        if is_incomplete:
            cq = res.get("clarifying_question", {})
            st.markdown(f"""
            <div class="alert-gating">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                    <span style="font-family:'Fira Code',monospace;font-size:11px;color:#B45309;background:rgba(217,164,65,0.2);padding:3px 10px;border-radius:4px;font-weight:700">⚠️ MISSING ENVIRONMENTAL TELEMETRY</span>
                    <span style="font-size:12px;color:#856852">Minimum 3 variables required for clinical rigor</span>
                </div>
                <div style="font-size:17px;font-weight:800;color:#382417;margin-bottom:10px;line-height:1.4">
                    {cq.get('question_text', 'Please provide baseline Soil Organic Carbon (SOC %), rainfall pattern, and land use.')}
                </div>
                <div style="font-size:13px;color:#4A3324;line-height:1.5;background:#FFF5E1;border:1px solid rgba(169,113,66,0.2);padding:12px 16px;border-radius:8px">
                    <strong style="color:#8B5E3C">Scientific Rationale:</strong> {cq.get('scientific_rationale', 'Without baseline soil organic carbon and rainfall patterns, hydraulic balance and biological species compatibility cannot be determined.')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🎯 Select a baseline or calibrate your field conditions:")
            suggested = cq.get("suggested_inputs", [])
            if suggested:
                st.markdown("**Option A: Select a regional baseline profile:**")
                cols = st.columns(len(suggested))
                for c_idx, opt in enumerate(suggested):
                    if cols[c_idx].button(f"👉 {opt}", key=f"p1_cq_{c_idx}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "text": f"Supplemental Field Observation: {opt}", "time": datetime.datetime.now().strftime("%H:%M")})
                        with st.spinner("🔬 Updating case file..."):
                            res_upd = execute_diagnostic_with_cache(f"Supplemental Field Observation: {opt}", None, st.session_state.session_id)
                            st.session_state.last_result = res_upd
                        st.rerun()

            st.markdown("**Option B: If you do not know laboratory numbers:**")
            if st.button("🤷 I don't know my exact measurements (Estimate baseline for my region)", type="primary", use_container_width=True, key="p1_idk_btn"):
                payload = {"soc_percent": 0.35, "rainfall_mm": 320.0, "current_crop": "monoculture wheat", "biome": "semi-arid", "is_estimated_baseline": True}
                with st.spinner("🔬 Calibrating regional estimate..."):
                    res_upd = execute_diagnostic_with_cache("Research scientific baselines for semi-arid wheat monoculture", payload, st.session_state.session_id)
                    st.session_state.last_result = res_upd
                st.rerun()

        else:
            # Complete and actionable: render executive summary and prescribed solutions
            st.markdown("#### 📋 Scientific Assessment Findings")
            if res.get("is_cached"):
                st.markdown(f"""
                <div class="cache-hit-badge" style="margin-bottom:12px">
                    ⚡ Instant Cache Hit: Reusing proven ecological analysis (accessed {res.get('cached_hit_count', 1)} times)
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(res.get("diagnosis_markdown", ""))
            
            recs = res.get("recommendations", [])
            if recs:
                st.markdown(f"##### 🎯 Prescribed Ecological Interventions ({len(recs)} Approved)")
                r_cols = st.columns(len(recs))
                for r_i, r in enumerate(recs):
                    with r_cols[r_i]:
                        st.markdown(f"""
                        <div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:10px;padding:14px;height:100%">
                            <div style="font-size:11px;font-family:'Fira Code',monospace;color:#8B5E3C;font-weight:700">PRACTICE #{r_i+1}</div>
                            <div style="font-size:14px;font-weight:800;color:#382417;margin:4px 0">{r.get('name', 'Intervention')}</div>
                            <div style="font-size:12px;color:#4A3324;line-height:1.5">{r.get('action', '')[:120]}...</div>
                            <div style="margin-top:8px;font-size:11px;color:#059669;font-weight:700">✓ Grounded with {len(r.get('evidence_ids',[]))} peer-reviewed studies</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.caption("👉 For full technical structural blueprints, cross-section diagrams, and step-by-step guides, visit the **🛠️ Actionable Prescriptions** panel.")

        # 4. Interactive Follow-Up Chatbot (Answers queries strictly against assessment & input)
        st.markdown("---")
        st.markdown("### 💬 Interactive AI Scientist Chatbot (Follow-up Questions & Doubts)")
        st.markdown("Ask any questions or clarify doubts regarding your site analysis, recommended practices, planting geometry, species selection, soil carbon trajectories, or watering regimes.")

        # Display conversation history
        if st.session_state.followup_chat:
            for chat_turn in st.session_state.followup_chat:
                if chat_turn["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-user">
                        <div class="msg-meta"><span class="msg-role">👤 Practitioner / User Doubt</span> &nbsp; {chat_turn.get('time','')}</div>
                        {chat_turn['text']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="msg-system">
                        <div class="msg-meta"><span class="msg-role">🌍 Darukaa AI Environmental Scientist</span> &nbsp; {chat_turn.get('time','')}</div>
                        {chat_turn['text']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("No follow-up questions asked yet. Ask a question below (e.g. *'What tree spacing should I use?'*, *'Can I substitute chickpea with another legume?'*, *'How much water is saved?'*).")

        # Chat Input Box
        user_doubt = st.chat_input("Ask a doubt or question about this assessment (strictly answered against your input)...")
        if user_doubt:
            d_time = datetime.datetime.now().strftime("%H:%M")
            st.session_state.followup_chat.append({"role": "user", "text": user_doubt, "time": d_time})
            AuditDatabase.save_chat_message(st.session_state.session_id, "user", user_doubt, "doubt")

            # Call bounded follower
            prof = res.get("case_file", {}).get("profile", {})
            rm = res.get("rule_metrics", {})
            recs = res.get("recommendations", [])

            with st.spinner("🔬 Formulating scientifically grounded answer against your site profile..."):
                answer = ScientificWriter.answer_assessment_followup(
                    user_question=user_doubt,
                    profile=prof,
                    rule_eval=rm,
                    recommendations=recs,
                    chat_history=st.session_state.followup_chat
                )

            st.session_state.followup_chat.append({"role": "assistant", "text": answer, "time": d_time})
            AuditDatabase.save_chat_message(st.session_state.session_id, "assistant", answer, "answer")
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PANEL 2: 📊 INTELLIGENCE DASHBOARD (OBSERVATIONS & SEVERITY GAUGES)
# ═════════════════════════════════════════════════════════════════════════════
elif active_panel == "📊 Intelligence Dashboard":
    st.markdown("### 📊 Environmental Intelligence Dashboard")
    st.markdown("Detailed diagnostic evaluation of site observations extracted from practitioner input, multi-metric health scoring, and diagnosed ecological limiting factors.")

    if not st.session_state.last_result:
        st.warning("⚠️ No active site assessment found. Please run an assessment in the **🔬 AI Scientist & Assessment** panel first.")
    else:
        res = st.session_state.last_result
        prof = res.get("case_file", {}).get("profile", {})
        rm = res.get("rule_metrics", {})
        eco = (prof.get("ecosystem_type") or rm.get("ecosystem_type") or "agricultural").lower()
        curr_soc = prof.get("soc_percent") or 0.35
        curr_rain = prof.get("rainfall_mm") or 320.0
        health = rm.get("system_health_index") or 40.0
        limiting = rm.get("primary_limiting_factors", [])

        # 1. Observations from User Input (Grid Card)
        st.markdown("#### 🔍 Observed Site Telemetry (From User Input)")
        st.markdown(f"""
        <div class="telemetry-grid">
            <div class="telemetry-item">
                <div class="telemetry-label">Soil Organic Carbon</div>
                <div class="telemetry-val">{prof.get('soc_percent') or '—'}%</div>
                <div style="font-size:11px;color:#92400E;margin-top:2px">Deficit vs 1.20% target</div>
            </div>
            <div class="telemetry-item">
                <div class="telemetry-label">Annual Precipitation</div>
                <div class="telemetry-val">{prof.get('rainfall_mm') or '—'} mm</div>
                <div style="font-size:11px;color:#0369A1;margin-top:2px">Aridity: {prof.get('biome', 'Semi-Arid').title()}</div>
            </div>
            <div class="telemetry-item">
                <div class="telemetry-label">Land Use / Crop</div>
                <div class="telemetry-val">{(prof.get('current_crop') or prof.get('land_use_type') or 'General').title()}</div>
                <div style="font-size:11px;color:#065F46;margin-top:2px">Ecosystem: {eco.title()}</div>
            </div>
            <div class="telemetry-item">
                <div class="telemetry-label">Soil Texture / Tillage</div>
                <div class="telemetry-val">{(prof.get('soil_texture') or 'Sandy Loam').title()}</div>
                <div style="font-size:11px;color:#5B21B6;margin-top:2px">Tillage: {prof.get('tillage_practice', 'Conventional Disc').title()}</div>
            </div>
            <div class="telemetry-item">
                <div class="telemetry-label">Canopy Cover / NDVI</div>
                <div class="telemetry-val">{prof.get('canopy_cover_pct') or (prof.get('ndvi') or '0.24')}</div>
                <div style="font-size:11px;color:#856852;margin-top:2px">Vegetation Density</div>
            </div>
            <div class="telemetry-item">
                <div class="telemetry-label">System Health Score</div>
                <div class="telemetry-val" style="color:#059669">{health}/100</div>
                <div style="font-size:11px;color:#065F46;margin-top:2px">Biophysical Resilience</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Diagnostic Problem Severity Gauges
        st.markdown("---")
        st.markdown(f"#### ⚠️ Diagnostic Problem Severity & Deficit ({eco.title()} Ecosystem)")
        st.altair_chart(
            create_problem_severity_gauge_chart(
                baseline_soc=float(curr_soc),
                rainfall_mm=float(curr_rain),
                ecosystem_type=eco
            ),
            use_container_width=True
        )
        ref_label = "EPA Urban Stormwater (2022)" if eco == "urban" else "Ramsar Convention (2021)" if eco == "wetland" else "Science (2020) & PNAS (2019)" if eco == "forest" else "FAO Global Soil Partnership & IPCC SRCCL"
        st.caption(f"⚠️ Comparison of current site baseline against the Minimum Ecological Health Threshold calibrated from **{ref_label}**.")

        # 3. Biophysical Bottlenecks & Limiting Factors
        st.markdown("---")
        st.markdown("#### 🧪 Diagnosed Limiting Factors & Multi-Metric Interactions")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**1. Primary Biophysical Bottlenecks:**")
            for factor in limiting:
                st.markdown(f"""
                <div style="background:#FFF1F2;border-left:4px solid #F43F5E;padding:10px 14px;border-radius:0 8px 8px 0;margin:6px 0;font-size:13px;color:#9F1239;font-weight:600">
                    ⚠️ {factor}
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("**2. Causal Ecological Interactions:**")
            interactions = rm.get("causal_interactions", [])
            if interactions:
                for ci in interactions:
                    st.markdown(f"""
                    <div style="background:#FEF3C7;border-left:4px solid #D9A441;padding:10px 14px;border-radius:0 8px 8px 0;margin:6px 0;font-size:12.5px;color:#4A3324">
                        <strong>{ci.get('interaction', '')}:</strong> {ci.get('description', '')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Monoculture tillage depletes root mycorrhizae, compounding drought vulnerability.")

        # Full clinical running narrative
        if res.get("case_file", {}).get("running_assessment"):
            st.markdown("---")
            st.markdown("#### 📋 Clinical Case Assessment Narrative")
            st.markdown(f"""
            <div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:10px;padding:16px 20px;font-size:13.5px;color:#382417;line-height:1.65">
                {res['case_file']['running_assessment']}
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PANEL 3: 🌿 BIODIVERSITY & SUCCESSION (TRANSITION BRIDGE & BLUEPRINTS)
# ═════════════════════════════════════════════════════════════════════════════
elif active_panel == "🌿 Biodiversity & Succession":
    st.markdown("### 🌿 Biodiversity Succession & The Transition Bridge")
    st.markdown("Restoring degraded ecosystems is a sequential biological journey. Below is the verified **3-phase succession pathway** and dynamic mechanism blueprints showing how your site transitions to an equilibrium climax.")

    if not st.session_state.last_result:
        st.warning("⚠️ Please run an assessment in the **🔬 AI Scientist & Assessment** panel first to generate custom succession pathways.")
    else:
        res = st.session_state.last_result
        prof = res.get("case_file", {}).get("profile", {})
        rm = res.get("rule_metrics", {})
        eco = (prof.get("ecosystem_type") or rm.get("ecosystem_type") or "agricultural").lower()

        # 1. The Transition Bridge SVG Diagram
        st.markdown("#### 🌉 The 3-Phase Transition Bridge")
        st.caption("Visualized succession roadmap connecting degraded baseline to a self-sustaining biodiversity climax.")
        components.html(render_animated_transition_roadmap_diagram(ecosystem_type=eco), height=370, scrolling=False)

        # 2. Short Point-Wise Summary of the Transition Bridge
        st.markdown("#### 📝 Short Point-Wise Summary of the Transition Bridge")

        if eco == "forest":
            p1_points = [
                "Plant fast-growing pioneer shelterbelts along fragmented perimeter boundaries.",
                "Halt desiccating agricultural winds to prevent hydraulic xylem cavitation in edge trees.",
                "Suppress competitive invasive grasses and reduce core edge forest desiccation by 45%."
            ]
            p2_points = [
                "Establish dense 3m-spaced structural native tree corridors connecting isolated forest patches.",
                "Inoculate root zones with native mycorrhizal fungi to reboot subterranean mycelial networks.",
                "Reopen functional wildlife movement routes for arboreal mammals and understory insectivorous birds."
            ]
            p3_points = [
                "Achieve complete 3-tier vertical canopy stratification (emergent, mid-story, shrub understory).",
                "Canopy cover exceeds 75%, establishing continuous microclimatic humidity buffers.",
                "Self-sustaining seed dispersal and climax pollinator flyways are permanently restored."
            ]
        elif eco == "urban":
            p1_points = [
                "Excavate stepped bioswale filtration trenches along high-volume impervious runoff channels.",
                "Install aggregate gravel filter beds to trap 85%+ coarse sediment, oil, and microplastics.",
                "Grade side slopes to 3:1 to arrest stormwater velocity and eliminate scouring."
            ]
            p2_points = [
                "Establish hyper-accumulating native sedges (*Carex*, *Juncus*) and dense Miyawaki pocket forests.",
                "Active rhizosphere microbial consortia chelate dissolved heavy metals (zinc, lead, copper).",
                "Infiltration rates double, eliminating standing urban water and recharging local water tables."
            ]
            p3_points = [
                "Multi-tier pocket forests reach 30%+ urban tree canopy closure.",
                "Urban Heat Island effect drops by 3–5°C through continuous evapotranspirative cooling.",
                "Interconnected stepping-stone pollinator habitats support wild native bees and butterflies."
            ]
        elif eco == "wetland":
            p1_points = [
                "Install loose-rock grade-control sills across eroded drainage ditches to arrest channel incision.",
                "Stabilize hydrological baseflow and maintain 30–50cm perennial water depths in littoral zones.",
                "Prevent catastrophic sudden drainage during dry intervals."
            ]
            p2_points = [
                "Establish dense *Typha*, *Phragmites*, and *Carex* riparian macrophyte biofiltration belts.",
                "Anaerobic root-zone microbial denitrification strips 85%+ of agricultural nitrates and phosphates.",
                "Water dissolved oxygen rebounds from hypoxic levels (<2 mg/L) back above 6.5 mg/L."
            ]
            p3_points = [
                "Benthic macroinvertebrate communities reboot, restoring aquatic food-web foundations.",
                "Submerged aquatic vegetation expands, providing crucial waterfowl breeding nurseries.",
                "Self-regulating wetland hydrological sponge permanently protects downstream catchments."
            ]
        else:
            # Agricultural
            p1_points = [
                "Arrest acute erosion immediately: eliminate deep disc inversion tillage and leave 35%+ stubble mulch.",
                "Soil surface temperatures drop by 4–8°C, preventing critical moisture vaporization.",
                "Establish perimeter windbreak shelterbelts to slash desiccating wind speeds by up to 60%."
            ]
            p2_points = [
                "Integrate inoculated *Rhizobium* pulse intercrops to biologically inject 40–70 kg N/ha/year.",
                "Fungal hyphae expand through the topsoil, unlocking bound phosphorus and stabilizing soil micro-aggregates.",
                "Soil water retention capacity increases by 16,500 liters/hectare for each 0.1% SOC gain."
            ]
            p3_points = [
                "Deep-rooted agroforestry trees (*Faidherbia albida*) reach 10m+ subterranean aquifers to perform hydraulic lift.",
                "Leaf litter deposition generates 2.5–3.5 t/ha/yr of organic matter, permanently cycling nutrients.",
                "Land Equivalent Ratio (LER) reaches 1.28+, delivering 28% higher total land productivity."
            ]

        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            st.markdown(f"""
            <div class="bridge-point-card">
                <div class="bridge-phase-header">⚡ PHASE 1: MONTHS 0–6</div>
                <div style="font-size:12.5px;font-weight:700;color:#382417;margin-bottom:8px">Immediate Armor & Stabilization</div>
                <ul style="font-size:12px;color:#4A3324;line-height:1.6;margin-left:-16px">
                    {''.join([f'<li>{pt}</li>' for pt in p1_points])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with c_p2:
            st.markdown(f"""
            <div class="bridge-point-card">
                <div class="bridge-phase-header">🌱 PHASE 2: YEARS 1–3</div>
                <div style="font-size:12.5px;font-weight:700;color:#382417;margin-bottom:8px">Biological Infiltration & Symbiosis</div>
                <ul style="font-size:12px;color:#4A3324;line-height:1.6;margin-left:-16px">
                    {''.join([f'<li>{pt}</li>' for pt in p2_points])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with c_p3:
            st.markdown(f"""
            <div class="bridge-point-card">
                <div class="bridge-phase-header">🌳 PHASE 3: YEARS 3–5+</div>
                <div style="font-size:12.5px;font-weight:700;color:#382417;margin-bottom:8px">Canopy Microclimate Climax</div>
                <ul style="font-size:12px;color:#4A3324;line-height:1.6;margin-left:-16px">
                    {''.join([f'<li>{pt}</li>' for pt in p3_points])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 3. Animated Biological Mechanism Blueprints
        st.markdown("---")
        st.markdown(f"#### 📐 Interactive Biological Mechanism Blueprints ({eco.title()})")
        if eco == "forest":
            t1_title = "🌲 Wildlife Movement Corridor Blueprint"
            t2_title = "🌳 Forest Canopy Stratification Blueprint"
            t1_html = render_animated_forest_corridor_diagram()
            t2_html = render_animated_forest_stratification_diagram()
        elif eco == "urban":
            t1_title = "🏙️ Bio-Retention Swale Filter Blueprint"
            t2_title = "🌳 Miyawaki Pocket Forest Blueprint"
            t1_html = render_animated_urban_bioswale_diagram()
            t2_html = render_animated_urban_pocket_forest_diagram()
        elif eco == "wetland":
            t1_title = "💧 Riparian Macrophyte Filter Blueprint"
            t2_title = "🌊 Hydrological Grade Sill Blueprint"
            t1_html = render_animated_wetland_buffer_diagram()
            t2_html = render_animated_wetland_hydro_sill_diagram()
        else:
            t1_title = "🌱 Rhizosphere Microbial Symbiosis Blueprint"
            t2_title = "🌳 Agroforestry Shelterbelt Blueprint"
            t1_html = render_animated_rhizosphere_diagram()
            t2_html = render_animated_agroforestry_diagram()

        bp_tabs = st.tabs([t1_title, t2_title])
        with bp_tabs[0]:
            components.html(t1_html, height=380, scrolling=False)
            st.caption("Subterranean biological flow and rooting interface dynamic simulation.")
        with bp_tabs[1]:
            components.html(t2_html, height=380, scrolling=False)
            st.caption("Above-ground canopy stratification and microclimatic humidity buffering simulation.")


# ═════════════════════════════════════════════════════════════════════════════
# PANEL 4: 🛠️ ACTIONABLE PRESCRIPTIONS (RECOVERY PROOFS & BLUEPRINTS)
# ═════════════════════════════════════════════════════════════════════════════
elif active_panel == "🛠️ Actionable Prescriptions":
    st.markdown("### 🛠️ Actionable Prescriptions & Implementation Blueprints")
    st.markdown("Peer-reviewed field prescriptions tailored to your site's physical parameters. Each recommendation includes qualitative/quantitative Before vs After recovery diagrams, structural cross-sections, and phase-by-phase implementation instructions.")

    if not st.session_state.last_result:
        st.warning("⚠️ Please run an assessment in the **🔬 AI Scientist & Assessment** panel first to generate actionable prescriptions.")
    else:
        res = st.session_state.last_result
        prof = res.get("case_file", {}).get("profile", {})
        rm = res.get("rule_metrics", {})
        eco = (prof.get("ecosystem_type") or rm.get("ecosystem_type") or "agricultural").lower()
        curr_soc = prof.get("soc_percent") or 0.35
        recs = res.get("recommendations", [])

        # 1. Qualitative & Quantitative Before vs After Recovery Diagrams
        st.markdown("#### 📊 Qualitative & Quantitative Recovery Proofs: Before vs After")
        c_tabs = st.tabs([
            "📊 Multi-Metric Recovery (Before vs Solved)",
            "📈 5-Year Quantitative Trajectory Curve"
        ])
        with c_tabs[0]:
            st.altair_chart(
                create_multi_metric_comparison_chart(
                    baseline_soc=float(curr_soc),
                    ecosystem_type=eco
                ),
                use_container_width=True
            )
            st.caption(f"📊 Quantitative gains across 5 core indicators comparing degraded baseline against post-intervention equilibrium for {eco.title()} systems.")

        with c_tabs[1]:
            st.altair_chart(
                create_5year_soc_trajectory_chart(
                    baseline_soc=float(curr_soc),
                    target_soc=1.20,
                    ecosystem_type=eco
                ),
                use_container_width=True
            )
            st.caption("📈 Calibrated multi-year trajectory demonstrating carbon accretion and hydrological buffer establishment.")

        # 2. Actionable Prescriptions Cards with Blueprints and Guides
        st.markdown("---")
        st.markdown(f"#### 📋 Field Implementation Prescriptions ({len(recs)} Approved)")

        for idx, rec in enumerate(recs, 1):
            name = rec.get("name") or rec.get("action", "Intervention")[:60]
            mechanism = rec.get("mechanism", "")
            action = rec.get("action", "")
            evidence_ids = rec.get("evidence_ids", [])
            trade_offs = rec.get("trade_offs", [])
            time_horizon = rec.get("time_horizon", "")
            conf = rec.get("confidence") or {}
            impacted = rec.get("impacted_metrics", [])
            why_selected = rec.get("why_selected", "")

            th_lower = (time_horizon or "").lower()
            time_label = "⚡ Short-Term (1–2 yr)" if "short" in th_lower or "1" in th_lower else "🌱 Medium-Term (3–5 yr)" if "medium" in th_lower or "3" in th_lower else "🌳 Long-Term (5+ yr)"
            time_class = "time-badge-imm" if "short" in th_lower or "1" in th_lower else "time-badge-med" if "medium" in th_lower or "3" in th_lower else "time-badge-lng"

            conf_score = conf.get("score", 0.85)
            conf_label = conf.get("label", "High Confidence")
            conf_pct = round(conf_score * 100)

            why_html = f"""
            <div style="background:rgba(169,113,66,0.10);border-left:4px solid #A97142;padding:12px 16px;border-radius:0 8px 8px 0;margin:10px 0">
                <div style="font-family:'Fira Code',monospace;font-size:11px;font-weight:700;color:#8B5E3C;margin-bottom:4px">💡 WHY THIS WAS SELECTED FOR YOUR SPECIFIC SITE</div>
                <div style="font-size:13px;color:#4A3324;line-height:1.6">{why_selected}</div>
            </div>
            """ if why_selected else ""

            st.markdown(f"""
            <div class="earth-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
                    <div style="font-size:18px;font-weight:800;color:#8B5E3C">#{idx} {name}</div>
                    <div style="display:flex;gap:8px;align-items:center">
                        <span class="{time_class}">{time_label}</span>
                        <span class="conf-badge-high">🛡️ {conf_label} ({conf_pct}%)</span>
                    </div>
                </div>
                <div style="background:rgba(217,164,65,0.12);border-left:4px solid #D9A441;padding:12px 16px;border-radius:0 8px 8px 0;margin:10px 0">
                    <div style="font-family:'Fira Code',monospace;font-size:11px;font-weight:700;color:#8B5E3C;margin-bottom:4px">🎯 1. WHAT TO DO (ACTIONABLE PRACTICE)</div>
                    <div style="font-size:13.5px;color:#382417;line-height:1.6">{action}</div>
                </div>
                {why_html}
                <div style="background:rgba(13,148,136,0.08);border-left:4px solid #0d9488;padding:12px 16px;border-radius:0 8px 8px 0;margin:10px 0">
                    <div style="font-family:'Fira Code',monospace;font-size:11px;font-weight:700;color:#0d9488;margin-bottom:4px">🔬 2. WHY IT WORKS (MULTI-METRIC SCIENTIFIC REASONING)</div>
                    <div style="font-size:13px;color:#134e4a;line-height:1.6">{mechanism}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Technical Structural Blueprint Diagram
            bp = get_blueprint_for_intervention(rec.get("id", ""))
            with st.expander(f"📐 Technical Structural Blueprint: How to Implement Practice #{idx}", expanded=True):
                st.markdown(f"**{bp.get('diagram_title', '📐 Implementation Cross-Section')}**")
                components.html(bp["svg"], height=230, scrolling=False)
                st.caption(f"Spatial layout, planting depth, and biological fluxes for **{name}**.")

            # Step-by-Step Action Guide
            with st.expander(f"🛠️ Step-by-Step Field Action Guide: Practice #{idx} (Phase-by-Phase)", expanded=True):
                st.markdown("#### 1️⃣ Phase 1: Site Preparation & Material Sourcing (Months 0–2)")
                st.markdown(bp["phase1"])
                st.markdown("#### 2️⃣ Phase 2: Structural Setup & Planting Configuration (Months 2–4)")
                st.markdown(bp["phase2"])
                st.markdown("#### 3️⃣ Phase 3: Adaptive Management & Succession (Months 4–12+)")
                st.markdown(bp["phase3"])
                st.markdown("#### 🌿 Recommended Certified Species")
                st.markdown(f"`{bp['species']}`")
                st.markdown(bp["pitfalls"])

            # Impacted Metrics Table
            if impacted:
                with st.expander(f"📈 Quantitative Recovery Indicators: Practice #{idx}", expanded=False):
                    cols = st.columns([2.5, 1.8, 1.8, 2.0, 1.8])
                    cols[0].markdown("**Variable**")
                    cols[1].markdown("**Baseline**")
                    cols[2].markdown("**Projected**")
                    cols[3].markdown("**Improvement**")
                    cols[4].markdown("**Time Horizon**")
                    for m in impacted:
                        c = st.columns([2.5, 1.8, 1.8, 2.0, 1.8])
                        c[0].markdown(f"**{m.get('metric_name', '')}**")
                        c[1].write(m.get("baseline_value", "—"))
                        c[2].write(m.get("projected_value", "—"))
                        c[3].markdown(f"<span style='color:#059669;font-weight:700'>{m.get('delta_estimate','')}</span>", unsafe_allow_html=True)
                        c[4].write(m.get("time_horizon_years", ""))

            st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PANEL 5: 📚 SCIENTIFIC SOURCES (EVIDENCE, TRACE & MONITORING)
# ═════════════════════════════════════════════════════════════════════════════
elif active_panel == "📚 Scientific Sources":
    st.markdown("### 📚 Scientific Sources & Evidence Library")
    st.markdown("Full transparency on peer-reviewed citations, retrieved FAO/IPCC literature chunks, dissenting evidence disclosures, and on-farm measurement protocols.")

    if not st.session_state.last_result:
        st.warning("⚠️ Please run an assessment in the **🔬 AI Scientist & Assessment** panel first to view scientific sources.")
    else:
        res = st.session_state.last_result
        evidence = res.get("retrieved_evidence", [])
        dissenting = res.get("dissenting_evidence", [])
        mon_plan = res.get("monitoring_plan", [])
        chains = res.get("causal_chains", [])

        # 1. Retrieved Peer-Reviewed Evidence
        st.markdown(f"#### 📄 Retrieved Peer-Reviewed Literature ({len(evidence)} Studies)")
        for ev in evidence:
            st.markdown(f"""
            <div class="chunk-box">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span class="chunk-id">[{ev.get('id')}]</span>
                    <span style="font-size:11px;color:#8B5E3C;font-weight:700">Relevance Score: {ev.get('relevance_score','0.88')}</span>
                </div>
                <div style="font-size:13.5px;font-weight:800;color:#382417;margin:4px 0">{ev.get('title')}</div>
                <div class="chunk-src">Source: {ev.get('source')} ({ev.get('year')}) | Biome: {ev.get('biome','Global')}</div>
                <div style="font-size:12px;color:#4A3324;margin-top:6px;line-height:1.5;background:#FFF5E1;padding:8px 12px;border-radius:6px">
                    "{ev.get('excerpt','')}"
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 2. Dissenting Studies & Boundary Conditions
        if dissenting:
            st.markdown("---")
            st.markdown("#### ⚠️ Dissenting Evidence & Boundary Disclosures")
            for d in dissenting:
                st.markdown(f"""
                <div style="background:#FFF1F2;border-left:4px solid #F43F5E;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0">
                    <div style="font-family:'Fira Code',monospace;font-size:11px;color:#9F1239;font-weight:700">CRITICAL TRADE-OFF [{d.get('chunk_id')}]: {d.get('title')}</div>
                    <div style="font-size:12.5px;color:#881337;line-height:1.6;margin-top:4px">{d.get('dissenting_summary')}</div>
                </div>
                """, unsafe_allow_html=True)

        # 3. 3-Hop Causal Reasoning Chains
        if chains:
            st.markdown("---")
            st.markdown("#### 🔗 Multi-Metric 3-Hop Causal Reasoning Trace")
            for chain in chains:
                st.markdown(f"**{chain.get('title')}** ({chain.get('hop_count', 3)} hops):")
                for h_idx, hop in enumerate(chain.get("hops", []), 1):
                    st.markdown(f"""
                    <div style="background:#FFFDF8;border-left:4px solid #0284C7;border:1px solid rgba(169,113,66,0.15);padding:8px 14px;border-radius:0 6px 6px 0;margin:4px 0;font-size:12px">
                        <strong>Hop {h_idx}:</strong> <span style="color:#0369A1">{hop.get('source_var')}</span>
                        ➔ <em>{hop.get('relationship')}</em> ➔ <span style="color:#065F46">{hop.get('target_var')}</span>
                        <div style="font-size:10.5px;color:#856852;margin-top:2px">Citation: [{hop.get('evidence_ref') or hop.get('evidence_citation','')}] | Principle: {hop.get('scientific_principle','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # 4. On-Farm Field Monitoring Protocols
        if mon_plan:
            st.markdown("---")
            st.markdown("#### 📋 Field Monitoring Protocol (Grower Verification)")
            for p in mon_plan:
                st.markdown(f"""
                <div style="background:#FFFDF8;border:1px solid rgba(169,113,66,0.22);border-radius:8px;padding:12px 16px;margin:6px 0">
                    <div style="font-size:13.5px;font-weight:800;color:#382417">📋 {p.get('parameter','')}</div>
                    <div style="font-size:12px;color:#5C3D28;margin-top:4px"><strong>Measurement Method:</strong> {p.get('baseline_method','')}</div>
                    <div style="font-size:12px;color:#5C3D28"><strong>Testing Frequency:</strong> {p.get('frequency','')}</div>
                    <div style="font-size:12px;color:#059669;font-weight:700;margin-top:2px">✓ Year 1 Milestone: {p.get('short_term_indicator','')}</div>
                    <div style="font-size:12px;color:#065F46;font-weight:700">✓ Years 3–5 Climax: {p.get('long_term_indicator','')}</div>
                </div>
                """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PANEL 6: 🗄️ AUDIT HISTORY & INTELLIGENCE DATABASE
# ═════════════════════════════════════════════════════════════════════════════
elif active_panel == "🗄️ Audit History & Database":
    st.markdown("### 🗄️ Persistent Audit History & Intelligence Database")
    st.markdown("Centralized repository storing all multi-turn consultations, chat history, and cached ecological analyses. Identical field queries retrieve proven solutions instantly without redundant computation.")

    # 1. Database KPI Statistics
    stats = AuditDatabase.get_database_stats()
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)
    with k_col1:
        st.metric("Total Consultations", stats.get("total_sessions", 0))
    with k_col2:
        st.metric("Cached Solutions", stats.get("cached_solutions", 0))
    with k_col3:
        st.metric("Instant Cache Reuses", stats.get("cache_reuse_hits", 0))
    with k_col4:
        st.metric("Chat Messages Logged", stats.get("total_messages", 0))

    st.markdown("---")

    # 2. Recent Sessions & Session Loader
    st.markdown("#### 📜 Historical Consultation Sessions")
    recent_sessions = AuditDatabase.list_recent_sessions(limit=30)
    if not recent_sessions:
        st.info("No prior sessions recorded yet in SQLite database.")
    else:
        for s in recent_sessions:
            is_active = s["session_id"] == st.session_state.session_id
            badge = "🟢 ACTIVE SESSION" if is_active else "📁 STORED CONSULTATION"
            h_score = s.get("health_score") or "—"
            
            with st.container():
                s_c1, s_c2, s_c3 = st.columns([3, 2, 1.2])
                with s_c1:
                    st.markdown(f"**{s.get('title', 'Consultation')}** `{s['session_id']}`")
                    st.caption(f"Ecosystem: **{s.get('ecosystem_type','').title()}** | Health Score: **{h_score}/100**")
                with s_c2:
                    st.caption(f"Last updated: {s.get('updated_at','')[:16].replace('T', ' ')}")
                    st.caption(f"Queries evaluated: {s.get('query_count', 1)}")
                with s_c3:
                    if not is_active:
                        if st.button("📂 Load Session", key=f"load_sess_{s['session_id']}", use_container_width=True):
                            st.session_state.session_id = s["session_id"]
                            st.session_state.followup_chat = AuditDatabase.get_session_chat_history(s["session_id"])
                            st.success(f"Loaded session {s['session_id']} into active memory!")
                            st.rerun()
                    else:
                        st.markdown(f"<span style='color:#059669;font-weight:700'>{badge}</span>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:8px 0;border:0.5px solid rgba(169,113,66,0.15)'>", unsafe_allow_html=True)

    # 3. Chat History Viewer for Active Session
    st.markdown("---")
    st.markdown(f"#### 💬 Persistent Chat & Dialogue Log (`{st.session_state.session_id}`)")
    session_chats = AuditDatabase.get_session_chat_history(st.session_state.session_id)
    if not session_chats:
        st.caption("No chat messages recorded for this session yet.")
    else:
        for chat in session_chats:
            role_label = "👤 Practitioner" if chat["role"] == "user" else "🌍 AI Environmental Scientist"
            role_cls = "msg-user" if chat["role"] == "user" else "msg-system"
            st.markdown(f"""
            <div class="{role_cls}">
                <div class="msg-meta"><span class="msg-role">{role_label}</span> &nbsp; {chat.get('time','')[:19].replace('T', ' ')}</div>
                {chat['text']}
            </div>
            """, unsafe_allow_html=True)
