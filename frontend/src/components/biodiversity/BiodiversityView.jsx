import React from 'react';
import {
  EcologicalBalanceRadarChart,
  FiveYearRecoveryTrajectoryChart
} from '../charts/EnvironmentalCharts';

export default function BiodiversityView({
  caseFile = {},
  ruleMetrics = {},
  onNavigateTab
}) {
  const profile = caseFile.profile || {};
  const eco = (profile.ecosystem_type || ruleMetrics?.ecosystem_type || 'agricultural').toLowerCase();

  return (
    <div className="biodiversity-view-container">
      {/* Header Banner */}
      <div className="section-header-box">
        <div>
          <h2>🧬 BIODIVERSITY & HABITAT INTEGRITY ANALYSIS</h2>
          <p className="section-subtitle">
            Quantitative multi-metric ecological indicators, trophic connectivity, and calibrated 5-year recovery projection.
          </p>
        </div>
        <div className="eco-pill-large">
          <span>ECOSYSTEM: <strong>{eco.toUpperCase()}</strong></span>
        </div>
      </div>

      {/* Main Charts Grid */}
      <div className="bio-charts-grid">
        {/* Radar Chart: Ecological Balance */}
        <div className="dash-card">
          <div className="card-header-clean">
            <span className="card-title">ECOLOGICAL EQUILIBRIUM RADAR</span>
            <span className="card-tag">5-AXIS INDICATOR</span>
          </div>
          <EcologicalBalanceRadarChart profile={profile} ruleMetrics={ruleMetrics} />
          <div className="chart-caption-text">
            Radar mapping highlights the severity of structural deficit across five interdependent environmental axes comparing current baseline (red) to peer-reviewed target (green).
          </div>
        </div>

        {/* Line Chart: 5-Year Trajectory */}
        <div className="dash-card">
          <div className="card-header-clean">
            <span className="card-title">5-YEAR RECOVERY TRAJECTORY</span>
            <span className="card-tag">BIOPHYSICAL MODEL</span>
          </div>
          <FiveYearRecoveryTrajectoryChart profile={profile} ruleMetrics={ruleMetrics} />
          <div className="chart-caption-text">
            Calibrated recovery projection demonstrating non-linear gains following phase-by-phase biophysical remediation protocols.
          </div>
        </div>
      </div>

      {/* Detailed Biophysical Diagnosis Cards */}
      <div className="bio-mechanism-section">
        <div className="dash-card mechanism-highlight-card">
          <div className="card-header-clean">
            <span className="card-title">🔬 BIOPHYSICAL MECHANISM: STRUCTURAL FRAGMENTATION & DEGRADATION</span>
            <span className="card-tag citation-tag">SCIENCE &amp; FAO SOFO</span>
          </div>

          <div className="mechanism-content">
            {eco === 'forest' ? (
              <>
                <p className="mechanism-paragraph">
                  <strong>Scientific Diagnosis (Science &amp; FAO State of the World's Forests - SOFO)</strong>:
                  Canopy perforation and anthropogenic clearcut matrices rupture contiguous microclimatic humidity buffers, permitting high-velocity advective drying and elevating vapor-pressure deficit (VPD) up to 200 meters into interior forest fragments.
                  Moisture-sensitive climax canopy species with narrow hydraulic safety margins undergo acute xylem cavitation, driving perimeter tree mortality up to 65% above core baseline levels.
                  Simultaneously, extensive structural canopy gaps establish insurmountable behavioral and physical dispersal barriers for forest-interior avifauna and arboreal taxa, precipitating genetic bottlenecking and trophic decoupling.
                </p>

                <div className="mechanism-breakdown-grid">
                  <div className="mechanism-col">
                    <span className="col-label">HYDRAULIC CAVITATION</span>
                    <p className="col-text">Moisture-sensitive primary canopy trees experience continuous negative xylem pressure, causing embolism and hydraulic pathway collapse.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">EDGE DESICCATION PENETRATION</span>
                    <p className="col-text">High-velocity agricultural winds blow through perimeter breaks, heating interior forest microclimates by 4–7°C.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">GENETIC BOTTLENECK</span>
                    <p className="col-text">Canopy fragmentation creates absolute physical flight barriers for specialized interior bird and pollinator species.</p>
                  </div>
                </div>
              </>
            ) : eco === 'urban' ? (
              <>
                <p className="mechanism-paragraph">
                  <strong>Scientific Diagnosis (EPA Urban Green Infrastructure &amp; Nature Sustainability)</strong>:
                  Extensive impervious surfaces truncate subterranean hydrologic infiltration, converting rainfall into high-velocity surface runoff contaminated with suspended sediments (&gt;120 mg/L TSS) and heavy metal particulates (Pb, Zn, Cu).
                  Lack of multi-tier vegetative canopies intensifies urban heat island effects, suppressing pollinator stepping-stone pathways and elevating water temperatures in municipal catchments.
                </p>
                <div className="mechanism-breakdown-grid">
                  <div className="mechanism-col">
                    <span className="col-label">URBAN HEAT ISLAND</span>
                    <p className="col-text">Asphalt surfaces reach 48°C, preventing cooling nighttime dew formation and driving away native pollinators.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">HYDROLOGIC BYPASS</span>
                    <p className="col-text">Flash runoff bypasses soil aquifers, generating localized flash floods and eroding urban streambanks.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">POLLUTANT PLUME</span>
                    <p className="col-text">Unfiltered stormwater runoff flushes automotive hydrocarbons and heavy metals directly into aquatic systems.</p>
                  </div>
                </div>
              </>
            ) : eco === 'wetland' ? (
              <>
                <p className="mechanism-paragraph">
                  <strong>Scientific Diagnosis (Ramsar Convention &amp; Ecological Engineering)</strong>:
                  Unbuffered diffuse nutrient inflows trigger severe stoichiometric imbalances (N:P &lt; 16:1), fueling dense Microcystis cyanobacterial blooms. Subsequent biomass senescence creates overwhelming biological oxygen demand (BOD), causing benthic dissolved oxygen to collapse below 2.0 mg/L and terminating macroinvertebrate food webs.
                </p>
                <div className="mechanism-breakdown-grid">
                  <div className="mechanism-col">
                    <span className="col-label">BENTHIC HYPOXIA</span>
                    <p className="col-text">Dissolved oxygen depletion below 2.0 mg/L suffocates benthic larvae and forces fish kill events.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">CYANOBACTERIAL TOXINS</span>
                    <p className="col-text">Microcystin toxins inhibit submerged aquatic vegetation (SAV) germination and endanger waterfowl.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">LITTORAL DESICCATION</span>
                    <p className="col-text">Artificial lake drainage desiccates shallow breeding pools before amphibian metamorphosis concludes.</p>
                  </div>
                </div>
              </>
            ) : (
              <>
                <p className="mechanism-paragraph">
                  <strong>Scientific Diagnosis (IPCC SRCCL Ch4 &amp; FAO Recarbonizing Global Soils)</strong>:
                  Continuous cereal monocropping without biomass return starves the soil microbiome of critical root exudates. Repeated inversion plowing shears arbuscular mycorrhizal fungal (AMF) hyphae, halting biological glomalin secretion. Soil aggregates slake under rainfall, driving bulk density above 1.50 g/cm³ and collapsing available water capacity by 55%.
                </p>
                <div className="mechanism-breakdown-grid">
                  <div className="mechanism-col">
                    <span className="col-label">GLOMALIN DEPLETION</span>
                    <p className="col-text">AMF hyphal loss collapses the organic glycoprotein glue required to bind microaggregates into crumbs.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">SURFACE CRUSTING</span>
                    <p className="col-text">Compacted soil caps prevent seed penetration and reduce water infiltration to less than 8 mm/hr.</p>
                  </div>
                  <div className="mechanism-col">
                    <span className="col-label">CAPILLARY DROUGHT</span>
                    <p className="col-text">Loss of pore space means soil cannot store capillary water, triggering drought wilting within 5 days of rainfall.</p>
                  </div>
                </div>
              </>
            )}
          </div>

          <div className="mechanism-footer">
            <button
              className="btn-dash-primary"
              onClick={() => onNavigateTab('recommendations')}
            >
              🚀 View Targeted Ecosystem Restoration Prescriptions →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
