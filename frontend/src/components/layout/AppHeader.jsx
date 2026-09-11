import React from 'react';

export default function AppHeader({
  ecosystemType = 'agricultural',
  onSelectPreset,
  onResetSession,
  onOpenAssessment,
  onOpenStreamlit,
  isProcessing = false,
  sessions = [],
  selectedSessionId = '',
  onSelectSession,
  onCreateSession
}) {
  const PRESETS = [
    {
      id: 'forest',
      label: ' Forest Corridor',
      desc: 'Fragmentation & Xylem Cavitation',
      payload: {
        ecosystem_type: 'forest',
        land_use: 'fragmented temperate mixed forest buffer',
        vegetation_cover: 24.0,
        fragmentation_index: 'severe',
        deforestation_rate: 'high',
        rainfall_mm: 850.0
      },
      text: 'Our forest landscape suffers from severe fragmentation, 24% canopy cover, and edge desiccation.'
    },
    {
      id: 'urban',
      label: ' Urban Lake',
      desc: 'Stormwater & Runoff Pollutants',
      payload: {
        ecosystem_type: 'urban',
        land_use: 'urban lake catchment and commercial periphery',
        pervious_area_percent: 14.0,
        pollution_level: 'high',
        runoff_risk: 'high',
        rainfall_mm: 720.0
      },
      text: 'Urban stormwater runoff with high suspended solids (120 mg/L TSS) and heavy metals is polluting our municipal lake.'
    },
    {
      id: 'wetland',
      label: ' Eutrophic Wetland',
      desc: 'Algal Blooms & Lake Drawdown',
      payload: {
        ecosystem_type: 'wetland',
        land_use: 'freshwater marshland and agricultural basin',
        water_quality: 'eutrophic',
        water_level: 'declining',
        pollution_level: 'high',
        rainfall_mm: 620.0
      },
      text: 'Freshwater marshland experiencing severe agricultural nutrient runoff, toxic algal blooms, and 2.1 mg/L dissolved oxygen.'
    },
    {
      id: 'ag',
      label: ' Semi-Arid Cropland',
      desc: 'SOC 0.35% & High VPD',
      payload: {
        ecosystem_type: 'agricultural',
        current_crop: 'monoculture wheat',
        soc_percent: 0.35,
        rainfall_mm: 320.0,
        biome: 'semi-arid'
      },
      text: 'SOC 0.35%, low rainfall 320mm/yr, monoculture wheat in semi-arid region with declining soil moisture.'
    }
  ];

  return (
    <header className="app-top-header">
      <div className="header-left">
        <div className="eco-badge">
          <span className="eco-indicator-dot"></span>
          <span className="eco-label-text">ECOSYSTEM:</span>
          <span className="eco-name">{ecosystemType.toUpperCase()}</span>
        </div>

        {/* Global Session Switcher */}
        <div className="header-session-switcher">
          <span className="session-switch-lbl">SESSION:</span>
          <select
            className="header-session-select"
            value={selectedSessionId}
            onChange={(e) => onSelectSession && onSelectSession(e.target.value)}
            disabled={isProcessing}
            title="Switch active research session (all components update instantly)"
          >
            {sessions.map((s) => (
              <option key={s.session_id} value={s.session_id}>
                {s.title || s.session_id} ({s.session_id.slice(-6)})
              </option>
            ))}
            {sessions.length === 0 && (
              <option value={selectedSessionId}>Session #{selectedSessionId?.slice(-6) || 'current'}</option>
            )}
          </select>
          {onCreateSession && (
            <button
              className="btn-header-new-session"
              onClick={onCreateSession}
              disabled={isProcessing}
              title="Create a new isolated session"
            >
              + New
            </button>
          )}
        </div>
      </div>

      <div className="header-center">
        <div className="preset-strip">
          <span className="preset-strip-lbl">PRESETS:</span>
          {PRESETS.map((p) => (
            <button
              key={p.id}
              className="preset-chip-btn"
              disabled={isProcessing}
              title={p.desc}
              onClick={() => onSelectPreset(p.text, p.payload)}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      <div className="header-right">
        {onOpenStreamlit && (
          <button
            className="btn-new-assessment"
            onClick={onOpenStreamlit}
            style={{
              background: 'linear-gradient(135deg, #10b981, #059669)',
              color: '#ffffff',
              borderColor: '#059669',
              fontWeight: '700'
            }}
            title="Switch to 6-Panel Streamlit Intelligence View"
          >
            <span>⚡</span> Streamlit Portal
          </button>
        )}

        <button
          className="btn-new-assessment"
          onClick={onOpenAssessment}
        >
          <span></span> Telemetry Form
        </button>

        <button
          className="btn-reset-session"
          onClick={onResetSession}
          disabled={isProcessing}
          title="Reset environmental case profile"
        >
          <span></span> Reset
        </button>
      </div>
    </header>
  );
}
