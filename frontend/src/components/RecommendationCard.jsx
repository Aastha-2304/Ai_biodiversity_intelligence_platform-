import React, { useState } from 'react';
import ConfidenceBadge from './ConfidenceBadge';

/**
 * RecommendationCard — Evidence-backed intervention card with expandable metrics table
 */
export default function RecommendationCard({ recommendation, index }) {
  const [expanded, setExpanded] = useState(false);

  if (!recommendation) return null;

  const {
    id,
    name,
    action,
    mechanism,
    impacted_metrics = [],
    time_horizon,
    trade_offs = [],
    evidence_ids = [],
    confidence,
    compatibility_status
  } = recommendation;

  const th = (time_horizon || '').toLowerCase();
  let timeLabel = ' Long-term';
  let timeClass = 'long';
  if (th.includes('immediate') || th.includes('1 season') || th.includes('year 1')) {
    timeLabel = ' Immediate / Year 1';
    timeClass = 'immediate';
  } else if (th.includes('1 to 3') || th.includes('2-3') || th.includes('1-3') || th.includes('3 season')) {
    timeLabel = ' Short-Medium (1–3 yr)';
    timeClass = 'medium';
  }

  const isRestricted = compatibility_status === 'Restricted';

  return (
    <div className={`rec-card ${isRestricted ? 'rec-restricted' : ''}`}>
      {/* Header */}
      <div className="rec-header">
        <div className="rec-title-row">
          <span className="rec-index">#{index}</span>
          <span className="rec-name">{name || action?.split('.')[0]}</span>
          {isRestricted && <span className="rec-restricted-badge"> RESTRICTED</span>}
        </div>
        <div className="rec-meta-row">
          <span className={`rec-time-badge ${timeClass}`}>{timeLabel}</span>
          <span className="rec-id-chip">{id}</span>
        </div>
      </div>

      {/* Mechanism */}
      <div className="rec-mechanism-box">
        <strong>WHY IT WORKS:</strong> {mechanism}
      </div>

      {/* Evidence citations always visible */}
      {evidence_ids.length > 0 && (
        <div className="rec-evidence-row">
          <span className="evidence-label">SOURCES:</span>
          {evidence_ids.map((eid, idx) => (
            <span key={idx} className="evidence-chip">[{eid}]</span>
          ))}
        </div>
      )}

      <ConfidenceBadge confidence={confidence} />

      {/* Expand toggle */}
      <button
        className="rec-expand-btn"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? '▲ Collapse Details' : '▼ View Impacted Metrics & Trade-offs'}
      </button>

      {/* Expanded section */}
      {expanded && (
        <div className="rec-expanded-details">
          {impacted_metrics.length > 0 && (
            <div>
              <div className="rec-section-label">IMPACTED ENVIRONMENTAL METRICS:</div>
              <table className="metrics-impact-table">
                <thead>
                  <tr>
                    <th>Variable</th>
                    <th>Baseline</th>
                    <th>Projected</th>
                    <th>Δ Estimate</th>
                    <th>Horizon</th>
                  </tr>
                </thead>
                <tbody>
                  {impacted_metrics.map((m, idx) => (
                    <tr key={idx}>
                      <td className="metric-name-cell">{m.metric_name}</td>
                      <td>{m.baseline_value}</td>
                      <td>{m.projected_value}</td>
                      <td className="metric-delta-cell">{m.delta_estimate}</td>
                      <td className="metric-time-cell">{m.time_horizon_years}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {trade_offs.length > 0 && (
            <div className="rec-trade-offs">
              <strong>TRADE-OFFS & IMPLEMENTATION CONSTRAINTS:</strong>
              <ul>
                {trade_offs.map((t, idx) => (
                  <li key={idx}>{t}</li>
                ))}
              </ul>
            </div>
          )}

          {action && (
            <div className="rec-full-action">
              <strong>FULL ACTION:</strong> {action}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
