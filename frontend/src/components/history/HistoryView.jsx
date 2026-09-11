import React, { useState, useEffect } from 'react';
import { fetchSessions } from '../../api/client';

export default function HistoryView({
  messages = [],
  caseFile = {},
  onNavigateTab,
  sessionId,
  onSwitchSession
}) {
  const [sessionsList, setSessionsList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchSessions()
      .then(data => {
        setSessionsList(data.sessions || data);
      })
      .catch(err => console.error("Error fetching sessions", err))
      .finally(() => setIsLoading(false));
  }, []);

  const turns = messages.filter((m) => m.role === 'user');

  return (
    <div className="history-view-container" style={{ display: 'flex', gap: '20px', height: '100%' }}>
      {/* LEFT PANE: SESSIONS LIST */}
      <div style={{ flex: '0 0 320px', background: 'var(--bg-surface)', borderRight: '1px solid var(--border-mid)', overflowY: 'auto', padding: '20px' }}>
        <h3 style={{ marginBottom: '16px', color: 'var(--text-primary)', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '10px' }}>📁 Previous Audits</h3>
        
        {isLoading ? (
          <div>Loading sessions...</div>
        ) : sessionsList.length === 0 ? (
          <div style={{ color: 'var(--text-muted)' }}>No previous sessions found.</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {sessionsList.map(s => {
              const isCurrent = s.session_id === sessionId;
              return (
                <div 
                  key={s.session_id} 
                  onClick={() => !isCurrent && onSwitchSession(s.session_id)}
                  style={{
                    padding: '12px',
                    borderRadius: '8px',
                    background: isCurrent ? 'var(--bg-clay)' : 'var(--bg-input)',
                    border: `1px solid ${isCurrent ? 'var(--border-gold)' : 'var(--border-subtle)'}`,
                    cursor: isCurrent ? 'default' : 'pointer',
                    boxShadow: isCurrent ? 'var(--shadow-warm)' : 'none',
                    transition: 'all 0.2s'
                  }}
                >
                  <div style={{ fontWeight: 'bold', fontSize: '13px', color: 'var(--text-primary)' }}>{s.title || `Session ${s.session_id.substring(0,6)}`}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Ecosystem: {s.ecosystem_type || 'Unknown'}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>{new Date(s.updated_at).toLocaleString()}</div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* RIGHT PANE: SELECTED SESSION AUDIT TRAIL */}
      <div style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
        <div className="section-header-box">
          <div>
            <h2>📜 ENVIRONMENTAL AUDIT TRAIL &amp; TELEMETRY LOG</h2>
            <p className="section-subtitle">
              Complete chronological record of submitted telemetry parameters, contradiction checks, diagnostic hypotheses, and AI recommendations for session <strong style={{color: 'var(--earth-rich)'}}>{sessionId}</strong>.
            </p>
          </div>
          <div className="badge-count-large">
            <span>{turns.length} AUDITED TURNS</span>
          </div>
        </div>

        {turns.length === 0 ? (
          <div className="empty-view-state">
            <div className="empty-icon">📜</div>
            <h3>No Assessment History Yet</h3>
            <p>Previous diagnostic runs and multi-turn parameter inputs will appear here for longitudinal audit.</p>
            <button
              className="btn-dash-primary"
              style={{ marginTop: '16px' }}
              onClick={() => onNavigateTab('assessment')}
            >
              📝 Submit First Assessment
            </button>
          </div>
        ) : (
          <div className="history-timeline">
            {messages.map((msg, idx) => {
              const isUser = msg.role === 'user';
              return (
                <div key={idx} className={`timeline-entry ${isUser ? 'entry-user' : 'entry-ai'}`}>
                  <div className="entry-marker">
                    <span className="marker-icon">{isUser ? '👤' : '🌿'}</span>
                  </div>

                  <div className="entry-card">
                    <div className="entry-header">
                      <span className="entry-author">
                        {isUser ? 'PRACTITIONER FIELD TELEMETRY' : 'DIAGNOSTIC PIPELINE SYNTHESIS'}
                      </span>
                      <span className="entry-time">{msg.timestamp || `Turn #${idx + 1}`}</span>
                    </div>

                    <div className="entry-body">
                      {msg.text.slice(0, 320)}
                      {msg.text.length > 320 ? '...' : ''}
                    </div>

                    {msg.recommendations && msg.recommendations.length > 0 && (
                      <div className="entry-recs-tag">
                        🎯 Generated {msg.recommendations.length} Action Prescriptions
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
