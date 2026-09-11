"""
Scientific Visualizations & Animated Diagrams Module
Darukaa.Earth AI Biodiversity Intelligence Platform

Generates interactive Altair charts, comparative metric graphs, and
pure SVG/CSS animated diagrams to illustrate biophysical mechanisms:
- 5-Year Multi-Metric Recovery Trajectories
- Before vs After Soil Health & Biodiversity Bar Comparisons
- Animated Rhizosphere Symbiosis Diagram (AMF hyphae, N-fixation, pollinators)
- Animated Agroforestry Microclimate Diagram (windbreak boundary layer & hydraulic lift)
- Interactive 3-Hop Causal Graph SVG
"""

import altair as alt
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any, List


# ═════════════════════════════════════════════════════════════════════════════
# 1. ALTAIR CHARTS: RECOVERY TRAJECTORIES & METRIC COMPARISONS
# ═════════════════════════════════════════════════════════════════════════════

def create_problem_severity_gauge_chart(
    baseline_soc: float = 0.30,
    rainfall_mm: float = 320.0,
    ecosystem_type: str = "agricultural",
    profile: Dict[str, Any] = None
) -> alt.Chart:
    """Grouped bar chart showing Current Problem State vs Minimum Ecological Health Threshold per ecosystem."""
    eco = (ecosystem_type or "agricultural").lower()

    if eco == "urban":
        metrics = [
            {"Metric": "Stormwater Runoff TSS (mg/L)", "Current_State": 120.0, "Healthy_Threshold": 25.0, "Unit": "mg/L TSS", "Status": "CRITICAL POLLUTANT PLUME"},
            {"Metric": "Heavy Metal Bio-Load (ppm)", "Current_State": 48.0, "Healthy_Threshold": 10.0, "Unit": "ppm", "Status": "ELEVATED TOXICITY"},
            {"Metric": "Urban Tree Canopy (%)", "Current_State": 6.0, "Healthy_Threshold": 30.0, "Unit": "%", "Status": "EXTREME HEAT ISLAND"},
            {"Metric": "Avian Nesting Diversity", "Current_State": 14.0, "Healthy_Threshold": 55.0, "Unit": "Index", "Status": "SPECIES DEPAUPERATE"},
            {"Metric": "Stormwater Infiltration (%)", "Current_State": 15.0, "Healthy_Threshold": 75.0, "Unit": "%", "Status": "IMPERVIOUS FLOOD RISK"}
        ]
        title_text = " Urban Diagnostic Deficit: Current Runoff/Habitat vs EPA Green Infrastructure Thresholds"
    elif eco == "wetland":
        metrics = [
            {"Metric": "Nitrate & Phosphate (mg/L)", "Current_State": 18.5, "Healthy_Threshold": 2.5, "Unit": "mg/L", "Status": "SEVERE EUTROPHICATION"},
            {"Metric": "Dissolved Oxygen (mg/L)", "Current_State": 2.1, "Healthy_Threshold": 6.5, "Unit": "mg/L", "Status": "CRITICAL BENTHIC HYPOXIA"},
            {"Metric": "Littoral Macrophyte Cover (%)", "Current_State": 8.0, "Healthy_Threshold": 50.0, "Unit": "%", "Status": "BUFFER LOSS"},
            {"Metric": "Benthic Macroinvertebrate Index", "Current_State": 18.0, "Healthy_Threshold": 65.0, "Unit": "Index", "Status": "TROPHIC COLLAPSE"},
            {"Metric": "Waterfowl Breeding Habitat (%)", "Current_State": 15.0, "Healthy_Threshold": 60.0, "Unit": "%", "Status": "NESTING DESICCATION"}
        ]
        title_text = " Wetland Diagnostic Deficit: Current Eutrophication vs Ramsar Conservation Baselines"
    elif eco == "forest":
        metrics = [
            {"Metric": "Canopy Cover (%)", "Current_State": 24.0, "Healthy_Threshold": 75.0, "Unit": "%", "Status": "DEFORESTATION STRESS"},
            {"Metric": "Core Interior Habitat Area (%)", "Current_State": 15.0, "Healthy_Threshold": 65.0, "Unit": "%", "Status": "SEVERE FRAGMENTATION"},
            {"Metric": "Edge Desiccation Penetration (m)", "Current_State": 110.0, "Healthy_Threshold": 20.0, "Unit": "m depth", "Status": "MICROCLIMATE DRYING"},
            {"Metric": "Interior Bird Species Richness", "Current_State": 8.0, "Healthy_Threshold": 28.0, "Unit": "species", "Status": "HABITAT COLLAPSE"},
            {"Metric": "Corridor Connectivity (%)", "Current_State": 18.0, "Healthy_Threshold": 70.0, "Unit": "%", "Status": "ISOLATED PATCH"}
        ]
        title_text = " Forest Diagnostic Deficit: Current Fragmentation vs Structural Ecological Threshold"
    else:
        # Agricultural
        target_soc = 1.20
        metrics = [
            {"Metric": "Soil Carbon (SOC %)", "Current_State": baseline_soc, "Healthy_Threshold": target_soc, "Unit": "%", "Status": "CRITICAL DEFICIT (-75%)"},
            {"Metric": "Available Water Cap. (%)", "Current_State": round(min(50.0, baseline_soc * 80), 1), "Healthy_Threshold": 70.0, "Unit": "%", "Status": "HIGH VULNERABILITY"},
            {"Metric": "Microbial Biomass (mg C/100g)", "Current_State": 12.0, "Healthy_Threshold": 35.0, "Unit": "mg C", "Status": "SEVERE STARVATION"},
            {"Metric": "Infiltration Rate (mm/hr)", "Current_State": 8.0, "Healthy_Threshold": 25.0, "Unit": "mm/hr", "Status": "SURFACE CRUSTING"},
            {"Metric": "Biodiversity Intactness (%)", "Current_State": 20.0, "Healthy_Threshold": 60.0, "Unit": "%", "Status": "MONOCULTURE DEPLETION"}
        ]
        title_text = " Diagnostic Soil & Ecosystem Deficit: Current Farm Baseline vs Sustainable Threshold (FAO)"

    data = []
    for m in metrics:
        data.append({"Metric": m["Metric"], "Condition": "1. Current Site Baseline (Degraded)", "Value": m["Current_State"], "Unit": m["Unit"]})
        data.append({"Metric": m["Metric"], "Condition": "2. Minimum Ecological Threshold", "Value": m["Healthy_Threshold"], "Unit": m["Unit"]})

    df = pd.DataFrame(data)

    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Metric:N", title=None, axis=alt.Axis(labelAngle=-15, labelColor="#4A3324")),
        y=alt.Y("Value:Q", title="Parametric Metric Value", axis=alt.Axis(labelColor="#4A3324", titleColor="#382417")),
        color=alt.Color(
            "Condition:N",
            scale=alt.Scale(
                domain=["1. Current Site Baseline (Degraded)", "2. Minimum Ecological Threshold"],
                range=["#e11d48", "#0284c7"]
            ),
            legend=alt.Legend(orient="top", title=None, labelColor="#382417")
        ),
        xOffset="Condition:N",
        tooltip=["Condition", "Metric", "Value", "Unit"]
    ).properties(
        width=600,
        height=260,
        title=title_text
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        gridColor="rgba(169, 113, 66, 0.15)",
        labelColor="#4A3324",
        titleColor="#382417"
    ).configure_title(
        color="#382417",
        fontSize=13,
        fontWeight="bold"
    )

    return chart


def create_5year_soc_trajectory_chart(
    baseline_soc: float = 0.30,
    target_soc: float = 1.20,
    ecosystem_type: str = "agricultural"
) -> alt.Chart:
    """Generates an interactive 5-year trajectory comparing Degraded baseline vs Verified Recovery per ecosystem."""
    years = [0, 1, 2, 3, 4, 5]
    eco = (ecosystem_type or "agricultural").lower()

    if eco == "urban":
        y_title = "Stormwater & Heavy Metal Interception Efficiency (%)"
        chart_title = " 5-Year Urban Stormwater & Biodiversity Trajectory (EPA / Nature Sustainability)"
        degraded_vals = [15.0, 14.0, 13.0, 12.0, 11.0, 10.0]
        regen_vals = [15.0, 38.0, 56.0, 72.0, 84.0, 92.0]
        degraded_label = "Unmitigated Impervious Runoff (Decline)"
        regen_label = "Engineered Bioswales & Pocket Forests (Recovery)"
    elif eco == "wetland":
        y_title = "Dissolved Oxygen (mg/L) & Buffer Nitrate Removal"
        chart_title = " 5-Year Wetland Water Quality & DO Trajectory (Ramsar Guidelines)"
        degraded_vals = [2.1, 1.9, 1.8, 1.6, 1.5, 1.4]
        regen_vals = [2.1, 3.6, 4.8, 5.9, 6.6, 7.1]
        degraded_label = "Unbuffered Eutrophic Runoff (Hypoxia Path)"
        regen_label = "Riparian Macrophyte Buffer Strips (Recovery Path)"
    elif eco == "forest":
        y_title = "Structural Canopy Connectivity (%)"
        chart_title = " 5-Year Forest Habitat Connectivity Trajectory (Science 2020)"
        degraded_vals = [22.0, 20.0, 18.0, 16.0, 14.0, 12.0]
        regen_vals = [22.0, 36.0, 49.0, 62.0, 71.0, 78.0]
        degraded_label = "Continued Clearing & Edge Dieback (Loss)"
        regen_label = "Wildlife Canopy Corridors & ANR (Recovery Path)"
    else:
        # Agricultural
        y_title = "Soil Organic Carbon (SOC %)"
        chart_title = " 5-Year Soil Organic Carbon Trajectory: Baseline vs Verified Recovery (FAO / IPCC)"
        degraded_vals = [round(max(0.18, baseline_soc - (i * 0.02)), 3) for i in years]
        regen_vals = [
            baseline_soc,
            round(baseline_soc * 1.18, 3),
            round(baseline_soc * 1.35, 3),
            round(baseline_soc + 0.22, 3),
            round(baseline_soc + 0.35, 3),
            round(min(target_soc, baseline_soc + 0.48), 3)
        ]
        degraded_label = "Conventional Monoculture (Degradation Path)"
        regen_label = "Regenerative Agroforestry + Legumes (Recovery Path)"

    df_degraded = pd.DataFrame({
        "Year": [f"Year {y}" if y > 0 else "Baseline" for y in years],
        "Year_Num": years,
        "Value": degraded_vals,
        "System": degraded_label
    })

    df_regen = pd.DataFrame({
        "Year": [f"Year {y}" if y > 0 else "Baseline" for y in years],
        "Year_Num": years,
        "Value": regen_vals,
        "System": regen_label
    })

    df = pd.concat([df_degraded, df_regen])

    line = alt.Chart(df).mark_line(point=True, strokeWidth=3.5).encode(
        x=alt.X("Year:N", sort=[f"Year {y}" if y > 0 else "Baseline" for y in years], title="Time Horizon", axis=alt.Axis(labelColor="#4A3324", titleColor="#382417")),
        y=alt.Y("Value:Q", title=y_title, axis=alt.Axis(labelColor="#4A3324", titleColor="#382417")),
        color=alt.Color(
            "System:N",
            scale=alt.Scale(
                domain=[regen_label, degraded_label],
                range=["#059669", "#e11d48"]
            ),
            legend=alt.Legend(orient="top", title=None, labelColor="#382417")
        ),
        tooltip=["System", "Year", "Value"]
    ).properties(
        width=600,
        height=260,
        title=chart_title
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        gridColor="rgba(169, 113, 66, 0.15)",
        labelColor="#4A3324",
        titleColor="#382417"
    ).configure_title(
        color="#382417",
        fontSize=13,
        fontWeight="bold"
    )

    return line


def create_multi_metric_comparison_chart(
    baseline_soc: float = 0.3,
    ecosystem_type: str = "agricultural"
) -> alt.Chart:
    """Grouped bar chart comparing 5 vital biophysical metrics: Before vs After Intervention."""
    eco = (ecosystem_type or "agricultural").lower()

    if eco == "urban":
        metrics = [
            {"Metric": "Stormwater TSS (100 - x)", "Baseline": 15.0, "Post_Intervention": 82.0, "Unit": "% captured"},
            {"Metric": "Heavy Metal Bio-Filtration", "Baseline": 12.0, "Post_Intervention": 78.0, "Unit": "% removed"},
            {"Metric": "Native Canopy & Green Ratio", "Baseline": 8.0, "Post_Intervention": 32.0, "Unit": "% cover"},
            {"Metric": "Avian Nesting Habitat Index", "Baseline": 16.0, "Post_Intervention": 62.0, "Unit": "index /100"},
            {"Metric": "Heat Island Mitigation (°C)", "Baseline": 10.0, "Post_Intervention": 68.0, "Unit": "% cooled"}
        ]
        chart_title = " Urban Multi-Metric Recovery: Before vs 3-Year Post-Intervention"
    elif eco == "wetland":
        metrics = [
            {"Metric": "Nutrient Inflow Removal (%)", "Baseline": 12.0, "Post_Intervention": 85.0, "Unit": "% NO3/PO4 trapped"},
            {"Metric": "Dissolved Oxygen (mg/L x10)", "Baseline": 21.0, "Post_Intervention": 68.0, "Unit": "mg/L DO x10"},
            {"Metric": "Macrophyte Filter Coverage", "Baseline": 8.0, "Post_Intervention": 65.0, "Unit": "% cover"},
            {"Metric": "Macroinvertebrate Diversity", "Baseline": 18.0, "Post_Intervention": 72.0, "Unit": "index /100"},
            {"Metric": "Waterfowl Breeding Fledging", "Baseline": 15.0, "Post_Intervention": 60.0, "Unit": "% success"}
        ]
        chart_title = " Wetland Multi-Metric Recovery: Before vs 3-Year Post-Intervention"
    elif eco == "forest":
        metrics = [
            {"Metric": "Canopy Continuity (%)", "Baseline": 24.0, "Post_Intervention": 72.0, "Unit": "% closed canopy"},
            {"Metric": "Core Interior Habitat (%)", "Baseline": 15.0, "Post_Intervention": 58.0, "Unit": "% core area"},
            {"Metric": "Edge Wind Shielding (%)", "Baseline": 20.0, "Post_Intervention": 75.0, "Unit": "% desiccation blocked"},
            {"Metric": "Forest Bird Species Count", "Baseline": 8.0, "Post_Intervention": 26.0, "Unit": "resident species"},
            {"Metric": "Landscape Gene Flow Index", "Baseline": 18.0, "Post_Intervention": 74.0, "Unit": "connectivity /100"}
        ]
        chart_title = " Forest Multi-Metric Recovery: Before vs 3-Year Post-Intervention"
    else:
        # Agricultural
        metrics = [
            {"Metric": "Soil Carbon (x10 %)", "Baseline": baseline_soc * 10, "Post_Intervention": round((baseline_soc + 0.28) * 10, 1), "Unit": "SOC % x10"},
            {"Metric": "Available Water Cap. (%)", "Baseline": 35.0, "Post_Intervention": 68.0, "Unit": "% retention"},
            {"Metric": "Microbial Biomass (mg C)", "Baseline": 12.0, "Post_Intervention": 28.0, "Unit": "mg C/100g"},
            {"Metric": "Infiltration Rate (mm/hr)", "Baseline": 8.0, "Post_Intervention": 28.0, "Unit": "mm/hr"},
            {"Metric": "Pollinator Floral Density", "Baseline": 20.0, "Post_Intervention": 68.0, "Unit": "visitation index"}
        ]
        chart_title = " Agricultural Multi-Metric Recovery: Before vs 3-Year Post-Intervention"

    data = []
    for m in metrics:
        data.append({"Metric": m["Metric"], "State": "1. Degraded Baseline (Before)", "Value": m["Baseline"], "Unit": m["Unit"]})
        data.append({"Metric": m["Metric"], "State": "2. Solved State (After 3-5 Yrs)", "Value": m["Post_Intervention"], "Unit": m["Unit"]})

    df = pd.DataFrame(data)

    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Metric:N", title=None, axis=alt.Axis(labelAngle=-15, labelColor="#4A3324")),
        y=alt.Y("Value:Q", title="Normalized Quantitative Index Level", axis=alt.Axis(labelColor="#4A3324", titleColor="#382417")),
        color=alt.Color(
            "State:N",
            scale=alt.Scale(
                domain=["1. Degraded Baseline (Before)", "2. Solved State (After 3-5 Yrs)"],
                range=["#d97706", "#0d9488"]
            ),
            legend=alt.Legend(orient="top", title=None, labelColor="#382417")
        ),
        xOffset="State:N",
        tooltip=["State", "Metric", "Value", "Unit"]
    ).properties(
        width=600,
        height=260,
        title=chart_title
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        gridColor="rgba(169, 113, 66, 0.15)",
        labelColor="#4A3324",
        titleColor="#382417"
    ).configure_title(
        color="#382417",
        fontSize=13,
        fontWeight="bold"
    )

    return chart


def create_ecological_threshold_comparison_chart(profile: dict, rule_metrics: dict) -> go.Figure:
    """Grouped bar chart matching the dashboard threshold comparison with explicit cream theme, Y-axis grid, and labels."""
    eco = (profile.get("ecosystem_type") or rule_metrics.get("ecosystem_type") or "agricultural").lower()

    if eco == "forest":
        veg = float(profile.get("vegetation_cover") or profile.get("canopy_cover_pct") or 24.0)
        metrics = [
            {"Metric": "Canopy %", "Baseline": veg, "Target": 75.0},
            {"Metric": "Core Area %", "Baseline": 18.0, "Target": 65.0},
            {"Metric": "Interior Birds", "Baseline": 8.0, "Target": 28.0},
            {"Metric": "Connectivity %", "Baseline": 22.0, "Target": 72.0}
        ]
    elif eco == "urban":
        pervious = float(profile.get("pervious_area_percent") or 14.0)
        metrics = [
            {"Metric": "Infiltration %", "Baseline": pervious, "Target": 75.0},
            {"Metric": "TSS Removal %", "Baseline": 20.0, "Target": 88.0},
            {"Metric": "Tree Canopy %", "Baseline": 8.0, "Target": 32.0},
            {"Metric": "Green Space %", "Baseline": 12.0, "Target": 45.0}
        ]
    elif eco == "wetland":
        metrics = [
            {"Metric": "Dissolved O2 (x10)", "Baseline": 21.0, "Target": 70.0},
            {"Metric": "Nitrate Strip %", "Baseline": 15.0, "Target": 88.0},
            {"Metric": "Macrophyte %", "Baseline": 10.0, "Target": 55.0},
            {"Metric": "Benthic Index", "Baseline": 18.0, "Target": 65.0}
        ]
    else:
        # Agricultural
        soc = float(profile.get("soc_percent") or 0.35)
        metrics = [
            {"Metric": "SOC % (x10)", "Baseline": round(soc * 10, 1), "Target": 12.0},
            {"Metric": "Infiltration (mm/h)", "Baseline": 8.0, "Target": 35.0},
            {"Metric": "Moisture Cap. %", "Baseline": 45.0, "Target": 90.0},
            {"Metric": "Mycorrhiza %", "Baseline": 15.0, "Target": 75.0}
        ]

    x_categories = [m["Metric"] for m in metrics]
    baseline_vals = [m["Baseline"] for m in metrics]
    target_vals = [m["Target"] for m in metrics]

    fig = go.Figure()

    # Current Baseline (Red)
    fig.add_trace(go.Bar(
        name="Current Baseline",
        x=x_categories,
        y=baseline_vals,
        marker=dict(
            color="#F43F5E",
            line=dict(color="#BE123C", width=1.5),
            cornerradius=4
        ),
        text=[f"{v:.0f}%" for v in baseline_vals],
        textposition="outside",
        textfont=dict(size=12, color="#BE123C", family="'Fira Code', monospace", weight="bold")
    ))

    # Ecological Threshold Target (Green)
    fig.add_trace(go.Bar(
        name="Ecological Threshold Target",
        x=x_categories,
        y=target_vals,
        marker=dict(
            color="#10B981",
            line=dict(color="#047857", width=1.5),
            cornerradius=4
        ),
        text=[f"{v:.0f}%" for v in target_vals],
        textposition="outside",
        textfont=dict(size=12, color="#047857", family="'Fira Code', monospace", weight="bold")
    ))

    fig.update_layout(
        barmode="group",
        bargap=0.28,
        bargroupgap=0.08,
        paper_bgcolor="#FFFDF8",
        plot_bgcolor="#FFFDF8",
        height=320,
        margin=dict(l=55, r=25, t=35, b=45),
        xaxis=dict(
            tickfont=dict(size=12, color="#382417", family="'Inter', sans-serif", weight="bold"),
            linecolor="rgba(169, 113, 66, 0.4)",
            linewidth=1.5,
            showgrid=False
        ),
        yaxis=dict(
            range=[0, 115],
            tickvals=[0, 20, 40, 60, 80, 100],
            ticktext=["0", "20", "40", "60", "80", "100"],
            tickfont=dict(size=12, color="#382417", family="'Fira Code', monospace", weight="bold"),
            gridcolor="rgba(169, 113, 66, 0.28)",
            gridwidth=1.5,
            showgrid=True,
            linecolor="rgba(169, 113, 66, 0.4)",
            linewidth=1.5,
            zeroline=True,
            zerolinecolor="rgba(169, 113, 66, 0.4)",
            zerolinewidth=1.5
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color="#382417", family="'Inter', sans-serif", weight="bold")
        )
    )
    return fig


def create_ecological_radar_chart(ecosystem_type: str = "forest", profile: dict = None) -> go.Figure:
    """Generates the 5-Axis Ecological Equilibrium Radar Chart comparing Current Field Baseline vs Healthy Target."""
    eco = (ecosystem_type or "agricultural").lower()
    if eco == "forest":
        categories = ["Canopy Cover", "Core Area %", "Interior Birds", "Moisture Buffer", "Corridor Link"]
        current_vals = [24, 18, 16, 22, 20]
        target_vals = [75, 65, 70, 80, 72]
    elif eco == "urban":
        categories = ["Infiltration", "TSS Trapping", "Tree Canopy", "Cooling Buffer", "Pollinator Link"]
        current_vals = [14, 20, 10, 15, 18]
        target_vals = [75, 88, 35, 70, 65]
    elif eco == "wetland":
        categories = ["Dissolved O2", "Nitrate Filter", "Littoral Cover", "Water Stability", "Avian Nesting"]
        current_vals = [21, 15, 12, 25, 18]
        target_vals = [70, 85, 60, 80, 75]
    else:
        # Agricultural
        categories = ["Topsoil SOC", "Infiltration", "Moisture Retention", "AMF Activity", "Yield Resilience"]
        current_vals = [25, 20, 30, 15, 28]
        target_vals = [80, 75, 85, 75, 85]

    # Close polygon loops
    categories_loop = categories + [categories[0]]
    current_loop = current_vals + [current_vals[0]]
    target_loop = target_vals + [target_vals[0]]

    fig = go.Figure()

    # Target (Green)
    fig.add_trace(go.Scatterpolar(
        r=target_loop,
        theta=categories_loop,
        fill="toself",
        fillcolor="rgba(16, 185, 129, 0.16)",
        line=dict(color="#10B981", width=2.5),
        name="Healthy Ecological Target (2-5 Yr)",
        mode="lines+markers",
        marker=dict(size=5, color="#10B981")
    ))

    # Baseline (Red)
    fig.add_trace(go.Scatterpolar(
        r=current_loop,
        theta=categories_loop,
        fill="toself",
        fillcolor="rgba(244, 63, 94, 0.16)",
        line=dict(color="#F43F5E", width=2.5),
        name="Current Field Baseline",
        mode="lines+markers",
        marker=dict(size=5, color="#F43F5E")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                linecolor="rgba(169, 113, 66, 0.2)",
                gridcolor="rgba(169, 113, 66, 0.18)"
            ),
            angularaxis=dict(
                linecolor="rgba(169, 113, 66, 0.25)",
                gridcolor="rgba(169, 113, 66, 0.18)",
                tickfont=dict(size=11, color="#382417", family="'Inter', sans-serif")
            ),
            bgcolor="#FFFDF8"
        ),
        paper_bgcolor="#FFFDF8",
        plot_bgcolor="#FFFDF8",
        margin=dict(l=35, r=35, t=15, b=35),
        height=260,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#382417")
        ),
        showlegend=True
    )
    return fig


def create_5year_recovery_trajectory_chart(ecosystem_type: str = "forest", profile: dict = None) -> go.Figure:
    """Generates the 5-Year Recovery Trajectory line chart matching the biophysical recovery model."""
    eco = (ecosystem_type or "agricultural").lower()
    x_labels = ["Year 0 (Baseline)", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5 (Climax)"]

    if eco == "forest":
        series_name = "Canopy & Structural Corridor (%)"
        y_vals = [24, 36, 50, 63, 73, 82]
    elif eco == "urban":
        series_name = "Runoff Interception & Canopy (%)"
        y_vals = [14, 32, 52, 68, 80, 88]
    elif eco == "wetland":
        series_name = "Dissolved Oxygen & Buffer Cover (%)"
        y_vals = [21, 35, 52, 67, 78, 85]
    else:
        # Agricultural
        series_name = "Soil Health & Carbon Index (%)"
        y_vals = [25, 38, 54, 69, 80, 89]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_labels,
        y=y_vals,
        mode="lines+markers",
        name=series_name,
        line=dict(color="#10B981", width=3.5),
        marker=dict(size=7, color="#10B981", symbol="circle"),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.08)"
    ))

    fig.update_layout(
        paper_bgcolor="#FFFDF8",
        plot_bgcolor="#FFFDF8",
        height=260,
        margin=dict(l=35, r=20, t=15, b=35),
        xaxis=dict(
            tickfont=dict(size=10.5, color="#4A3324", family="'Inter', sans-serif"),
            showgrid=False,
            linecolor="rgba(169, 113, 66, 0.25)"
        ),
        yaxis=dict(
            range=[0, 100],
            tickvals=[10, 20, 30, 40, 50, 60, 70, 80, 90],
            ticktext=["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"],
            tickfont=dict(size=10.5, color="#4A3324", family="'Inter', sans-serif"),
            gridcolor="rgba(169, 113, 66, 0.15)",
            linecolor="rgba(169, 113, 66, 0.25)"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#382417", weight="bold")
        ),
        showlegend=True
    )
    return fig


def create_current_vs_solved_recovery_plotly_chart(
    baseline_soc: float = 0.35,
    ecosystem_type: str = "forest",
    profile: dict = None
) -> go.Figure:
    """Grouped bar chart comparing 5 vital biophysical metrics: Current Degraded Baseline vs Solved Climax State."""
    eco = (ecosystem_type or "agricultural").lower()

    if eco == "urban":
        metrics = [
            {"Metric": "Stormwater TSS Filtration", "Baseline": 15.0, "Solved": 85.0},
            {"Metric": "Heavy Metal Bio-Removal", "Baseline": 12.0, "Solved": 78.0},
            {"Metric": "Native Tree Canopy Ratio", "Baseline": 10.0, "Solved": 35.0},
            {"Metric": "Avian Nesting Diversity", "Baseline": 16.0, "Solved": 62.0},
            {"Metric": "Urban Cooling Effect", "Baseline": 14.0, "Solved": 70.0}
        ]
    elif eco == "wetland":
        metrics = [
            {"Metric": "Nitrate & Phosphate Filter", "Baseline": 12.0, "Solved": 85.0},
            {"Metric": "Dissolved Oxygen (DO)", "Baseline": 21.0, "Solved": 72.0},
            {"Metric": "Littoral Macrophyte Strip", "Baseline": 10.0, "Solved": 65.0},
            {"Metric": "Benthic Macroinvertebrates", "Baseline": 18.0, "Solved": 72.0},
            {"Metric": "Waterfowl Breeding Fledging", "Baseline": 15.0, "Solved": 68.0}
        ]
    elif eco == "forest":
        metrics = [
            {"Metric": "Canopy Continuity %", "Baseline": 24.0, "Solved": 75.0},
            {"Metric": "Core Interior Habitat %", "Baseline": 18.0, "Solved": 65.0},
            {"Metric": "Edge Wind Shielding %", "Baseline": 20.0, "Solved": 78.0},
            {"Metric": "Forest Bird Richness", "Baseline": 16.0, "Solved": 70.0},
            {"Metric": "Landscape Gene Flow Index", "Baseline": 18.0, "Solved": 74.0}
        ]
    else:
        # Agricultural
        soc_b = min(100.0, (baseline_soc or 0.35) * 35)
        soc_s = min(100.0, soc_b + 45.0)
        metrics = [
            {"Metric": "Topsoil SOC Index", "Baseline": round(soc_b, 1), "Solved": round(soc_s, 1)},
            {"Metric": "Soil Water Retention Cap.", "Baseline": 35.0, "Solved": 82.0},
            {"Metric": "Mycorrhizal AMF Inoculation", "Baseline": 15.0, "Solved": 75.0},
            {"Metric": "Rainfall Infiltration Rate", "Baseline": 20.0, "Solved": 70.0},
            {"Metric": "Wild Pollinator Forage Index", "Baseline": 22.0, "Solved": 78.0}
        ]

    x_cats = [m["Metric"] for m in metrics]
    b_vals = [m["Baseline"] for m in metrics]
    s_vals = [m["Solved"] for m in metrics]

    fig = go.Figure()

    # Current Degraded Baseline (Red)
    fig.add_trace(go.Bar(
        name="Current Degraded Baseline (Before)",
        x=x_cats,
        y=b_vals,
        marker=dict(
            color="#F43F5E",
            line=dict(color="#BE123C", width=1.5),
            cornerradius=4
        ),
        text=[f"{v:.0f}%" for v in b_vals],
        textposition="outside",
        textfont=dict(size=11, color="#BE123C", family="'Fira Code', monospace", weight="bold")
    ))

    # Solved Climax State (Green)
    fig.add_trace(go.Bar(
        name="Solved Ecosystem Equilibrium (After 3–5 Yrs)",
        x=x_cats,
        y=s_vals,
        marker=dict(
            color="#10B981",
            line=dict(color="#047857", width=1.5),
            cornerradius=4
        ),
        text=[f"{v:.0f}%" for v in s_vals],
        textposition="outside",
        textfont=dict(size=11, color="#047857", family="'Fira Code', monospace", weight="bold")
    ))

    fig.update_layout(
        barmode="group",
        bargap=0.28,
        bargroupgap=0.08,
        paper_bgcolor="#FFFDF8",
        plot_bgcolor="#FFFDF8",
        height=320,
        margin=dict(l=45, r=25, t=35, b=45),
        xaxis=dict(
            tickfont=dict(size=11.5, color="#382417", family="'Inter', sans-serif", weight="bold"),
            linecolor="rgba(169, 113, 66, 0.4)",
            linewidth=1.5,
            showgrid=False
        ),
        yaxis=dict(
            range=[0, 115],
            tickvals=[0, 20, 40, 60, 80, 100],
            ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
            tickfont=dict(size=11, color="#382417", family="'Fira Code', monospace", weight="bold"),
            gridcolor="rgba(169, 113, 66, 0.28)",
            gridwidth=1.5,
            showgrid=True,
            linecolor="rgba(169, 113, 66, 0.4)",
            linewidth=1.5,
            zeroline=True,
            zerolinecolor="rgba(169, 113, 66, 0.4)",
            zerolinewidth=1.5
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color="#382417", family="'Inter', sans-serif", weight="bold")
        )
    )
    return fig


# ═════════════════════════════════════════════════════════════════════════════
# 2. ANIMATED SVG DIAGRAMS (RHIZOSPHERE, AGROFORESTRY & CAUSAL FLOW)
# ═════════════════════════════════════════════════════════════════════════════

def render_animated_rhizosphere_diagram() -> str:
    """Pure SVG+CSS animated scientific diagram of legume-cereal rhizosphere symbiosis."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:12px;padding:16px;margin:0;box-shadow:0 4px 18px rgba(139,94,60,0.08);overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#8B5E3C;font-weight:800"> ANIMATED MECHANISM: RHIZOSPHERE MYCORRHIZAL &amp; NITROGEN SYMBIOSIS</span>
        <span style="background:rgba(217,164,65,0.18);color:#B45309;padding:3px 9px;border-radius:10px;font-size:10px;font-weight:700">FAO &amp; Nature Plants (2021)</span>
    </div>
    <div style="font-size:12.5px;color:#4A3324;margin-bottom:12px;line-height:1.5">
        Showing symbiotic Rhizobium nitrogen fixation, arbuscular mycorrhizal (AMF) hyphal bridges solubilizing phosphorus, and floral nectary pollinator support.
    </div>
    <svg viewBox="0 0 700 320" width="100%" height="280" style="background:#FFF8EC;border:1px solid rgba(169,113,66,0.2);border-radius:8px">
        <defs>
            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#0a1d17"/>
                <stop offset="100%" stop-color="#122b22"/>
            </linearGradient>
            <linearGradient id="soilGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#3d2817"/>
                <stop offset="30%" stop-color="#2a1b0e"/>
                <stop offset="100%" stop-color="#1a1109"/>
            </linearGradient>
            <linearGradient id="rootGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#fbbf24"/>
                <stop offset="100%" stop-color="#d97706"/>
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur"/>
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>

        <style>
            @keyframes n2flow {
                0% { transform: translateY(0); opacity: 0.2; }
                50% { opacity: 0.9; }
                100% { transform: translateY(55px); opacity: 0; }
            }
            @keyframes pulseNodule {
                0%, 100% { r: 6px; fill: #fbbf24; }
                50% { r: 8.5px; fill: #34d399; }
            }
            @keyframes hyphaFlow {
                0% { stroke-dashoffset: 100; }
                100% { stroke-dashoffset: 0; }
            }
            @keyframes beeHover {
                0%, 100% { transform: translate(0, 0); }
                50% { transform: translate(8px, -6px); }
            }
            @keyframes moistureRise {
                0% { transform: translateY(40px); opacity: 0; }
                50% { opacity: 1; }
                100% { transform: translateY(-20px); opacity: 0; }
            }
            .particle-n { animation: n2flow 2.2s infinite ease-in; }
            .particle-h { animation: moistureRise 2.8s infinite linear; }
            .nodule { animation: pulseNodule 2s infinite ease-in-out; }
            .bee { animation: beeHover 2.5s infinite ease-in-out; }
            .hypha-line { stroke-dasharray: 6, 4; animation: hyphaFlow 1.8s infinite linear; }
        </style>

        <!-- Above Ground / Sky -->
        <rect x="0" y="0" width="700" height="110" fill="url(#skyGrad)"/>
        <!-- Soil Horizon -->
        <rect x="0" y="110" width="700" height="210" fill="url(#soilGrad)"/>
        <line x1="0" y1="110" x2="700" y2="110" stroke="#34d399" stroke-width="2.5" opacity="0.6"/>
        <text x="12" y="102" fill="#34d399" font-family="'Fira Code', monospace" font-size="10">CANOPY &amp; FLORAL FORAGE LAYER</text>
        <text x="12" y="130" fill="#a78bfa" font-family="'Fira Code', monospace" font-size="10">TOPMINERAL TOPSOIL (0-30 cm)</text>

        <!-- Crop 1: Chickpea/Pigeonpea Legume (Left) -->
        <!-- Stem & Leaves -->
        <path d="M 220 110 Q 215 70 210 30" stroke="#10b981" stroke-width="5" fill="none"/>
        <ellipse cx="195" cy="55" rx="14" ry="7" fill="#34d399" transform="rotate(-30 195 55)"/>
        <ellipse cx="228" cy="45" rx="14" ry="7" fill="#34d399" transform="rotate(30 228 45)"/>
        <!-- Floral Head (Nectary) -->
        <circle cx="210" cy="24" r="8" fill="#f43f5e" filter="url(#glow)"/>
        <text x="145" y="24" fill="#fb7185" font-family="'Inter', sans-serif" font-size="10" font-weight="bold">Legume Nectary</text>

        <!-- Pollinator Bee -->
        <g class="bee" transform="translate(240, 20)">
            <ellipse cx="0" cy="0" rx="8" ry="5" fill="#facc15"/>
            <path d="M -3 -4 Q 0 -10 4 -4" stroke="#ffffff" stroke-width="2" fill="none"/>
            <text x="12" y="4" fill="#fef08a" font-family="'Inter', sans-serif" font-size="9.5"> Wild Pollinator (+180-240%)</text>
        </g>

        <!-- Legume Roots & Nodules -->
        <path d="M 220 110 Q 210 160 190 230" stroke="url(#rootGrad)" stroke-width="4.5" fill="none"/>
        <path d="M 210 150 Q 170 190 150 240" stroke="url(#rootGrad)" stroke-width="2.5" fill="none"/>
        <path d="M 215 170 Q 250 200 270 250" stroke="url(#rootGrad)" stroke-width="2.5" fill="none"/>

        <!-- Nodules (Rhizobium) -->
        <circle class="nodule" cx="205" cy="155" r="7"/>
        <circle class="nodule" cx="178" cy="185" r="6"/>
        <circle class="nodule" cx="240" cy="180" r="7"/>
        <text x="80" y="165" fill="#34d399" font-family="'Inter', sans-serif" font-size="10.5" font-weight="bold">Rhizobium Nodule</text>
        <text x="80" y="180" fill="#a7f3d0" font-family="'Inter', sans-serif" font-size="9">(Fixes 35-75 kg N/ha)</text>

        <!-- Infalling N2 particles -->
        <circle class="particle-n" cx="205" cy="115" r="3" fill="#60a5fa"/>
        <circle class="particle-n" cx="205" cy="130" r="2.5" fill="#93c5fd" style="animation-delay: 0.8s"/>

        <!-- Crop 2: Winter Wheat (Right) -->
        <!-- Stem & Grain Head -->
        <path d="M 480 110 Q 485 65 490 25" stroke="#f59e0b" stroke-width="4.5" fill="none"/>
        <ellipse cx="490" cy="18" rx="7" ry="16" fill="#fbbf24"/>
        <path d="M 490 8 L 490 0 M 486 12 L 480 5 M 494 12 L 500 5" stroke="#fbbf24" stroke-width="1.5"/>
        <text x="510" y="24" fill="#fde68a" font-family="'Inter', sans-serif" font-size="11" font-weight="bold">Winter Wheat (Cereal)</text>

        <!-- Wheat Roots -->
        <path d="M 480 110 Q 470 170 460 240" stroke="#fbbf24" stroke-width="3.5" fill="none"/>
        <path d="M 475 140 Q 430 180 400 230" stroke="#fbbf24" stroke-width="2" fill="none"/>
        <path d="M 482 160 Q 520 200 540 250" stroke="#fbbf24" stroke-width="2" fill="none"/>

        <!-- AMF Mycorrhizal Hyphal Network Connecting Both Plants -->
        <path class="hypha-line" d="M 270 200 C 330 220, 360 210, 400 210" stroke="#38bdf8" stroke-width="3" fill="none" filter="url(#glow)"/>
        <path class="hypha-line" d="M 250 220 C 320 260, 360 240, 420 225" stroke="#38bdf8" stroke-width="2" fill="none"/>
        <path class="hypha-line" d="M 190 230 C 260 290, 390 290, 460 240" stroke="#38bdf8" stroke-width="2.5" fill="none"/>

        <!-- Rising Moisture / Phosphorus Transport particles -->
        <circle class="particle-h" cx="330" cy="220" r="3" fill="#38bdf8"/>
        <circle class="particle-h" cx="370" cy="215" r="2.5" fill="#67e8f9" style="animation-delay: 1.1s"/>
        <circle class="particle-h" cx="310" cy="250" r="3" fill="#a7f3d0" style="animation-delay: 0.5s"/>

        <!-- Labels & Callouts -->
        <rect x="290" y="140" width="165" height="42" rx="6" fill="rgba(0,0,0,0.65)" stroke="#38bdf8" stroke-width="1"/>
        <text x="298" y="156" fill="#38bdf8" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">AMF HYPHAL BRIDGE</text>
        <text x="298" y="172" fill="#e0f2fe" font-family="'Inter', sans-serif" font-size="9">Translocates P &amp; capillary H₂O</text>

        <rect x="260" y="275" width="220" height="32" rx="4" fill="rgba(0,0,0,0.7)" stroke="#34d399" stroke-width="1"/>
        <text x="268" y="295" fill="#34d399" font-family="'Inter', sans-serif" font-size="10" font-weight="bold">Net Land Equivalent Ratio (LER) = 1.28</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_agroforestry_diagram() -> str:
    """Pure SVG+CSS animated scientific diagram of dryland agroforestry shelterbelt microclimate."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:12px;padding:16px;margin:0;box-shadow:0 4px 18px rgba(139,94,60,0.08);overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#8B5E3C;font-weight:800"> ANIMATED MECHANISM: DRYLAND PARKLAND AGROFORESTRY MICROCLIMATE</span>
        <span style="background:rgba(217,164,65,0.18);color:#B45309;padding:3px 9px;border-radius:10px;font-size:10px;font-weight:700">FAO Guidelines &amp; IPCC SRCCL</span>
    </div>
    <div style="font-size:12.5px;color:#4A3324;margin-bottom:12px;line-height:1.5">
        Faidherbia albida aerodynamic windbreak cuts vapor pressure deficit (VPD) by 40-50%, while deep taproots hydraulically lift subsoil water.
    </div>
    <svg viewBox="0 0 700 320" width="100%" height="280" style="background:#FFF8EC;border:1px solid rgba(169,113,66,0.2);border-radius:8px">
        <defs>
            <linearGradient id="skyAgro" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#0a1d17"/>
                <stop offset="100%" stop-color="#142e24"/>
            </linearGradient>
            <linearGradient id="subsoilGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#3b2514"/>
                <stop offset="50%" stop-color="#24170d"/>
                <stop offset="100%" stop-color="#0f293b"/> <!-- Subsoil Aquifer -->
            </linearGradient>
        </defs>

        <style>
            @keyframes windStream {
                0% { stroke-dashoffset: 200; }
                100% { stroke-dashoffset: 0; }
            }
            @keyframes leafFall {
                0% { transform: translate(0, 0) rotate(0deg); opacity: 1; }
                100% { transform: translate(45px, 90px) rotate(180deg); opacity: 0; }
            }
            @keyframes waterLift {
                0% { stroke-dashoffset: 120; }
                100% { stroke-dashoffset: 0; }
            }
            .wind-fast { stroke-dasharray: 20, 15; animation: windStream 1.6s infinite linear; }
            .wind-deflected { stroke-dasharray: 12, 12; animation: windStream 3.2s infinite linear; }
            .falling-leaf { animation: leafFall 3.8s infinite linear; }
            .water-column { stroke-dasharray: 8, 6; animation: waterLift 2s infinite linear; }
        </style>

        <!-- Sky & Atmosphere -->
        <rect x="0" y="0" width="700" height="130" fill="url(#skyAgro)"/>
        <!-- Ground / Subsoil -->
        <rect x="0" y="130" width="700" height="190" fill="url(#subsoilGrad)"/>
        <line x1="0" y1="130" x2="700" y2="130" stroke="#34d399" stroke-width="2"/>

        <!-- Deep Aquifer Reservoir Water Marker -->
        <rect x="0" y="280" width="700" height="40" fill="rgba(56,189,248,0.18)"/>
        <text x="14" y="302" fill="#38bdf8" font-family="'Fira Code', monospace" font-size="10">SUBSOIL CAPILLARY WATER RESERVOIR (>10m Depth)</text>

        <!-- High-Velocity Dry Wind Incoming (Left) -->
        <path class="wind-fast" d="M 10 30 L 140 30" stroke="#f87171" stroke-width="3.5" fill="none"/>
        <path class="wind-fast" d="M 10 60 L 140 60" stroke="#f87171" stroke-width="3" fill="none"/>
        <path class="wind-fast" d="M 10 90 L 140 90" stroke="#f87171" stroke-width="2.5" fill="none"/>
        <text x="12" y="20" fill="#f87171" font-family="'Inter', sans-serif" font-size="10" font-weight="bold">Erosive High-Velocity Wind (35-50 km/h)</text>

        <!-- Parkland Agroforestry Tree: Faidherbia albida (Center-Left) -->
        <!-- Trunk -->
        <path d="M 175 130 Q 180 80 185 45" stroke="#78350f" stroke-width="12" fill="none"/>
        <!-- Reverse Phenology Canopy (Porous Aerodynamic Filter) -->
        <ellipse cx="185" cy="40" rx="42" ry="32" fill="#047857" opacity="0.85"/>
        <ellipse cx="170" cy="35" rx="30" ry="22" fill="#10b981" opacity="0.9"/>
        <ellipse cx="205" cy="38" rx="28" ry="20" fill="#059669" opacity="0.9"/>
        <text x="145" y="10" fill="#a7f3d0" font-family="'Inter', sans-serif" font-size="11" font-weight="bold">Faidherbia albida (Windbreak)</text>

        <!-- Falling Leaf Litter Adding Soil Carbon -->
        <ellipse class="falling-leaf" cx="195" cy="55" rx="5" ry="2.5" fill="#f59e0b"/>
        <ellipse class="falling-leaf" cx="215" cy="65" rx="4" ry="2" fill="#d97706" style="animation-delay: 1.8s"/>
        <text x="215" y="120" fill="#f59e0b" font-family="'Inter', sans-serif" font-size="9.5">Annual Litter (2.5-3.5 t/ha)</text>

        <!-- Deep Taproot System (>10m) -->
        <path d="M 180 130 Q 185 200 188 290" stroke="#92400e" stroke-width="6" fill="none"/>
        <path d="M 185 190 Q 220 230 230 285" stroke="#92400e" stroke-width="3" fill="none"/>

        <!-- Hydraulic Water Lift Upward in Taproot -->
        <path class="water-column" d="M 188 285 L 180 140" stroke="#38bdf8" stroke-width="3" fill="none"/>
        <text x="80" y="240" fill="#38bdf8" font-family="'Inter', sans-serif" font-size="10" font-weight="bold">Hydraulic Water Lift</text>
        <text x="80" y="254" fill="#bae6fd" font-family="'Inter', sans-serif" font-size="9">Subsoil → Topsoil moisture</text>

        <!-- Deflected Aerodynamic Wind Profile (Elevated above crop canopy) -->
        <path class="wind-deflected" d="M 180 30 Q 230 15 320 20 Q 460 25 680 25" stroke="#34d399" stroke-width="2.5" fill="none"/>
        <path class="wind-deflected" d="M 210 60 Q 280 40 420 50 Q 560 55 680 55" stroke="#34d399" stroke-width="2" fill="none"/>

        <!-- Sheltered Calm Microclimate Crop Zone (Right) -->
        <rect x="250" y="75" width="430" height="52" rx="6" fill="rgba(52,211,153,0.08)" stroke="#34d399" stroke-width="1" stroke-dasharray="4,4"/>
        <text x="260" y="93" fill="#34d399" font-family="'Fira Code', monospace" font-size="10.5" font-weight="bold">PROTECTED MICROCLIMATE ZONE (15-20x Tree Height)</text>
        <text x="260" y="112" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">Near-surface wind speed cut by 40-60% | Evaporative VPD reduced by 30%</text>

        <!-- Protected Wheat Crops Growing Happily -->
        <g transform="translate(310, 130)">
            <line x1="0" y1="0" x2="0" y2="-35" stroke="#f59e0b" stroke-width="3"/>
            <ellipse cx="0" cy="-38" rx="4" ry="10" fill="#fbbf24"/>
        </g>
        <g transform="translate(380, 130)">
            <line x1="0" y1="0" x2="0" y2="-38" stroke="#f59e0b" stroke-width="3"/>
            <ellipse cx="0" cy="-42" rx="4" ry="11" fill="#fbbf24"/>
        </g>
        <g transform="translate(450, 130)">
            <line x1="0" y1="0" x2="0" y2="-36" stroke="#f59e0b" stroke-width="3"/>
            <ellipse cx="0" cy="-40" rx="4" ry="10" fill="#fbbf24"/>
        </g>
        <g transform="translate(520, 130)">
            <line x1="0" y1="0" x2="0" y2="-37" stroke="#f59e0b" stroke-width="3"/>
            <ellipse cx="0" cy="-40" rx="4" ry="10" fill="#fbbf24"/>
        </g>
        <g transform="translate(590, 130)">
            <line x1="0" y1="0" x2="0" y2="-35" stroke="#f59e0b" stroke-width="3"/>
            <ellipse cx="0" cy="-38" rx="4" ry="10" fill="#fbbf24"/>
        </g>

        <!-- Humus Accretion Layer in Topsoil -->
        <rect x="240" y="132" width="440" height="22" fill="rgba(52,211,153,0.16)"/>
        <text x="260" y="148" fill="#a7f3d0" font-family="'Inter', sans-serif" font-size="9.5" font-weight="bold">Rebuilt Stable Humus Pool (+0.35% to +0.55% SOC over 5 yrs)</text>
    </svg>
</div>
</body>
</html>
"""


def render_degradation_problem_diagram() -> str:
    """Animated SVG diagram showing the degradation cascade of bare monoculture."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#140e0a;border:1px solid rgba(248,113,113,0.35);border-radius:12px;padding:16px;overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
        <span style="font-family:'Fira Code',monospace;font-size:11px;color:#f87171;font-weight:700"> DIAGNOSTIC MECHANISM: CONTINUOUS MONOCULTURE DEGRADATION CASCADE</span>
        <span style="background:rgba(248,113,113,0.15);color:#f87171;padding:2px 8px;border-radius:10px;font-size:10px">IPCC SRCCL &amp; IPBES</span>
    </div>
    <div style="font-size:12px;color:#fca5a5;margin-bottom:12px">
        Visualizing how continuous cereal monoculture without residue retention causes microbial starvation, glomalin loss, soil crusting, and wind erosion.
    </div>
    <svg viewBox="0 0 700 240" width="100%" height="220" style="background:#0d0907;border-radius:8px">
        <defs>
            <linearGradient id="badSoilGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#4a3020"/>
                <stop offset="100%" stop-color="#24170d"/>
            </linearGradient>
        </defs>

        <style>
            @keyframes dustBlow {
                0% { transform: translateX(0) translateY(0); opacity: 0; }
                50% { opacity: 0.8; }
                100% { transform: translateX(120px) translateY(-30px); opacity: 0; }
            }
            .dust-particle { animation: dustBlow 2s infinite ease-out; }
        </style>

        <!-- Sky -->
        <rect x="0" y="0" width="700" height="90" fill="#1c120c"/>
        <!-- Compacted Crusted Soil -->
        <rect x="0" y="90" width="700" height="150" fill="url(#badSoilGrad)"/>
        <!-- Surface Crusting Line -->
        <line x1="0" y1="90" x2="700" y2="90" stroke="#f87171" stroke-width="4"/>

        <!-- Wind blowing topsoil dust -->
        <path d="M 20 45 L 220 45" stroke="#fbbf24" stroke-width="2.5" stroke-dasharray="10, 8"/>
        <circle class="dust-particle" cx="150" cy="85" r="3" fill="#d97706"/>
        <circle class="dust-particle" cx="210" cy="82" r="3.5" fill="#b45309" style="animation-delay: 0.7s"/>
        <circle class="dust-particle" cx="290" cy="80" r="2.5" fill="#d97706" style="animation-delay: 1.2s"/>

        <!-- Box 1: Monotypic Root -->
        <rect x="40" y="110" width="180" height="100" rx="6" fill="rgba(0,0,0,0.5)" stroke="#f87171" stroke-width="1"/>
        <text x="50" y="130" fill="#fca5a5" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">1. ROOT STARVATION</text>
        <text x="50" y="150" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">• Monotypic root exudates</text>
        <text x="50" y="168" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">• 85% AMF fungal die-off</text>
        <text x="50" y="186" fill="#f87171" font-family="'Inter', sans-serif" font-size="9.5">• Microbial biomass depleted</text>

        <!-- Arrow 1 -->
        <text x="235" y="165" fill="#f87171" font-size="20"></text>

        <!-- Box 2: Glomalin Loss -->
        <rect x="260" y="110" width="180" height="100" rx="6" fill="rgba(0,0,0,0.5)" stroke="#f87171" stroke-width="1"/>
        <text x="270" y="130" fill="#fca5a5" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">2. AGGREGATE COLLAPSE</text>
        <text x="270" y="150" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">• Fungal glomalin lost</text>
        <text x="270" y="168" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">• Macroaggregates slake</text>
        <text x="270" y="186" fill="#f87171" font-family="'Inter', sans-serif" font-size="9.5">• Bulk density >1.55 g/cm³</text>

        <!-- Arrow 2 -->
        <text x="455" y="165" fill="#f87171" font-size="20"></text>

        <!-- Box 3: Capillary Failure -->
        <rect x="480" y="110" width="190" height="100" rx="6" fill="rgba(0,0,0,0.5)" stroke="#f87171" stroke-width="1"/>
        <text x="490" y="130" fill="#fca5a5" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">3. CAPILLARY DESICCATION</text>
        <text x="490" y="150" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">• Infiltration <8 mm/hr</text>
        <text x="490" y="168" fill="#e2f0ec" font-family="'Inter', sans-serif" font-size="9.5">• 60% AWC capacity lost</text>
        <text x="490" y="186" fill="#f87171" font-family="'Inter', sans-serif" font-size="9.5">• Flash erosion & drought</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_transition_roadmap_diagram(ecosystem_type: str = "agricultural") -> str:
    """Animated SVG diagram showing the 3-phase transition bridge from degraded state to restored ecosystem."""
    eco = (ecosystem_type or "agricultural").lower()

    if eco == "forest":
        banner_title = " 3-PHASE FOREST CONNECTIVITY BRIDGE: HOW TO REACH THE CLIMAX CORRIDOR"
        citation = "Science (2020) & PNAS (2019)"
        desc = "A clear step-by-step journey: from isolated forest fragments &rarr; pioneer framework canopy &rarr; closed canopy wildlife corridor."
        
        p1_badge = "PHASE 1 (0-6 MO)"
        p1_title = " Edge Shield & Nursery"
        p1_b1 = "• Eradicate aggressive exotic lianas"
        p1_b2 = "• Establish 15m perimeter shrub buffer"
        p1_b3 = "• Arrest illegal logging & cattle incursions"
        p1_mech = "Stops desiccating winds; stabilizes interior humidity"
        p1_pool_lbl = "CANOPY CONNECTIVITY:"
        p1_pool_w = 45
        p1_pool_txt = "22% &rarr; 34%"

        p2_badge = "PHASE 2 (YR 1-3)"
        p2_title = " Structural Corridor Reconnection"
        p2_b1 = "• Plant fast-growing native pioneers at 1.8m"
        p2_b2 = "• Install 25m bird perches for seed rain"
        p2_b3 = "• Mulch tree stems with 10cm woodchips"
        p2_mech = "Frugivorous birds drop diverse wild climax seeds"
        p2_pool_lbl = "CANOPY CONNECTIVITY:"
        p2_pool_w = 110
        p2_pool_txt = "34% &rarr; 58%"

        p3_badge = "PHASE 3 (YR 3-5+)"
        p3_title = " Canopy Microclimate Climax"
        p3_b1 = "• 50–100m wide continuous canopy closed"
        p3_b2 = "• High-canopy stepping bridges linked"
        p3_b3 = "• Climax dipterocarp & fig guilds mature"
        p3_mech = "Cuts edge mortality by 60%; gene flow active"
        p3_pool_lbl = "CANOPY CONNECTIVITY:"
        p3_pool_w = 165
        p3_pool_txt = "58% &rarr; 78%+"

    elif eco == "urban":
        banner_title = " 3-PHASE URBAN BIO-RETENTION BRIDGE: RESTORING URBAN WATER QUALITY"
        citation = "EPA Stormwater & Nature Sustainability (2022)"
        desc = "A clear step-by-step journey: from impervious runoff &rarr; engineered bio-retention media &rarr; microclimate pocket forest."

        p1_badge = "PHASE 1 (0-6 MO)"
        p1_title = " Silt Sump & Swale Trench"
        p1_b1 = "• Excavate 1.0m deep bio-retention swale"
        p1_b2 = "• Install rock rip-rap energy dissipater"
        p1_b3 = "• Lay perforated PVC underdrain in gravel"
        p1_mech = "Arrests kinetic runoff & traps coarse suspended gravel"
        p1_pool_lbl = "RUNOFF PURITY / RETENTION:"
        p1_pool_w = 35
        p1_pool_txt = "15% &rarr; 38%"

        p2_badge = "PHASE 2 (YR 1-3)"
        p2_title = " Engineered Bio-Filter Media"
        p2_b1 = "• 85% sand / 10% fines / 5% compost layer"
        p2_b2 = "• Plant deep-rooting Carex sedges & rushes"
        p2_b3 = "• 50mm shredded bark filtration mulch"
        p2_mech = "Rhizosphere microbes chelate heavy metals (78%)"
        p2_pool_lbl = "RUNOFF PURITY / RETENTION:"
        p2_pool_w = 115
        p2_pool_txt = "38% &rarr; 72%"

        p3_badge = "PHASE 3 (YR 3-5+)"
        p3_title = " Miyawaki Pocket Forest"
        p3_b1 = "• Ultra-dense native tree stepping stones"
        p3_b2 = "• Cools local heat island by 3–4°C"
        p3_b3 = "• Avian foraging & insect habitat bridges"
        p3_mech = "Eliminates lake toxicity; restores urban bird paths"
        p3_pool_lbl = "RUNOFF PURITY / RETENTION:"
        p3_pool_w = 170
        p3_pool_txt = "72% &rarr; 92%+"

    elif eco == "wetland":
        banner_title = " 3-PHASE WETLAND RESTORATION BRIDGE: CONQUERING EUTROPHICATION"
        citation = "Ramsar Wetland Restoration Guidelines (2021)"
        desc = "A clear step-by-step journey: from eutrophic hypoxia &rarr; emergent macrophyte biofilter &rarr; stable littoral nursery."

        p1_badge = "PHASE 1 (0-6 MO)"
        p1_title = " Shoreline Reshaping & Armor"
        p1_b1 = "• Reshape steep undercut banks to 5:1 slope"
        p1_b2 = "• Anchor coconut coir geotextile bio-logs"
        p1_b3 = "• Halt agricultural nutrient channelization"
        p1_mech = "Stops shoreline slumping & benthic resuspension"
        p1_pool_lbl = "WATER DISSOLVED OXYGEN:"
        p1_pool_w = 40
        p1_pool_txt = "2.1 &rarr; 3.8 mg/L"

        p2_badge = "PHASE 2 (YR 1-3)"
        p2_title = " Macrophyte Biofilter Fringe"
        p2_b1 = "• Plant Cattail & Bulrush rhizomes at 40cm"
        p2_b2 = "• Establish Zone 2 deep-root tree buffer"
        p2_b3 = "• Anaerobic denitrification zone forms"
        p2_mech = "Microbes convert NO3- into harmless N2 gas (88%)"
        p2_pool_lbl = "WATER DISSOLVED OXYGEN:"
        p2_pool_w = 110
        p2_pool_txt = "3.8 &rarr; 5.8 mg/L"

        p3_badge = "PHASE 3 (YR 3-5+)"
        p3_title = " Littoral Shallows & Nursery"
        p3_b1 = "• Water clarity restored (Secchi depth >1.8m)"
        p3_b2 = "• Benthic macroinvertebrate webs reboot"
        p3_b3 = "• Waterfowl & amphibian fledging success"
        p3_mech = "Cyanobacterial blooms suppressed; DO stabilized"
        p3_pool_lbl = "WATER DISSOLVED OXYGEN:"
        p3_pool_w = 165
        p3_pool_txt = "5.8 &rarr; 7.1+ mg/L"

    else:
        # Agricultural
        banner_title = " 3-PHASE RECOVERY BRIDGE: HOW TO REACH THE SOLVED ECOSYSTEM"
        citation = "FAO Recarbonizing Soils (2019) & IPCC SRCCL"
        desc = "A clear step-by-step journey: from depleted topsoil &rarr; biological inoculation &rarr; underground hyphal mutualism &rarr; resilient agroforestry microclimate."

        p1_badge = "PHASE 1 (0-6 MO)"
        p1_title = " Ground Shield & Seed"
        p1_b1 = "• Stop inversion plowing immediately"
        p1_b2 = "• Leave 35%+ wheat stubble mulch"
        p1_b3 = "• Drill inoculated chickpea/pulse"
        p1_mech = "Buffers soil temp by 6°C; halts evaporation"
        p1_pool_lbl = "ORGANIC CARBON POOL:"
        p1_pool_w = 40
        p1_pool_txt = "0.35% &rarr; 0.42%"

        p2_badge = "PHASE 2 (YR 1-3)"
        p2_title = " Underground Symbiosis"
        p2_b1 = "• Alternate cereal & legume strips"
        p2_b2 = "• Rhizobia fixes 35-75 kg N/ha free"
        p2_b3 = "• Plant Faidherbia albida saplings"
        p2_mech = "Fungal hyphae channel locked P (LER 1.28)"
        p2_pool_lbl = "ORGANIC CARBON POOL:"
        p2_pool_w = 95
        p2_pool_txt = "0.42% &rarr; 0.58%"

        p3_badge = "PHASE 3 (YR 3-5+)"
        p3_title = " Microclimate Shield"
        p3_b1 = "• Tree canopy reverse phenology"
        p3_b2 = "• 10m deep roots lift subsoil water"
        p3_b3 = "• 2.5 t/ha leaf litter builds humus"
        p3_mech = "Cuts wind VPD 40-60%; permanent humus"
        p3_pool_lbl = "ORGANIC CARBON POOL:"
        p3_pool_w = 160
        p3_pool_txt = "0.58% &rarr; 0.85%+"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }}
  @keyframes pathFlow {{
      0% {{ stroke-dashoffset: 160; }}
      100% {{ stroke-dashoffset: 0; }}
  }}
  @keyframes pulseBadge {{
      0%, 100% {{ transform: scale(1); opacity: 0.85; }}
      50% {{ transform: scale(1.08); opacity: 1; }}
  }}
  .flow-line {{ stroke-dasharray: 8, 6; animation: pathFlow 1.6s infinite linear; }}
</style>
</head>
<body>
<div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:12px;padding:16px;margin:0;box-shadow:0 4px 18px rgba(139,94,60,0.08);overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#8B5E3C;font-weight:800">{banner_title}</span>
        <span style="background:rgba(217,164,65,0.18);color:#B45309;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:700">{citation}</span>
    </div>
    <div style="font-size:12.5px;color:#4A3324;margin-bottom:12px;line-height:1.5">
        {desc}
    </div>
    <svg viewBox="0 0 720 270" width="100%" height="260" style="background:#FFF8EC;border:1px solid rgba(169,113,66,0.2);border-radius:8px">
        <defs>
            <linearGradient id="phase1Grad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#FFFDF8"/>
                <stop offset="100%" stop-color="#FEF3C7"/>
            </linearGradient>
            <linearGradient id="phase2Grad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#FFFDF8"/>
                <stop offset="100%" stop-color="#E0F2FE"/>
            </linearGradient>
            <linearGradient id="phase3Grad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#FFFDF8"/>
                <stop offset="100%" stop-color="#ECFDF5"/>
            </linearGradient>
        </defs>

        <!-- Phase Connector Lines (Dashed Flow) -->
        <path class="flow-line" d="M 230 135 L 260 135" stroke="#D9A441" stroke-width="3" fill="none"/>
        <polygon points="260,135 250,130 250,140" fill="#D9A441"/>

        <path class="flow-line" d="M 480 135 L 510 135" stroke="#059669" stroke-width="3" fill="none"/>
        <polygon points="510,135 500,130 500,140" fill="#059669"/>

        <!-- Phase 1 Box -->
        <rect x="15" y="20" width="215" height="230" rx="8" fill="url(#phase1Grad)" stroke="#D9A441" stroke-width="1.5"/>
        <rect x="25" y="30" width="115" height="20" rx="4" fill="rgba(217,164,65,0.25)"/>
        <text x="32" y="44" fill="#92400E" font-family="'Fira Code', monospace" font-size="9.5" font-weight="bold">{p1_badge}</text>
        <text x="25" y="70" fill="#78350F" font-family="'Inter', sans-serif" font-size="12" font-weight="bold">{p1_title}</text>
        
        <text x="25" y="92" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p1_b1}</text>
        <text x="25" y="108" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p1_b2}</text>
        <text x="25" y="124" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p1_b3}</text>

        <rect x="25" y="142" width="195" height="42" rx="4" fill="#FFFDF8" stroke="rgba(169,113,66,0.2)"/>
        <text x="32" y="157" fill="#92400E" font-family="'Inter', sans-serif" font-size="9.5" font-weight="bold">Biophysical Mechanism:</text>
        <text x="32" y="173" fill="#4A3324" font-family="'Inter', sans-serif" font-size="9">{p1_mech}</text>

        <text x="25" y="202" fill="#856852" font-family="'Fira Code', monospace" font-size="9">{p1_pool_lbl}</text>
        <rect x="25" y="210" width="195" height="12" rx="3" fill="rgba(169,113,66,0.15)"/>
        <rect x="25" y="210" width="{p1_pool_w}" height="12" rx="3" fill="#D9A441"/>
        <text x="75" y="220" fill="#78350F" font-family="'Fira Code', monospace" font-size="9" font-weight="bold">{p1_pool_txt}</text>

        <!-- Phase 2 Box -->
        <rect x="260" y="20" width="220" height="230" rx="8" fill="url(#phase2Grad)" stroke="#0284C7" stroke-width="1.5"/>
        <rect x="270" y="30" width="115" height="20" rx="4" fill="rgba(2,132,199,0.18)"/>
        <text x="277" y="44" fill="#0369A1" font-family="'Fira Code', monospace" font-size="9.5" font-weight="bold">{p2_badge}</text>
        <text x="270" y="70" fill="#0369A1" font-family="'Inter', sans-serif" font-size="12" font-weight="bold">{p2_title}</text>

        <text x="270" y="92" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p2_b1}</text>
        <text x="270" y="108" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p2_b2}</text>
        <text x="270" y="124" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p2_b3}</text>

        <rect x="270" y="142" width="200" height="42" rx="4" fill="#FFFDF8" stroke="rgba(2,132,199,0.2)"/>
        <text x="277" y="157" fill="#0284C7" font-family="'Inter', sans-serif" font-size="9.5" font-weight="bold">Biophysical Mechanism:</text>
        <text x="277" y="173" fill="#4A3324" font-family="'Inter', sans-serif" font-size="9">{p2_mech}</text>

        <text x="270" y="202" fill="#856852" font-family="'Fira Code', monospace" font-size="9">{p2_pool_lbl}</text>
        <rect x="270" y="210" width="200" height="12" rx="3" fill="rgba(169,113,66,0.15)"/>
        <rect x="270" y="210" width="{p2_pool_w}" height="12" rx="3" fill="#0284C7"/>
        <text x="385" y="220" fill="#0369A1" font-family="'Fira Code', monospace" font-size="9" font-weight="bold">{p2_pool_txt}</text>

        <!-- Phase 3 Box -->
        <rect x="510" y="20" width="200" height="230" rx="8" fill="url(#phase3Grad)" stroke="#059669" stroke-width="1.5"/>
        <rect x="520" y="30" width="115" height="20" rx="4" fill="rgba(5,150,105,0.18)"/>
        <text x="527" y="44" fill="#065F46" font-family="'Fira Code', monospace" font-size="9.5" font-weight="bold">{p3_badge}</text>
        <text x="520" y="70" fill="#065F46" font-family="'Inter', sans-serif" font-size="12" font-weight="bold">{p3_title}</text>

        <text x="520" y="92" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p3_b1}</text>
        <text x="520" y="108" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p3_b2}</text>
        <text x="520" y="124" fill="#382417" font-family="'Inter', sans-serif" font-size="10">{p3_b3}</text>

        <rect x="520" y="142" width="180" height="42" rx="4" fill="#FFFDF8" stroke="rgba(5,150,105,0.2)"/>
        <text x="527" y="157" fill="#059669" font-family="'Inter', sans-serif" font-size="9.5" font-weight="bold">Biophysical Mechanism:</text>
        <text x="527" y="173" fill="#4A3324" font-family="'Inter', sans-serif" font-size="9">{p3_mech}</text>

        <text x="520" y="202" fill="#856852" font-family="'Fira Code', monospace" font-size="9">{p3_pool_lbl}</text>
        <rect x="520" y="210" width="180" height="12" rx="3" fill="rgba(169,113,66,0.15)"/>
        <rect x="520" y="210" width="{p3_pool_w}" height="12" rx="3" fill="#059669"/>
        <text x="625" y="220" fill="#065F46" font-family="'Fira Code', monospace" font-size="9" font-weight="bold">{p3_pool_txt}</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_forest_corridor_diagram() -> str:
    """Animated SVG diagram of Forest Wildlife Corridor & Canopy Stepping Bridges."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
  @keyframes flightFly {
      0% { transform: translateX(0) translateY(0); opacity: 0.2; }
      50% { opacity: 1; transform: translateX(220px) translateY(-18px); }
      100% { transform: translateX(450px) translateY(0); opacity: 0.2; }
  }
  .bird-flight { animation: flightFly 4.5s infinite linear; }
</style>
</head>
<body>
<div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:12px;padding:16px;margin:0;box-shadow:0 4px 18px rgba(139,94,60,0.08);overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#8B5E3C;font-weight:800"> ANIMATED MECHANISM: FOREST WILDLIFE CORRIDOR &amp; CANOPY BRIDGES</span>
        <span style="background:rgba(217,164,65,0.18);color:#B45309;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:700">Science (2020) &amp; PNAS (2019)</span>
    </div>
    <div style="font-size:12.5px;color:#4A3324;margin-bottom:12px;line-height:1.5">
        Continuous 50–100m native canopy bridge reconnecting isolated core patches, eliminating edge microclimate desiccation and enabling interior gene flow.
    </div>
    <svg viewBox="0 0 700 280" width="100%" height="260" style="background:#FFF8EC;border:1px solid rgba(169,113,66,0.2);border-radius:8px">
        <!-- Sky -->
        <rect x="0" y="0" width="700" height="90" fill="#FEF3C7"/>
        <!-- Soil Ground -->
        <rect x="0" y="90" width="700" height="190" fill="#78350F"/>
        <line x1="0" y1="90" x2="700" y2="90" stroke="#92400E" stroke-width="2"/>

        <!-- Core A Left -->
        <rect x="10" y="20" width="130" height="70" rx="6" fill="#ECFDF5" stroke="#059669" stroke-width="2"/>
        <text x="75" y="48" fill="#065F46" font-family="'Fira Code', monospace" font-size="11" font-weight="bold" text-anchor="middle">FOREST CORE A</text>
        <text x="75" y="66" fill="#047857" font-size="9" text-anchor="middle">Climax Old Growth</text>

        <!-- Core B Right -->
        <rect x="560" y="20" width="130" height="70" rx="6" fill="#ECFDF5" stroke="#059669" stroke-width="2"/>
        <text x="625" y="48" fill="#065F46" font-family="'Fira Code', monospace" font-size="11" font-weight="bold" text-anchor="middle">FOREST CORE B</text>
        <text x="625" y="66" fill="#047857" font-size="9" text-anchor="middle">Isolated Population</text>

        <!-- Connecting Trees -->
        <g transform="translate(180, 90)">
            <rect x="-6" y="-30" width="12" height="30" fill="#5c381e"/>
            <circle cx="0" cy="-45" r="24" fill="#047857"/>
        </g>
        <g transform="translate(260, 90)">
            <rect x="-7" y="-40" width="14" height="40" fill="#5c381e"/>
            <circle cx="0" cy="-58" r="30" fill="#059669"/>
        </g>
        <g transform="translate(350, 90)">
            <rect x="-8" y="-46" width="16" height="46" fill="#5c381e"/>
            <circle cx="0" cy="-68" r="36" fill="#10b981"/>
        </g>
        <g transform="translate(440, 90)">
            <rect x="-7" y="-40" width="14" height="40" fill="#5c381e"/>
            <circle cx="0" cy="-58" r="30" fill="#059669"/>
        </g>
        <g transform="translate(520, 90)">
            <rect x="-6" y="-30" width="12" height="30" fill="#5c381e"/>
            <circle cx="0" cy="-45" r="24" fill="#047857"/>
        </g>

        <!-- Animated Bird Flight Path -->
        <path d="M 120 40 Q 350 -15 580 40" stroke="#D9A441" stroke-width="2.5" stroke-dasharray="6,5" fill="none"/>
        <g class="bird-flight">
            <polygon points="120,40 112,48 128,48" fill="#D97706"/>
        </g>
        <text x="350" y="18" fill="#92400E" font-family="'Inter', sans-serif" font-size="10.5" font-weight="bold" text-anchor="middle">AVIAN &amp; MAMMAL GENETIC HIGHWAY</text>

        <!-- Subsoil Root Network & Mycelium -->
        <path d="M 140 160 Q 350 210 560 160" stroke="#0284C7" stroke-width="2" stroke-dasharray="4,4" fill="none"/>
        <text x="350" y="195" fill="#BAE6FD" font-family="'Fira Code', monospace" font-size="9.5" text-anchor="middle">SUBTERRANEAN ECTOMYCORRHIZAL HYPHAE NETWORK (---)</text>

        <!-- Microclimate Buffer Callout -->
        <rect x="180" y="220" width="340" height="38" rx="6" fill="#FFFDF8" stroke="#059669" stroke-width="1.5"/>
        <text x="350" y="236" fill="#065F46" font-size="10" font-weight="bold" text-anchor="middle">50-100m CONTINUOUS CANOPY CORRIDOR</text>
        <text x="350" y="250" fill="#4A3324" font-size="9" text-anchor="middle">Edge desiccation drops 60%; interior species richness increases +110%</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_forest_stratification_diagram() -> str:
    """Animated SVG diagram showing multi-strata vertical forest architecture."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#FFFDF8;border:1.5px solid rgba(169,113,66,0.28);border-radius:12px;padding:16px;margin:0;box-shadow:0 4px 18px rgba(139,94,60,0.08);overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#8B5E3C;font-weight:800"> VERTICAL CANOPY STRATIFICATION &amp; INTERIOR MICROCLIMATE</span>
        <span style="background:rgba(217,164,65,0.18);color:#B45309;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:700">IUCN Forest Restoration Protocols</span>
    </div>
    <div style="font-size:12.5px;color:#4A3324;margin-bottom:12px;line-height:1.5">
        Assisted Natural Regeneration creates a 3-tier microclimate buffer: Emergent Climax (>25m), Mid-Story Sub-Canopy, and Humid Understory Shrub layer.
    </div>
    <svg viewBox="0 0 700 280" width="100%" height="260" style="background:#FFF8EC;border:1px solid rgba(169,113,66,0.2);border-radius:8px">
        <!-- Strata Lines -->
        <line x1="0" y1="80" x2="700" y2="80" stroke="rgba(169,113,66,0.2)" stroke-width="1" stroke-dasharray="4,4"/>
        <line x1="0" y1="160" x2="700" y2="160" stroke="rgba(169,113,66,0.2)" stroke-width="1" stroke-dasharray="4,4"/>
        <line x1="0" y1="230" x2="700" y2="230" stroke="#78350F" stroke-width="2"/>
        <rect x="0" y="230" width="700" height="50" fill="#78350F"/>

        <!-- Strata Labels -->
        <text x="20" y="46" fill="#047857" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">TIER 1: EMERGENT CLIMAX (>25m)</text>
        <text x="20" y="62" fill="#4A3324" font-size="8.5">Direct solar capture &amp; windbreak shield</text>

        <text x="20" y="122" fill="#0284C7" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">TIER 2: MID-STORY CANOPY (10-20m)</text>
        <text x="20" y="138" fill="#4A3324" font-size="8.5">Fruit &amp; nectar guilds for canopy birds</text>

        <text x="20" y="192" fill="#B45309" font-family="'Fira Code', monospace" font-size="10" font-weight="bold">TIER 3: HUMID UNDERSTORY (0-5m)</text>
        <text x="20" y="208" fill="#4A3324" font-size="8.5">High humidity, mosses, amphibians, humus</text>

        <!-- Emergent Tree Center -->
        <rect x="340" y="60" width="20" height="170" fill="#5c381e"/>
        <ellipse cx="350" cy="40" rx="90" ry="32" fill="rgba(5,150,105,0.2)" stroke="#059669" stroke-width="2"/>
        <text x="350" y="44" fill="#065F46" font-size="10" font-weight="bold" text-anchor="middle">Shorea / Dipterocarp Climax</text>

        <!-- Mid-story trees -->
        <rect x="210" y="130" width="12" height="100" fill="#4d301c"/>
        <circle cx="216" cy="115" r="30" fill="rgba(2,132,199,0.2)" stroke="#0284C7" stroke-width="1.8"/>
        <text x="216" y="118" fill="#0369A1" font-size="8.5" text-anchor="middle">Ficus</text>

        <rect x="480" y="130" width="12" height="100" fill="#4d301c"/>
        <circle cx="486" cy="115" r="30" fill="rgba(2,132,199,0.2)" stroke="#0284C7" stroke-width="1.8"/>
        <text x="486" y="118" fill="#0369A1" font-size="8.5" text-anchor="middle">Syzygium</text>

        <!-- Understory shrubs -->
        <circle cx="280" cy="205" r="16" fill="rgba(217,164,65,0.25)" stroke="#D9A441" stroke-width="1.5"/>
        <circle cx="420" cy="205" r="16" fill="rgba(217,164,65,0.25)" stroke="#D9A441" stroke-width="1.5"/>
    </svg>
</div>
</body>
</html>
"""


def render_animated_urban_bioswale_diagram() -> str:
    """Animated SVG diagram of Urban Vegetated Bio-Retention Swale Filter."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
  @keyframes runoffFlow {
      0% { transform: translateX(0); opacity: 0.3; }
      50% { opacity: 1; }
      100% { transform: translateX(110px); opacity: 0.1; }
  }
  .runoff-arrow { animation: runoffFlow 2s infinite ease-out; }
</style>
</head>
<body>
<div style="background:#091512;border:1.5px solid rgba(52,211,153,0.35);border-radius:12px;padding:16px;margin:0;overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#38bdf8;font-weight:700"> ANIMATED MECHANISM: URBAN BIO-RETENTION SWALE &amp; POLLUTANT FILTER</span>
        <span style="background:rgba(56,189,248,0.18);color:#38bdf8;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:600">EPA Stormwater Design Standards</span>
    </div>
    <div style="font-size:12px;color:#a7d2c7;margin-bottom:12px;line-height:1.5">
        Capturing urban street runoff, trapping suspended solids (TSS), biological chelation of heavy metals, and discharging purified water to urban water bodies.
    </div>
    <svg viewBox="0 0 700 280" width="100%" height="260" style="background:#06100d;border-radius:8px">
        <!-- Concrete Curbs -->
        <path d="M 0 70 L 120 70 L 150 110 L 550 110 L 580 70 L 700 70 L 700 280 L 0 280 Z" fill="#1c2b26"/>

        <!-- Swale Filter Media Layers -->
        <rect x="150" y="105" width="400" height="25" fill="#3d2918" stroke="#523924"/>
        <text x="350" y="122" fill="#facc15" font-family="'Fira Code', monospace" font-size="9" font-weight="bold" text-anchor="middle">50mm HARDWOOD BARK MULCH (Hydrocarbon Trap)</text>

        <rect x="150" y="130" width="400" height="60" fill="#473e35" stroke="#5e5347"/>
        <text x="350" y="165" fill="#38bdf8" font-family="'Fira Code', monospace" font-size="10" font-weight="bold" text-anchor="middle">BIO-RETENTION MEDIA (85% Sand, 10% Fines, 5% Compost)</text>

        <rect x="150" y="190" width="400" height="30" fill="#2d3748"/>
        <text x="350" y="210" fill="#94a3b8" font-family="'Fira Code', monospace" font-size="9" text-anchor="middle">PEA GRAVEL CHOKE LAYER (5mm Aggregate)</text>

        <!-- Underdrain Pipe -->
        <rect x="150" y="220" width="400" height="50" fill="#1e293b"/>
        <circle cx="350" cy="245" r="16" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
        <text x="350" y="249" fill="#38bdf8" font-size="9" font-weight="bold" text-anchor="middle">DRAIN</text>
        <text x="460" y="250" fill="#38bdf8" font-size="9">PURIFIED DISCHARGE TO LAKE</text>

        <!-- Hydrophytes on top -->
        <path d="M 230 105 L 230 55 M 220 80 Q 230 65 240 80" stroke="#34d399" stroke-width="2.5"/>
        <circle cx="230" cy="52" r="4" fill="#a7f3d0"/>
        <path d="M 310 105 L 310 45 M 300 70 Q 310 55 320 70" stroke="#34d399" stroke-width="3"/>
        <circle cx="310" cy="42" r="5" fill="#38bdf8"/>
        <path d="M 390 105 L 390 40 M 380 65 Q 390 50 400 65" stroke="#34d399" stroke-width="3"/>
        <circle cx="390" cy="37" r="5" fill="#f43f5e"/>
        <path d="M 470 105 L 470 50 M 460 75 Q 470 60 480 75" stroke="#34d399" stroke-width="2.5"/>
        <circle cx="470" cy="47" r="4" fill="#a7f3d0"/>

        <!-- Inflow arrow -->
        <path d="M 30 55 L 125 55 M 110 48 L 125 55 L 110 62" stroke="#f87171" stroke-width="3.5" fill="none"/>
        <text x="75" y="45" fill="#f87171" font-size="9.5" font-weight="bold">DIRTY RUNOFF</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_urban_pocket_forest_diagram() -> str:
    """Animated SVG diagram of Ultra-Dense Miyawaki Pocket Forest."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#091512;border:1.5px solid rgba(52,211,153,0.35);border-radius:12px;padding:16px;margin:0;overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#34d399;font-weight:700"> URBAN MIYAWAKI POCKET FOREST &amp; HEAT ISLAND SHIELD</span>
        <span style="background:rgba(52,211,153,0.18);color:#34d399;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:600">Nature Sustainability (2022)</span>
    </div>
    <div style="font-size:12px;color:#a7d2c7;margin-bottom:12px;line-height:1.5">
        Ultra-dense planting (30 native species, 3 trees/m²) grows 10x faster, creating a cool microclimate thermal shield and stepping stones for urban wildlife.
    </div>
    <svg viewBox="0 0 700 280" width="100%" height="260" style="background:#06100d;border-radius:8px">
        <!-- City Skyline Background -->
        <rect x="40" y="40" width="60" height="180" fill="#14211d"/>
        <rect x="120" y="20" width="70" height="200" fill="#0f1916"/>
        <rect x="520" y="30" width="75" height="190" fill="#0f1916"/>
        <rect x="610" y="60" width="65" height="160" fill="#14211d"/>

        <!-- Ground Line -->
        <line x1="0" y1="220" x2="700" y2="220" stroke="#34d399" stroke-width="2"/>
        <rect x="0" y="220" width="700" height="60" fill="#1a2722"/>

        <!-- Pocket Forest Center (200 to 500) -->
        <ellipse cx="350" cy="130" rx="140" ry="85" fill="rgba(52,211,153,0.25)" stroke="#34d399" stroke-width="2"/>
        <!-- Multi-tree trunks -->
        <rect x="250" y="140" width="8" height="80" fill="#5c381e"/>
        <circle cx="254" cy="120" r="28" fill="#047857"/>
        <rect x="310" y="110" width="10" height="110" fill="#5c381e"/>
        <circle cx="315" cy="85" r="38" fill="#10b981"/>
        <rect x="380" y="120" width="10" height="100" fill="#5c381e"/>
        <circle cx="385" cy="95" r="34" fill="#059669"/>
        <rect x="440" y="145" width="8" height="75" fill="#5c381e"/>
        <circle cx="444" cy="125" r="26" fill="#047857"/>

        <!-- Microclimate Cooling Callout -->
        <rect x="220" y="235" width="260" height="35" rx="6" fill="#132a22" stroke="#38bdf8" stroke-width="1"/>
        <text x="350" y="250" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">URBAN THERMAL SHIELD (-3.5°C to -5.2°C)</text>
        <text x="350" y="262" fill="#cbd5e1" font-size="8.5" text-anchor="middle">Ultra-dense canopy captures particulate matter &amp; buffers heat</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_wetland_buffer_diagram() -> str:
    """Animated SVG diagram of Multi-Tier Wetland Riparian Macrophyte Biofilter."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#091512;border:1.5px solid rgba(52,211,153,0.35);border-radius:12px;padding:16px;margin:0;overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#38bdf8;font-weight:700"> ANIMATED MECHANISM: MULTI-TIER WETLAND MACROPHYTE BIOFILTER</span>
        <span style="background:rgba(56,189,248,0.18);color:#38bdf8;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:600">Ramsar Guidelines (2021)</span>
    </div>
    <div style="font-size:12px;color:#a7d2c7;margin-bottom:12px;line-height:1.5">
        3-tier biofilter: Dense grass buffer captures sediment &rarr; riparian trees drive microbial denitrification &rarr; emergent cattails/reeds absorb phosphates.
    </div>
    <svg viewBox="0 0 700 280" width="100%" height="260" style="background:#06100d;border-radius:8px">
        <!-- Slope Ground down to Lake -->
        <path d="M 0 80 L 220 100 L 440 140 L 700 170 L 700 280 L 0 280 Z" fill="#2d1c10"/>
        <!-- Lake Water -->
        <rect x="440" y="140" width="260" height="140" fill="rgba(56,189,248,0.22)"/>
        <line x1="440" y1="140" x2="700" y2="140" stroke="#38bdf8" stroke-width="2.5"/>

        <!-- Zone 1: Grass -->
        <text x="110" y="25" fill="#facc15" font-family="'Fira Code', monospace" font-size="10" font-weight="bold" text-anchor="middle">ZONE 1: GRASS STRIP</text>
        <path d="M 50 85 L 50 55 M 90 88 L 90 52 M 140 92 L 140 58 M 190 97 L 190 60" stroke="#eab308" stroke-width="3"/>

        <!-- Zone 2: Trees -->
        <text x="330" y="25" fill="#34d399" font-family="'Fira Code', monospace" font-size="10" font-weight="bold" text-anchor="middle">ZONE 2: DEEP-ROOT BUFFER</text>
        <rect x="280" y="70" width="12" height="45" fill="#5c381e"/>
        <circle cx="286" cy="55" r="28" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2"/>
        <rect x="380" y="90" width="12" height="48" fill="#5c381e"/>
        <circle cx="386" cy="75" r="32" fill="rgba(52,211,153,0.3)" stroke="#34d399" stroke-width="2"/>
        <!-- Denitrification Roots -->
        <path d="M 286 115 L 286 210 M 386 138 L 386 230" stroke="#10b981" stroke-width="3"/>

        <!-- Zone 3: Reeds in Water -->
        <text x="560" y="25" fill="#38bdf8" font-family="'Fira Code', monospace" font-size="10" font-weight="bold" text-anchor="middle">ZONE 3: EMERGENT REEDS</text>
        <path d="M 480 155 L 480 105 M 530 160 L 530 100 M 590 165 L 590 110" stroke="#34d399" stroke-width="3.5"/>
        <circle cx="480" cy="102" r="4" fill="#854d0e"/>
        <circle cx="530" cy="97" r="4" fill="#854d0e"/>
        <circle cx="590" cy="107" r="4" fill="#854d0e"/>

        <!-- Info callout -->
        <rect x="230" y="235" width="280" height="35" rx="6" fill="#132a22" stroke="#38bdf8" stroke-width="1"/>
        <text x="370" y="250" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">DENITRIFICATION &amp; PHOSPHATE STRIP</text>
        <text x="370" y="262" fill="#cbd5e1" font-size="8.5" text-anchor="middle">88% of nitrates converted to N2; dissolved oxygen rises to >6.5 mg/L</text>
    </svg>
</div>
</body>
</html>
"""


def render_animated_wetland_hydro_sill_diagram() -> str:
    """Animated SVG diagram of Wetland Rock Grade-Control Sills & Hydrological Shallows."""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; }
</style>
</head>
<body>
<div style="background:#091512;border:1.5px solid rgba(52,211,153,0.35);border-radius:12px;padding:16px;margin:0;overflow:hidden">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:'Fira Code',monospace;font-size:11.5px;color:#38bdf8;font-weight:700"> HYDROLOGICAL GRADE-CONTROL SILL &amp; LITTORAL SHALLOWS</span>
        <span style="background:rgba(56,189,248,0.18);color:#38bdf8;padding:3px 9px;border-radius:12px;font-size:10px;font-weight:600">Ramsar Wetland Engineering Standards</span>
    </div>
    <div style="font-size:12px;color:#a7d2c7;margin-bottom:12px;line-height:1.5">
        Loose-rock grade sills arrest dry-season lake drawdown, maintaining critical 15–40cm littoral breeding shallows for waterfowl and amphibians.
    </div>
    <svg viewBox="0 0 700 280" width="100%" height="260" style="background:#06100d;border-radius:8px">
        <!-- Bed Profile -->
        <path d="M 0 130 L 320 130 L 370 170 L 700 170 L 700 280 L 0 280 Z" fill="#2d1c10"/>
        
        <!-- Retained Water Pool Left -->
        <rect x="0" y="80" width="340" height="50" fill="rgba(56,189,248,0.35)"/>
        <line x1="0" y1="80" x2="340" y2="80" stroke="#38bdf8" stroke-width="2.5"/>
        <text x="160" y="65" fill="#38bdf8" font-family="'Fira Code', monospace" font-size="10" font-weight="bold" text-anchor="middle">STABILIZED LITTORAL NURSERY POOL (30-50cm)</text>

        <!-- Lower Outflow Water Right -->
        <rect x="370" y="145" width="330" height="25" fill="rgba(56,189,248,0.2)"/>
        <line x1="370" y1="145" x2="700" y2="145" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3"/>

        <!-- Rock Grade Sill Center (320 to 370) -->
        <path d="M 320 130 L 340 78 L 370 170 Z" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>
        <circle cx="330" cy="110" r="10" fill="#64748b"/>
        <circle cx="345" cy="95" r="12" fill="#475569"/>
        <circle cx="340" cy="125" r="14" fill="#334155"/>
        <circle cx="355" cy="140" r="11" fill="#64748b"/>
        <text x="345" y="60" fill="#facc15" font-family="'Fira Code', monospace" font-size="9.5" font-weight="bold" text-anchor="middle">ROCK GRADE SILL</text>

        <!-- Waterfowl Swimming -->
        <ellipse cx="120" cy="74" rx="14" ry="7" fill="#f8fafc"/>
        <circle cx="132" cy="68" r="4.5" fill="#f8fafc"/>
        <polygon points="136,68 142,70 136,72" fill="#f59e0b"/>

        <!-- Info callout -->
        <rect x="180" y="235" width="340" height="35" rx="6" fill="#132a22" stroke="#38bdf8" stroke-width="1"/>
        <text x="350" y="250" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">WATER TABLE ANCHOR: HALTS LITTORAL DRYING</text>
        <text x="350" y="262" fill="#cbd5e1" font-size="8.5" text-anchor="middle">Maintains perennial breeding shallows even during severe dry season</text>
    </svg>
</div>
</body>
</html>
"""

