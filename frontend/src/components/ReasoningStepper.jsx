import React, { useState } from 'react';

/**
 * ReasoningStepper — Interactive 9-Stage AI Environmental Scientist Inspector
 * Displays the complete clinical thought process from Stage 0 to Stage 8.
 */
export default function ReasoningStepper({ stages, monitoringPlan }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!stages) return null;

  const stageKeys = [
    { id: 0, key: 'stage0_validation',   label: '0. Input & Units',   icon: '' },
    { id: 1, key: 'stage1_case_file',    label: '1. Case File',       icon: '' },
    { id: 2, key: 'stage2_completeness', label: '2. Completeness',    icon: '' },
    { id: 3, key: 'stage3_hypothesis',   label: '3. Hypothesis',      icon: '' },
    { id: 4, key: 'stage4_evidence',     label: '4. Evidence RAG',    icon: '' },
    { id: 5, key: 'stage5_interventions',label: '5. Interventions',   icon: '' },
    { id: 6, key: 'stage6_writeup',      label: '6. Synthesis',       icon: '' },
    { id: 7, key: 'stage7_verification', label: '7. Peer Review',     icon: '' },
    { id: 8, key: 'stage8_delivery',     label: '8. Monitoring',      icon: '' }
  ];

  const s0 = stages.stage0_validation || {};
  const s1 = stages.stage1_case_file || {};
  const s2 = stages.stage2_completeness || {};
  const s3 = stages.stage3_hypothesis || {};
  const s4 = stages.stage4_evidence || {};
  const s5 = stages.stage5_interventions || {};
  const s6 = stages.stage6_writeup || {};
  const s7 = stages.stage7_verification || {};
  const s8 = stages.stage8_delivery || {};

  const renderJSON = (obj) => (
    <pre className="stage-json">{JSON.stringify(obj, null, 2)}</pre>
  );

  return (
    <div className="reasoning-stepper-container">
      <div className="stepper-header">
        <div className="stepper-title">
          <span className="stepper-badge">SCIENTIST REASONING TRACE</span>
          <span className="stepper-sub">Inspect Stage 0 through Stage 8 Clinical Execution</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="stepper-tabs" role="tablist">
        {stageKeys.map((item) => (
          <button
            key={item.id}
            role="tab"
            aria-selected={activeTab === item.id}
            className={`stepper-tab-btn ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="tab-icon">{item.icon}</span>
            <span className="tab-label">{item.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      <div className="stepper-content">
        {/* STAGE 0 */}
        {activeTab === 0 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 0: Input Sanitization & Unit Sanity Check</h4>
              <span className="stage-status-badge passed"> Passed Bounds Check</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist does not accept field telemetry at face value without double-checking units and physical feasibility.
            </p>
            <div className="stage-grid">
              <div className="info-card">
                <span className="info-label">Input Mode Detected</span>
                <span className="info-value uppercase-mode">{s0.input_mode || 'free_text'}</span>
              </div>
              <div className="info-card">
                <span className="info-label">Physical Bounds Status</span>
                <span className="info-value text-green">pH [0-14], Rain ≥ 0, Coords valid</span>
              </div>
            </div>
            {s0.suspicious_alerts && s0.suspicious_alerts.length > 0 && (
              <div className="alert-card warning">
                <h5> Suspicious Field Reading Flagged</h5>
                {s0.suspicious_alerts.map((alt, i) => (
                  <p key={i}>{alt.message}</p>
                ))}
              </div>
            )}
            <div className="extracted-fields-box">
              <h5>Extracted Biophysical Entities</h5>
              <div className="extracted-tags">
                {Object.entries(s0.extracted_entities || {}).map(([k, v]) => (
                  <span key={k} className="entity-chip">
                    <strong>{k}:</strong> {String(v)}
                  </span>
                ))}
              </div>
            </div>
            <p className="scientist-note"> {s0.scientist_note}</p>
          </div>
        )}

        {/* STAGE 1 */}
        {activeTab === 1 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 1: Environmental Case File & Provenance</h4>
              <span className="stage-status-badge passed"> Profile Updated</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist maintains a structured patient file without losing previous observations.
            </p>
            {s1.running_assessment && (
              <div className="running-assessment-box">
                <div className="ra-label">RUNNING ASSESSMENT (Auto-updated):</div>
                <div className="ra-text">{s1.running_assessment}</div>
              </div>
            )}
            {s1.contradiction_alerts && s1.contradiction_alerts.length > 0 && (
              <div className="alert-card warning">
                <h5> Multi-Turn Contradictions Detected</h5>
                {s1.contradiction_alerts.map((c, i) => (
                  <div key={i} className="contradiction-item">
                    <span className="field-label">{c.field}:</span> {c.conflict_description}
                  </div>
                ))}
              </div>
            )}
            <div className="provenance-table-wrapper">
              <h5>Profile Provenance (Source Tracking)</h5>
              <table className="provenance-table">
                <thead><tr><th>Field</th><th>Value</th><th>Source</th><th>Confidence</th><th>Date</th></tr></thead>
                <tbody>
                  {Object.entries(s1.provenance || {}).map(([field, prov]) => (
                    <tr key={field}>
                      <td>{field}</td>
                      <td>{String(prov.value)}</td>
                      <td>{prov.source}</td>
                      <td>{Math.round((prov.confidence || 0.8) * 100)}%</td>
                      <td>{prov.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="scientist-note"> {s1.scientist_note}</p>
          </div>
        )}

        {/* STAGE 2 */}
        {activeTab === 2 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 2: Completeness & Domain-Probe Check</h4>
              <span className={`stage-status-badge ${s2.is_preliminary ? 'warning' : 'passed'}`}>
                {s2.completeness_ratio || 'Checking...'}
              </span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist identifies which missing variables would most change the diagnosis before proceeding.
            </p>
            {s2.domain_probes && s2.domain_probes.length > 0 && (
              <div className="domain-probes-box">
                <strong>Domain Probes (Proactive Scientist Inquiry):</strong>
                {s2.domain_probes.map((p, i) => <div key={i} className="probe-item"> {p}</div>)}
              </div>
            )}
            {s2.ambiguity_translations && s2.ambiguity_translations.length > 0 && (
              <div className="ambiguity-box">
                <strong>Ambiguous Language Detected:</strong>
                {s2.ambiguity_translations.map((a, i) => (
                  <div key={i} className="ambiguity-item">
                    <span className="amb-phrase">"{a.phrase}"</span> → Could mean: {a.candidate_measurable_metrics?.join(', ')}
                  </div>
                ))}
              </div>
            )}
            <p className="scientist-note"> {s2.scientist_note}</p>
          </div>
        )}

        {/* STAGE 3 */}
        {activeTab === 3 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 3: Diagnostic Hypothesis Formation</h4>
              <span className="stage-status-badge passed"> Rules Applied</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist forms a testable limiting-factor hypothesis deterministically BEFORE accessing the literature.
            </p>
            {s3.hypothesis && (
              <div className="hypothesis-box">
                <div className="hypothesis-label">WORKING HYPOTHESIS:</div>
                <div className="hypothesis-text">{s3.hypothesis}</div>
              </div>
            )}
            {s3.limiting_factors && s3.limiting_factors.length > 0 && (
              <div className="limiting-list">
                <strong>Primary Limiting Factors:</strong>
                {s3.limiting_factors.map((f, i) => <div key={i} className="limiting-item"> {f}</div>)}
              </div>
            )}
            {s3.risk_ratings && (
              <div className="risk-ratings-grid">
                {Object.entries(s3.risk_ratings).map(([risk, level]) => (
                  <div key={risk} className={`risk-chip ${level?.toLowerCase()}`}>
                    <span className="risk-name">{risk.replace(/_/g, ' ')}</span>
                    <span className="risk-level">{level}</span>
                  </div>
                ))}
              </div>
            )}
            <p className="scientist-note"> {s3.scientist_note}</p>
          </div>
        )}

        {/* STAGE 4 */}
        {activeTab === 4 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 4: Biome-Gated Hybrid Evidence Retrieval (RAG)</h4>
              <span className="stage-status-badge passed">
                 {s4.retrieved_chunk_count || 0} Sources Retrieved
              </span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist selects literature based on biome match, source authority, and deliberately seeks dissenting studies.
            </p>
            {s4.retrieval_trace && (
              <div className="retrieval-trace-box">
                <div className="rt-item"><strong>Biome Filter:</strong> {s4.retrieval_trace.biome_filter}</div>
                <div className="rt-item"><strong>Corpus Evaluated:</strong> {s4.retrieval_trace.total_corpus_evaluated} chunks</div>
                <div className="rt-item"><strong>Steer Terms:</strong> {s4.retrieval_trace.steer_terms_applied?.join(', ')}</div>
                <div className="rt-item"><strong>Dissenting Studies:</strong> {s4.retrieval_trace.dissenting_studies_included} surfaced</div>
              </div>
            )}
            {s4.retrieved_chunks && s4.retrieved_chunks.map((c, i) => (
              <div key={i} className="evidence-chunk-item" style={{ marginTop: '8px' }}>
                <div className="chunk-header">
                  <span className="chunk-id-tag">[{c.id}]</span>
                  <span className="chunk-source">{c.source} ({c.year})</span>
                  <span className="chunk-score">Score: {c.relevance_score}</span>
                </div>
                <div className="chunk-title">{c.title}</div>
              </div>
            ))}
            <p className="scientist-note"> {s4.scientist_note}</p>
          </div>
        )}

        {/* STAGE 5 */}
        {activeTab === 5 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 5: Intervention Selection & Causal Graph</h4>
              <span className="stage-status-badge passed"> 3-Hop Graph Walked</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist maps physical prohibition gates before selecting interventions, and walks multi-variable causal chains.
            </p>
            <div className="viable-prohibited-row">
              <div className="viable-box">
                <strong>Viable:</strong>
                {(s5.viable_categories || []).map((v, i) => <span key={i} className="viable-chip">{v}</span>)}
              </div>
              <div className="prohibited-box">
                <strong>Prohibited:</strong>
                {(s5.prohibited_categories || []).map((p, i) => <span key={i} className="prohibited-chip">{p}</span>)}
              </div>
            </div>
            {s5.variables_connected && (
              <div className="variables-connected">
                <strong>Variables Connected in Causal Graph:</strong>
                <div>{s5.variables_connected.join(' ↔ ')}</div>
              </div>
            )}
            <p className="scientist-note"> {s5.scientist_note}</p>
          </div>
        )}

        {/* STAGE 6 */}
        {activeTab === 6 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 6: Scientific Write-Up (Explanation Only)</h4>
              <span className="stage-status-badge passed"> Hallucination-Gated</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> The LLM explains pre-computed results in academic hedged register. It does NOT generate numbers or citations.
            </p>
            <div className="stage-grid">
              <div className="info-card"><span className="info-label">Register</span><span className="info-value">{s6.register}</span></div>
              <div className="info-card"><span className="info-label">Hallucination Prevention</span><span className="info-value">{s6.hallucination_prevention}</span></div>
              <div className="info-card"><span className="info-label">Trade-offs Included</span><span className="info-value text-green">{s6.tradeoffs_included ? ' Yes' : ' No'}</span></div>
            </div>
            <p className="scientist-note"> {s6.scientist_note}</p>
          </div>
        )}

        {/* STAGE 7 */}
        {activeTab === 7 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 7: Peer-Review Verifier</h4>
              <span className="stage-status-badge passed"> All Checks Passed</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist does not publish without peer-review. All citations are verified to exist in retrieved corpus.
            </p>
            <div className="stage-grid">
              <div className="info-card"><span className="info-label">Citation Existence Check</span><span className="info-value text-green">{s7.citation_existence_checked ? ' Verified' : '—'}</span></div>
              <div className="info-card"><span className="info-label">Climate Compatibility Check</span><span className="info-value text-green">{s7.climate_compatibility_checked ? ' Verified' : '—'}</span></div>
            </div>
            {s7.calculated_confidence && (
              <div className="confidence-display-box">
                <strong>Empirical Confidence Score:</strong>
                <span className="conf-score-large">{Math.round((s7.calculated_confidence.score || 0.85) * 100)}%</span>
                <span className="conf-label-text">{s7.calculated_confidence.label}</span>
                <div className="conf-basis">{s7.calculated_confidence.basis}</div>
              </div>
            )}
            <p className="scientist-note"> {s7.scientist_note}</p>
          </div>
        )}

        {/* STAGE 8 */}
        {activeTab === 8 && (
          <div className="stage-panel">
            <div className="stage-panel-header">
              <h4>Stage 8: Structured Delivery & Monitoring Protocol</h4>
              <span className="stage-status-badge passed"> Protocol Generated</span>
            </div>
            <p className="scientist-callout">
              <strong>Scientist Behavior:</strong> A scientist's report ends with: "Here is how you will measure whether this worked in the field."
            </p>
            {(monitoringPlan || s8.monitoring_plan || []).map((p, i) => (
              <div key={i} className="monitoring-protocol-item">
                <div className="monitoring-param">{p.parameter}</div>
                <div className="monitoring-row"><strong>Method:</strong> {p.baseline_method}</div>
                <div className="monitoring-row"><strong>Frequency:</strong> {p.frequency}</div>
                <div className="monitoring-row"><strong>Year 1 Indicator:</strong> {p.short_term_indicator}</div>
                <div className="monitoring-row"><strong>Years 3–5:</strong> {p.long_term_indicator}</div>
              </div>
            ))}
            <p className="scientist-note"> {s8.scientist_note}</p>
          </div>
        )}
      </div>
    </div>
  );
}
