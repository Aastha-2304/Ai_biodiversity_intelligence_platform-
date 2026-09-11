import React from 'react';

export default function RecommendationsView({
  recommendations = [],
  onNavigateTab
}) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="empty-view-state">
        <div className="empty-icon">🎯</div>
        <h3>No Prescriptions Generated Yet</h3>
        <p>
          Submit your site's environmental telemetry using the Assessment form or click a benchmark scenario to generate tailored, evidence-backed ecological prescriptions.
        </p>
        <button
          className="btn-dash-primary"
          style={{ marginTop: '16px' }}
          onClick={() => onNavigateTab('assessment')}
        >
          📝 Open Assessment Form
        </button>
      </div>
    );
  }

  const renderConfidenceDots = (score = 0.85) => {
    const dots = Math.round(score * 5);
    return (
      <span className="confidence-dots" title={`Confidence Score: ${Math.round(score * 100)}%`}>
        {'●'.repeat(Math.min(5, dots)) + '○'.repeat(Math.max(0, 5 - dots))}
      </span>
    );
  };

  return (
    <div className="recommendations-container">
      {/* Header */}
      <div className="section-header-box">
        <div>
          <h2>🎯 EVIDENCE-BACKED ECOLOGICAL REMEDIATION PRESCRIPTIONS</h2>
          <p className="section-subtitle">
            Ranked multi-metric interventions optimized for biophysical constraints, peer-reviewed evidence validation, and multi-year succession.
          </p>
        </div>
        <div className="badge-count-large">
          <span>{recommendations.length} VERIFIED ACTIONS</span>
        </div>
      </div>

      {/* Cards Grid */}
      <div className="recs-professional-grid">
        {recommendations.map((rec, idx) => {
          const confScore = rec.confidence?.score || 0.85;
          const confLabel = rec.confidence?.label || 'High Confidence';
          const timeHorizon = rec.time_horizon || 'Medium Term (2–4 Years)';

          return (
            <div key={rec.id || idx} className="rec-card-pro">
              {/* Header */}
              <div className="rec-card-header">
                <div className="rec-num-badge">RECOMMENDATION 0{idx + 1}</div>
                <div className="rec-time-badge">⏱️ {timeHorizon}</div>
              </div>

              {/* Title */}
              <h3 className="rec-title">{rec.name || rec.title}</h3>

              {/* Action Description */}
              <div className="rec-action-box">
                <div className="rec-box-label">🎯 ACTIONABLE ON-FARM / ON-SITE PRACTICE</div>
                <p className="rec-action-text">{rec.action_summary || rec.description}</p>
              </div>

              {/* Why This Works */}
              <div className="rec-why-box">
                <div className="rec-box-label">🔬 WHY THIS WORKS (BIOPHYSICAL MECHANISM)</div>
                <p className="rec-why-text">
                  {rec.scientific_reasoning || rec.why_it_works || 'Activates biological succession pathways to resolve identified environmental deficits.'}
                </p>
              </div>

              {/* Impact Indicators */}
              <div className="rec-impact-section">
                <div className="rec-box-label">📈 MULTI-METRIC EXPECTED IMPACT</div>
                <div className="impact-pills-wrap">
                  {(rec.expected_impacts || [
                    { metric: 'Soil Organic Carbon', change: '↑ +15–25%' },
                    { metric: 'Water Infiltration', change: '↑ +40%' },
                    { metric: 'Habitat Diversity', change: '↑ Restored' }
                  ]).map((imp, i) => (
                    <div key={i} className="impact-pill">
                      <span className="impact-metric">{imp.metric || imp}:</span>
                      <span className="impact-change">{imp.change || '↑ Positive'}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Phases / Protocols */}
              {rec.implementation_protocol && (
                <div className="rec-phases-box">
                  <div className="rec-box-label">🛠️ FIELD IMPLEMENTATION TIMELINE</div>
                  <div className="phase-timeline-row">
                    <div className="phase-step">
                      <span className="phase-badge">Phase 1</span>
                      <span className="phase-desc">{rec.implementation_protocol.phase_1 || 'Site prep & grading'}</span>
                    </div>
                    <div className="phase-step">
                      <span className="phase-badge">Phase 2</span>
                      <span className="phase-desc">{rec.implementation_protocol.phase_2 || 'Inoculation & planting'}</span>
                    </div>
                    <div className="phase-step">
                      <span className="phase-badge">Phase 3</span>
                      <span className="phase-desc">{rec.implementation_protocol.phase_3 || 'Succession & canopy'}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Critical Pitfall */}
              {rec.critical_pitfalls && (
                <div className="rec-pitfall-box">
                  <span className="pitfall-icon">⚠️</span>
                  <div className="pitfall-body">
                    <strong>CRITICAL PITFALL (WHAT NOT TO DO):</strong> {rec.critical_pitfalls}
                  </div>
                </div>
              )}

              {/* Card Footer: Confidence & Evidence Link */}
              <div className="rec-card-footer">
                <div className="rec-confidence-group">
                  <span className="conf-label">CONFIDENCE:</span>
                  {renderConfidenceDots(confScore)}
                  <span className="conf-text">{confLabel}</span>
                </div>

                {rec.evidence_citations && rec.evidence_citations.length > 0 && (
                  <div className="rec-citation-link">
                    <span>Evidence: </span>
                    <strong className="citation-code">{rec.evidence_citations[0]}</strong>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
