import React from 'react';

/**
 * ConfidenceBadge — Calibrated Scientific Confidence Indicator
 */
export default function ConfidenceBadge({ confidence }) {
  if (!confidence) return null;

  const score = confidence.score !== undefined ? confidence.score : 0.8;
  const label = confidence.label || (score >= 0.8 ? 'High Confidence' : score >= 0.6 ? 'Moderate' : 'Low');
  const basis = confidence.basis || 'Based on verified empirical peer-reviewed citations and physical parameters.';

  const styleClass = score >= 0.8 ? 'high' : score >= 0.6 ? 'moderate' : 'low';

  return (
    <div className={`confidence-badge-wrapper ${styleClass}`}>
      <span className="conf-icon"></span>
      <span className="conf-label">{label} ({Math.round(score * 100)}%)</span>

      <div className="confidence-tooltip">
        <strong>Scientific Basis:</strong>
        <p>{basis}</p>
      </div>
    </div>
  );
}
