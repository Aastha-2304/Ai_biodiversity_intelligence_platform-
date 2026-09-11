import React, { useState, useRef, useEffect } from 'react';
import ClarifyingQuestion from '../ClarifyingQuestion';

export default function AIScientistWorkspace({
  messages = [],
  onSendMessage,
  caseFile = {},
  ruleMetrics = {},
  isLoading = false
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  const profile = caseFile.profile || {};
  const eco = (profile.ecosystem_type || ruleMetrics?.ecosystem_type || 'agricultural').toLowerCase();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText);
    setInputText('');
  };

  const handleSelectOption = (optText, structuredPayload) => {
    if (structuredPayload) {
      onSendMessage(optText, structuredPayload);
    } else {
      onSendMessage(optText);
    }
  };

  return (
    <div className="scientist-workspace-grid">
      {/* LEFT PANE: Sessions & Scenario Prompts */}
      <aside className="scientist-left-pane">
        <div className="pane-header">
          <span className="pane-title">RESEARCH SESSIONS</span>
          <span className="badge-count">{messages.length} msgs</span>
        </div>

        <div className="session-history-list">
          <div className="session-item active">
            <div className="session-item-title">Current Diagnostic Session</div>
            <div className="session-item-sub">
              {eco.toUpperCase()} Matrix • SOC {profile.soc_percent ? `${profile.soc_percent}%` : '0.35%'}
            </div>
            <div className="session-meta-time">Active Now</div>
          </div>
        </div>

        <div className="quick-probes-section">
          <div className="pane-subtitle">QUICK INVESTIGATIVE PROBES</div>
          <button
            className="probe-btn"
            disabled={isLoading}
            onClick={() => onSendMessage("What specific native trees should we plant to stop edge xylem cavitation?")}
          >
            🌲 How to stop forest edge cavitation?
          </button>
          <button
            className="probe-btn"
            disabled={isLoading}
            onClick={() => onSendMessage("How much nitrogen will legume intercropping fix per hectare?")}
          >
            🌱 Expected nitrogen fixation gains?
          </button>
          <button
            className="probe-btn"
            disabled={isLoading}
            onClick={() => onSendMessage("What bioswale aggregate depth is required for heavy metal filtration?")}
          >
            🏙️ Engineered bioswale depths?
          </button>
          <button
            className="probe-btn"
            disabled={isLoading}
            onClick={() => onSendMessage("How quickly will benthic dissolved oxygen recover after macrophyte planting?")}
          >
            💧 Wetland dissolved oxygen recovery rate?
          </button>
        </div>
      </aside>

      {/* CENTER PANE: Scientific Dialogue */}
      <main className="scientist-center-pane">
        <div className="dialogue-header">
          <div className="dialogue-title-group">
            <h3>🔬 SCIENTIFIC DIALOGUE STREAM</h3>
            <span className="dialogue-sub">9-Stage Evidence-Gated Ecological Decision Support</span>
          </div>
          {isLoading && (
            <div className="loading-pulse-badge">
              <span className="pulse-dot"></span>
              <span>Analyzing biophysical constraints...</span>
            </div>
          )}
        </div>

        <div className="dialogue-scroll-area">
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div key={idx} className={`dialogue-bubble-wrap ${isUser ? 'user-wrap' : 'system-wrap'}`}>
                <div className="bubble-meta">
                  <span className="bubble-sender">{isUser ? '👤 Practitioner Telemetry' : '🌿 AI Environmental Scientist'}</span>
                  <span className="bubble-time">{msg.timestamp || ''}</span>
                </div>

                <div className={`dialogue-bubble ${isUser ? 'bubble-user' : 'bubble-system'}`}>
                  {/* Text content */}
                  <div className="bubble-markdown" style={{ whiteSpace: 'pre-wrap', lineHeight: '1.65' }}>
                    {msg.text}
                  </div>

                  {/* Clarifying Question Options */}
                  {msg.clarifying_question && (
                    <div style={{ marginTop: '14px' }}>
                      <ClarifyingQuestion
                        clarifyingQuestion={msg.clarifying_question}
                        onSelectOption={handleSelectOption}
                      />
                    </div>
                  )}

                  {/* Inline Recommendations Badge */}
                  {msg.recommendations && msg.recommendations.length > 0 && (
                    <div className="inline-recs-notice">
                      <span>🎯 <strong>{msg.recommendations.length} Actionable Prescriptions</strong> verified and available in the Recommendations view.</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>

        {/* Bottom Input Area */}
        <form onSubmit={handleSubmit} className="dialogue-input-form">
          <input
            type="text"
            className="dialogue-text-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask a scientific question (e.g. 'How does mycorrhizal hyphae unlock fixed phosphorus in dry soils?')..."
            disabled={isLoading}
          />
          <button
            type="submit"
            className="btn-send-dialogue"
            disabled={!inputText.trim() || isLoading}
          >
            {isLoading ? '...' : 'Inquire →'}
          </button>
        </form>
      </main>

      {/* RIGHT PANE: Current Environment Context Panel */}
      <aside className="scientist-right-pane">
        <div className="pane-header">
          <span className="pane-title">CURRENT ENVIRONMENT</span>
          <span className="status-live-chip">LIVE TELEMETRY</span>
        </div>

        <div className="context-profile-box">
          <div className="profile-section-title">ACTIVE SITE PROFILE</div>

          <div className="profile-field-row">
            <span className="field-key">Ecosystem Matrix</span>
            <span className="field-val highlight capitalize">{eco}</span>
          </div>

          <div className="profile-field-row">
            <span className="field-key">Land Use Type</span>
            <span className="field-val">{profile.land_use || profile.current_crop || 'Mixed Landscape'}</span>
          </div>

          <div className="profile-field-row">
            <span className="field-key">Soil Organic Carbon</span>
            <span className="field-val">{profile.soc_percent ? `${profile.soc_percent}%` : '0.35% (Baseline)'}</span>
          </div>

          <div className="profile-field-row">
            <span className="field-key">Annual Rainfall</span>
            <span className="field-val">{profile.rainfall_mm ? `${profile.rainfall_mm} mm/yr` : 'Semi-Arid'}</span>
          </div>

          <div className="profile-field-row">
            <span className="field-key">Canopy Cover</span>
            <span className="field-val">{profile.vegetation_cover ? `${profile.vegetation_cover}%` : 'Depleted'}</span>
          </div>

          <div className="profile-field-row">
            <span className="field-key">Health Index</span>
            <span className="field-val score">{ruleMetrics?.system_health_index || 48} / 100</span>
          </div>
        </div>

        {/* Limiting Factors Card */}
        <div className="context-card" style={{ marginTop: '14px' }}>
          <div className="profile-section-title">PRIMARY LIMITING FACTORS</div>
          <ul className="limiting-bullets">
            {(ruleMetrics?.primary_limiting_factors || [
              'High vapor pressure deficit (VPD)',
              'Suppressed biological glomalin production'
            ]).map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </div>

        {/* Causal Chains / Evidence Links */}
        <div className="context-card" style={{ marginTop: '14px' }}>
          <div className="profile-section-title">RETRIEVAL PROVENANCE</div>
          <div className="prov-text">
            All synthesis is strictly bounded by peer-reviewed evidence (FAO, IPCC, Science, PNAS, Nature, Ramsar) with zero unauthorized extrapolation.
          </div>
        </div>
      </aside>
    </div>
  );
}
