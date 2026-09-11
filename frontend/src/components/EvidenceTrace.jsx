import React, { useState } from 'react';

/**
 * EvidenceTrace — Expandable audit trail of verified peer-reviewed knowledge chunks & causal hops
 */
export default function EvidenceTrace({ evidenceChunks = [], causalHops = [] }) {
  const [isOpen, setIsOpen] = useState(false);

  if ((!evidenceChunks || evidenceChunks.length === 0) && (!causalHops || causalHops.length === 0)) {
    return null;
  }

  return (
    <div className="evidence-trace-box">
      <div
        className="evidence-trace-toggle"
        onClick={() => setIsOpen(!isOpen)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && setIsOpen(!isOpen)}
      >
        <span>
           VERIFIED EVIDENCE AUDIT TRAIL ({evidenceChunks.length} Citations, {causalHops.length} Causal Hops)
        </span>
        <span>{isOpen ? '▲ Collapse' : '▼ Inspect Evidence'}</span>
      </div>

      {isOpen && (
        <div className="evidence-trace-body">
          {/* Causal Graph Path */}
          {causalHops.length > 0 && (
            <div className="causal-hops-section">
              <strong style={{ fontSize: '11px', color: 'var(--accent-emerald)', fontFamily: 'var(--font-mono)' }}>
                MULTI-METRIC CAUSAL TRAJECTORY (WALKED {causalHops.length} HOPS):
              </strong>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '6px' }}>
                {causalHops.map((hop, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: 'rgba(0,0,0,0.3)',
                      padding: '8px 10px',
                      borderRadius: '4px',
                      borderLeft: '2px solid var(--accent-blue)',
                      fontSize: '12px'
                    }}
                  >
                    <div>
                      <strong style={{ color: '#bae6fd' }}>{hop.source_var}</strong>
                      <span style={{ color: 'var(--text-dim)', margin: '0 6px' }}>→</span>
                      <em>{hop.relationship}</em>
                      <span style={{ color: 'var(--text-dim)', margin: '0 6px' }}>→</span>
                      <strong style={{ color: '#a7f3d0' }}>{hop.target_var}</strong>
                    </div>
                    <div style={{ fontSize: '10.5px', color: 'var(--text-dim)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
                      Principle: {hop.scientific_principle} | Ref: [{hop.evidence_citation || hop.evidence_ref}]
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Retrieved Knowledge Base Passages */}
          {evidenceChunks.map((chunk) => (
            <div key={chunk.id} className="evidence-chunk-item">
              <div className="chunk-header">
                <span className="chunk-id-tag">[{chunk.id}]</span>
                <span className="chunk-source">{chunk.source} ({chunk.year})</span>
              </div>
              <div className="chunk-title">{chunk.title}</div>
              <div className="chunk-excerpt">"{chunk.excerpt}"</div>
              {chunk.doi_or_ref && (
                <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
                  Ref: {chunk.doi_or_ref}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
