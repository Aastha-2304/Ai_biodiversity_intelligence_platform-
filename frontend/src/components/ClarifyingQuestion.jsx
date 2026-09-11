import React, { useState } from 'react';

/**
 * ClarifyingQuestion — Interactive prompt when critical environmental variables are missing.
 * Provides preset options AND a dedicated last option to type custom values if presets do not match.
 */
export default function ClarifyingQuestion({ clarifyingQuestion, onSelectOption }) {
  if (!clarifyingQuestion) return null;

  const {
    missing_parameter,
    missing_parameters,
    question_text,
    scientific_rationale,
    suggested_inputs = [],
    allow_custom_input = true,
    custom_option_label = " Type my own field values (custom input)",
    custom_input_fields = []
  } = clarifyingQuestion;

  const [showCustomForm, setShowCustomForm] = useState(false);
  const [customSoc, setCustomSoc] = useState('');
  const [customRain, setCustomRain] = useState('');
  const [customLandUse, setCustomLandUse] = useState('');
  const [freeText, setFreeText] = useState('');

  const handlePresetClick = (opt) => {
    if (onSelectOption) {
      onSelectOption(opt);
    }
  };

  const handleCustomSubmit = (e) => {
    e.preventDefault();
    const parts = [];
    const structured = {};

    if (customSoc) {
      parts.push(`SOC: ${customSoc}%`);
      structured.soc_percent = parseFloat(customSoc);
    }
    if (customRain) {
      parts.push(`Rainfall: ${customRain}`);
      const numMatch = customRain.match(/[\d.]+/);
      if (numMatch) structured.rainfall_mm = parseFloat(numMatch[0]);
      structured.rainfall_pattern = customRain;
    }
    if (customLandUse) {
      parts.push(`Land use: ${customLandUse}`);
      structured.land_use_type = customLandUse;
      structured.current_crop = customLandUse;
    }
    if (freeText.trim()) {
      parts.push(freeText.trim());
    }

    if (parts.length === 0) return;

    const summaryText = `Supplemental Field Telemetry: ${parts.join(', ')}`;
    if (onSelectOption) {
      onSelectOption(summaryText, Object.keys(structured).length > 0 ? structured : null);
    }
    setShowCustomForm(false);
  };

  const paramLabel = missing_parameters && missing_parameters.length > 0
    ? missing_parameters.join(', ')
    : missing_parameter;

  return (
    <div className="clarifying-question-card">
      <div className="cq-badge-row">
        <span className="cq-pill">DATA CALIBRATION REQUIRED</span>
        <span className="cq-param-badge">
          Parameter(s): {paramLabel}
        </span>
      </div>

      <div className="cq-question">{question_text}</div>
      <div className="cq-rationale">
        <em>Scientific Rationale:</em> {scientific_rationale}
      </div>

      <div className="cq-subtitle">Select a typical baseline profile or type custom field telemetry:</div>

      {/* Suggested Options */}
      <div className="cq-options">
        {suggested_inputs.map((opt, idx) => (
          <button
            key={idx}
            className="cq-btn-option"
            onClick={() => handlePresetClick(opt)}
            title="Click to apply this preset baseline"
          >
            <span className="cq-btn-bullet">●</span> {opt}
          </button>
        ))}

        {/* LAST OPTION: Type custom values if options don't match */}
        {allow_custom_input && (
          <button
            className={`cq-btn-option cq-btn-custom-toggle ${showCustomForm ? 'active' : ''}`}
            onClick={() => setShowCustomForm(!showCustomForm)}
          >
            <span>{custom_option_label}</span>
            <span className="cq-toggle-icon">{showCustomForm ? '▲ Close' : '▼ Expand'}</span>
          </button>
        )}
      </div>

      {/* Expandable Custom Typing Form */}
      {showCustomForm && (
        <form className="cq-custom-form" onSubmit={handleCustomSubmit}>
          <div className="cq-form-header">
            <strong>Custom Field Telemetry (Values not listed above)</strong>
            <span>Direct calibration into multi-turn memory</span>
          </div>

          <div className="cq-form-grid">
            <div className="cq-field-group">
              <label>Soil Organic Carbon (SOC %)</label>
              <input
                type="number"
                step="0.05"
                min="0.0"
                max="15.0"
                placeholder="e.g. 0.35"
                value={customSoc}
                onChange={(e) => setCustomSoc(e.target.value)}
              />
            </div>

            <div className="cq-field-group">
              <label>Rainfall Pattern / Annual (mm)</label>
              <input
                type="text"
                placeholder="e.g. 340mm unimodal dryland"
                value={customRain}
                onChange={(e) => setCustomRain(e.target.value)}
              />
            </div>

            <div className="cq-field-group">
              <label>Land Use Type / Cropping</label>
              <input
                type="text"
                placeholder="e.g. continuous wheat monoculture"
                value={customLandUse}
                onChange={(e) => setCustomLandUse(e.target.value)}
              />
            </div>
          </div>

          <div className="cq-field-group" style={{ marginTop: '8px' }}>
            <label>Additional Field Observations / Desired Outcome</label>
            <input
              type="text"
              placeholder="e.g. High wind erosion, shallow sandy loam topsoil"
              value={freeText}
              onChange={(e) => setFreeText(e.target.value)}
            />
          </div>

          <div className="cq-form-actions">
            <button
              type="submit"
              className="cq-submit-btn"
              disabled={!customSoc && !customRain && !customLandUse && !freeText.trim()}
            >
              ▶ Submit My Custom Field Values
            </button>
            <button
              type="button"
              className="cq-cancel-btn"
              onClick={() => setShowCustomForm(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
