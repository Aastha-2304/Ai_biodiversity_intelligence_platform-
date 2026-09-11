import React, { useState, useRef, useEffect } from 'react';
import RecommendationCard from './RecommendationCard';
import EvidenceTrace from './EvidenceTrace';
import ClarifyingQuestion from './ClarifyingQuestion';
import ReasoningStepper from './ReasoningStepper';
import MarkdownContent from './common/MarkdownContent';
import { fetchDemoCase } from '../api/client';

const DEMO_SCENARIOS = [
  { key: 'canonical_semi_arid_wheat', label: ' Canonical Reference' },
  { key: 'suspicious_unit_test',      label: ' Unit Sanity Test' },
  { key: 'contradiction_test',        label: ' Contradiction Test' },
  { key: 'incomplete_probe_test',     label: ' Incomplete Input' },
  { key: 'ambiguous_input_test',      label: ' Ambiguity Test' }
];

export default function ChatWindow({ messages, onSendMessage, isLoading, onSelectClarifyingOption }) {
  const [inputText, setInputText] = useState('');
  const [jsonMode, setJsonMode] = useState(false);
  const [jsonText, setJsonText] = useState('');
  const [jsonError, setJsonError] = useState('');
  const [showStepper, setShowStepper] = useState({});
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = () => {
    const text = inputText.trim();
    let structuredInput = null;
    if (jsonMode && jsonText.trim()) {
      try {
        structuredInput = JSON.parse(jsonText);
        setJsonError('');
      } catch {
        setJsonError('Invalid JSON — please check your syntax.');
        return;
      }
    }
    if (!text && !structuredInput) return;
    onSendMessage(text || null, structuredInput);
    setInputText('');
    setJsonText('');
    setJsonMode(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleDemoLoad = async (demoKey) => {
    try {
      const demo = await fetchDemoCase(demoKey);
      onSendMessage(demo.input_text || null, demo.structured_json || null);
    } catch {
      onSendMessage(`Run demo: ${demoKey}`);
    }
  };

  const toggleStepper = (msgIdx) => {
    setShowStepper(prev => ({ ...prev, [msgIdx]: !prev[msgIdx] }));
  };

  return (
    <main className="chat-main">
      {/* Demo Scenarios Bar */}
      <div className="demo-bar">
        <span className="demo-bar-label">TEST SCENARIOS:</span>
        {DEMO_SCENARIOS.map(s => (
          <button
            key={s.key}
            className="demo-chip"
            onClick={() => handleDemoLoad(s.key)}
            disabled={isLoading}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* Message Feed */}
      <div className="messages-feed">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-bubble ${msg.role}`}>
            <div className="message-meta">
              <span className="message-role">
                {msg.role === 'user' ? ' You' : ' Darukaa AI Scientist'}
              </span>
              {msg.timestamp && <span className="message-time">{msg.timestamp}</span>}
              {msg.input_mode && (
                <span className="input-mode-badge">MODE: {msg.input_mode}</span>
              )}
            </div>

            {/* Contradiction / Suspicious Alerts */}
            {msg.suspicious_alerts && msg.suspicious_alerts.length > 0 && (
              <div className="alert-banner warning">
                 {msg.suspicious_alerts.map(a => a.message).join(' | ')}
              </div>
            )}
            {msg.contradiction_alerts && msg.contradiction_alerts.length > 0 && (
              <div className="alert-banner contradiction">
                 Multi-Turn Contradiction: {msg.contradiction_alerts.map(c => c.conflict_description).join(' | ')}
              </div>
            )}

            {/* Main Text */}
            <div className="message-text">
              {msg.role === 'user' ? (
                <p>{msg.text}</p>
              ) : (
                <MarkdownContent text={msg.text} />
              )}
            </div>

            {/* Clarifying Question */}
            {msg.clarifying_question && (
              <ClarifyingQuestion
                clarifyingQuestion={msg.clarifying_question}
                onSelectOption={onSelectClarifyingOption}
              />
            )}

            {/* Recommendations */}
            {msg.recommendations && msg.recommendations.length > 0 && (
              <div className="recommendations-section">
                <div className="recs-header">
                  <span> EVIDENCE-BACKED INTERVENTIONS ({msg.recommendations.length})</span>
                </div>
                {msg.recommendations.map((rec, ri) => (
                  <RecommendationCard key={ri} recommendation={rec} index={ri + 1} />
                ))}
              </div>
            )}

            {/* Evidence Trace */}
            {msg.retrieved_evidence && msg.retrieved_evidence.length > 0 && (
              <EvidenceTrace
                evidenceChunks={msg.retrieved_evidence}
                causalHops={msg.causal_hops || []}
              />
            )}

            {/* Stage Inspector Toggle */}
            {msg.stages && (
              <div className="stage-inspector-wrapper">
                <button
                  className="stage-inspector-toggle"
                  onClick={() => toggleStepper(idx)}
                >
                  {showStepper[idx] ? '▲ Close Scientist Reasoning Trace' : '▼ Inspect 9-Stage Scientist Reasoning Trace'}
                </button>
                {showStepper[idx] && (
                  <ReasoningStepper stages={msg.stages} monitoringPlan={msg.monitoring_plan} />
                )}
              </div>
            )}
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="message-bubble system loading-bubble">
            <div className="loading-stepper">
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
              <span className="loading-label">Running 9-stage pipeline...</span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="input-area">
        {/* JSON Mode Toggle */}
        <div className="input-controls-row">
          <button
            className={`json-toggle-btn ${jsonMode ? 'active' : ''}`}
            onClick={() => setJsonMode(!jsonMode)}
          >
            {jsonMode ? ' Switch to Text' : ' Paste JSON'}
          </button>
          {jsonMode && (
            <span className="json-mode-hint">JSON mode: paste structured field telemetry</span>
          )}
        </div>

        {jsonMode ? (
          <div className="json-input-wrapper">
            <textarea
              className="json-input"
              placeholder={`{\n  "soc_percent": 0.3,\n  "rainfall_mm": 320,\n  "current_crop": "monoculture wheat",\n  "biome": "semi-arid"\n}`}
              value={jsonText}
              onChange={(e) => setJsonText(e.target.value)}
              rows={8}
            />
            {jsonError && <div className="json-error">{jsonError}</div>}
          </div>
        ) : (
          <textarea
            className="chat-input"
            placeholder="Describe your land conditions... e.g. 'SOC 0.3%, 320mm rainfall, monoculture wheat, semi-arid region. What interventions do you recommend?'"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={3}
            disabled={isLoading}
          />
        )}

        <div className="input-actions-row">
          <span className="input-hint">Enter to send · Shift+Enter for newline</span>
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={isLoading || (!inputText.trim() && !jsonText.trim())}
          >
            {isLoading ? '⏳ Analyzing...' : '▶ Run Diagnostic'}
          </button>
        </div>
      </div>
    </main>
  );
}
