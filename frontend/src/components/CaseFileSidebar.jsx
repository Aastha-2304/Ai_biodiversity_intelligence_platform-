import React from 'react';

/**
 * CaseFileSidebar — Live Environmental Case File & Telemetry Dashboard
 */
export default function CaseFileSidebar({ caseFile, ruleMetrics, retrievedEvidence, onResetCase, isLoading }) {
  const profile = caseFile?.profile || {};
  const provenance = caseFile?.provenance || {};

  const biome = profile.biome || '—';
  const soc = profile.soc_percent ?? null;
  const rainfall = profile.rainfall_mm ?? null;
  const ph = profile.ph ?? null;
  const crop = profile.current_crop || '—';

  const socMetrics = ruleMetrics?.soc_metrics || null;
  const aridityMetrics = ruleMetrics?.aridity_metrics || null;
  const bioMetrics = ruleMetrics?.biodiversity_metrics || null;
  const limitingFactors = ruleMetrics?.primary_limiting_factors || [];
  const healthIndex = ruleMetrics?.system_health_index ?? null;

  const FIELD_SPECS = ['biome', 'rainfall_mm', 'soc_percent', 'current_crop', 'irrigation_status', 'ph'];
  const filledFields = FIELD_SPECS.filter(f => profile[f] != null).length;
  const completenessPct = Math.round((filledFields / FIELD_SPECS.length) * 100);

  const getSourceBadge = (field) => {
    const prov = provenance[field];
    if (!prov) return null;
    const src = prov.source || 'unknown';
    const isHighConf = src.includes('measured') || src.includes('json');
    return (
      <span className={`source-badge ${isHighConf ? 'measured' : 'reported'}`}>
        {isHighConf ? ' Measured' : ' Reported'}
      </span>
    );
  };

  const handleExportCase = () => {
    if (!window.jspdf) {
      alert("PDF generator not loaded yet. Please wait a moment.");
      return;
    }
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text("Darukaa.Earth - Case File Report", 15, 20);
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);
    let y = 35;
    
    doc.text(`Case ID: ${caseFile?.case_id || 'SESSION'}`, 15, y); y += 10;
    doc.text(`System Health Index: ${healthIndex != null ? healthIndex : 'N/A'}/100`, 15, y); y += 10;
    
    doc.setFont("helvetica", "bold");
    doc.text("Environmental Profile:", 15, y); y += 10;
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    if (caseFile?.profile) {
      for (const [key, value] of Object.entries(caseFile.profile)) {
        if (value != null && value !== '') {
          const text = `${key}: ${value}`;
          if (y > 270) { doc.addPage(); y = 20; }
          doc.text(text, 20, y); y += 7;
        }
      }
    }
    
    doc.save(`darukaa-case-${caseFile?.case_id || 'session'}.pdf`);
  };

  return (
    <aside className="case-file-sidebar">
      {/* Header */}
      <div className="sidebar-header">
        <div className="sidebar-title-row">
          <span className="sidebar-icon"></span>
          <div>
            <div className="sidebar-title">CASE FILE</div>
            <div className="sidebar-session-id">#{caseFile?.case_id || 'SESSION'}</div>
          </div>
          <div className={`health-badge ${(healthIndex || 0) < 40 ? 'critical' : (healthIndex || 0) < 70 ? 'moderate' : 'good'}`}>
            {healthIndex != null ? `${healthIndex}/100` : 'N/A'}
          </div>
        </div>

        {/* Running Assessment */}
        {caseFile?.running_assessment && (
          <div className="running-assessment-mini">
            <div className="ra-mini-label">ASSESSMENT:</div>
            <div className="ra-mini-text">{caseFile.running_assessment}</div>
          </div>
        )}

        {/* Completeness Progress Bar */}
        <div className="completeness-bar-wrapper">
          <div className="completeness-bar-track">
            <div
              className="completeness-bar-fill"
              style={{
                width: `${completenessPct}%`,
                backgroundColor:
                  completenessPct < 40 ? 'var(--accent-red)' :
                  completenessPct < 70 ? 'var(--accent-amber)' : 'var(--accent-emerald)'
              }}
            />
          </div>
          <div className="metric-caption">
            Diagnostic Completeness: <strong>{completenessPct}%</strong> ({filledFields}/6 core dimensions)
          </div>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="sidebar-scrollable-content">
        {/* Section 1: Eco-Region & Climate */}
        <div className="notebook-card">
          <div className="section-title-row">
            <span className="notebook-icon"></span>
            <span className="section-label">ECO-REGION & CLIMATE</span>
          </div>
          <div className="telemetry-grid">
            <div className="telemetry-item">
              <div className="telemetry-label-row">
                <span className="sub-label">Biome:</span>
                {getSourceBadge('biome')}
              </div>
              <span className="sub-value">{biome}</span>
            </div>
            <div className="telemetry-item">
              <div className="telemetry-label-row">
                <span className="sub-label">Precipitation:</span>
                {getSourceBadge('rainfall_mm')}
              </div>
              <span className="sub-value">
                {rainfall !== null ? `${rainfall} mm/yr` : <em className="missing">Awaiting input</em>}
              </span>
            </div>
            <div className="telemetry-item full-width">
              <span className="sub-label">Aridity Index (AI):</span>
              <span className="sub-value">
                {aridityMetrics?.aridity_index ? (
                  <span className="badge-aridity">
                    AI {aridityMetrics.aridity_index} — {aridityMetrics.classification} ({aridityMetrics.deficit_status})
                  </span>
                ) : (
                  <span className="status-neutral">Uncomputed</span>
                )}
              </span>
            </div>
          </div>
        </div>

        {/* Section 2: Soil Physico-Chemistry */}
        <div className="notebook-card">
          <div className="section-title-row">
            <span className="notebook-icon"></span>
            <span className="section-label">SOIL PHYSICO-CHEMISTRY</span>
          </div>
          <div className="telemetry-grid">
            <div className="telemetry-item full-width">
              <div className="metric-row-header">
                <div className="telemetry-label-row">
                  <span className="sub-label">Soil Organic Carbon (SOC):</span>
                  {getSourceBadge('soc_percent')}
                </div>
                <span className={`status-badge ${(socMetrics?.severity || '').toLowerCase().replace(' ', '-') || 'neutral'}`}>
                  {socMetrics?.severity || 'Missing'}
                </span>
              </div>
              <div className="soc-display-row">
                <span className="soc-val">{soc !== null ? `${soc}%` : '---'}</span>
                {socMetrics?.target_soc && (
                  <span className="soc-target">
                    (Target: {socMetrics.target_soc}% | Deficit: -{socMetrics.deficit_percent}%)
                  </span>
                )}
              </div>
              {socMetrics?.awc_loss_pct && (
                <div className="deficit-callout">
                   Estimated <strong>-{socMetrics.awc_loss_pct}%</strong> loss in plant-available water capacity.
                </div>
              )}
            </div>

            <div className="telemetry-item">
              <div className="telemetry-label-row">
                <span className="sub-label">pH Level:</span>
                {getSourceBadge('ph')}
              </div>
              <span className="sub-value">
                {ph !== null ? `${ph} (Mineral)` : <em className="missing">Not recorded</em>}
              </span>
            </div>

            <div className="telemetry-item">
              <span className="sub-label">Microbial Life:</span>
              <span className="sub-value">
                {socMetrics?.microbial_activity_collapse ? (
                  <span className="text-danger">Severe collapse</span>
                ) : soc !== null ? (
                  <span className="text-success">Functional</span>
                ) : 'Unknown'}
              </span>
            </div>
          </div>
        </div>

        {/* Section 3: Land Use & Agroecosystem */}
        <div className="notebook-card">
          <div className="section-title-row">
            <span className="notebook-icon"></span>
            <span className="section-label">LAND USE & CANOPY</span>
          </div>
          <div className="telemetry-grid">
            <div className="telemetry-item full-width">
              <div className="telemetry-label-row">
                <span className="sub-label">Cropping System:</span>
                {getSourceBadge('current_crop')}
              </div>
              <span className="sub-value crop-name">{crop}</span>
            </div>
            <div className="telemetry-item full-width">
              <span className="sub-label">Functional Biodiversity Index:</span>
              <div className="bio-index-row">
                <span className="bio-score">
                  {bioMetrics?.functional_biodiversity_index !== undefined
                    ? bioMetrics.functional_biodiversity_index
                    : '--'}
                </span>
                <span className="bio-status">{bioMetrics?.diversity_status || 'Awaiting system profile'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Section 4: Primary Limiting Factors */}
        {limitingFactors.length > 0 && (
          <div className="notebook-card limiting-card">
            <div className="section-title-row">
              <span className="notebook-icon"></span>
              <span className="section-label">PRIMARY LIMITING FACTORS</span>
            </div>
            <ul className="limiting-factors-list">
              {limitingFactors.map((fact, idx) => (
                <li key={idx} className="limiting-item">{fact}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Knowledge Retrieval System — RAG Pipeline Visibility */}
        {retrievedEvidence && retrievedEvidence.length > 0 && (
          <div className="notebook-card knowledge-retrieval-card">
            <div className="section-title-row">
              <span className="notebook-icon"></span>
              <span className="section-label">KNOWLEDGE RETRIEVAL SYSTEM (RAG)</span>
            </div>
            <p className="knowledge-retrieval-desc">
              {retrievedEvidence.length} peer-reviewed sources retrieved & used for evidence-backed reasoning:
            </p>
            {retrievedEvidence.map((chunk, idx) => (
              <div key={idx} className="knowledge-chunk-item">
                <div className="chunk-id-row">
                  <span className="chunk-id-badge">[{chunk.id}]</span>
                  <span className="chunk-year">{chunk.year}</span>
                </div>
                <div className="chunk-title">{chunk.title}</div>
                <div className="chunk-source">{chunk.source}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Export & Reset Actions */}
      <div className="sidebar-actions-row">
        <button className="btn-export" onClick={handleExportCase}>
           Export Case File (JSON)
        </button>
        {onResetCase && (
          <button className="btn-reset" onClick={onResetCase} disabled={isLoading}>
             Reset
          </button>
        )}
      </div>
    </aside>
  );
}
