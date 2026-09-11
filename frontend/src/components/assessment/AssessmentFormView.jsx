import React, { useState } from 'react';

export default function AssessmentFormView({
  onSubmitTelemetry,
  isProcessing = false
}) {
  const [formData, setFormData] = useState({
    ecosystem_type: 'forest',
    land_use: 'Fragmented secondary mixed forest',
    current_crop: 'Temperate canopy trees',
    vegetation_cover: '24',
    fragmentation_index: 'severe',
    deforestation_rate: 'high',
    soc_percent: '0.8',
    soil_ph: '6.2',
    soil_moisture: '22',
    soil_texture: 'Sandy Loam',
    rainfall_mm: '850',
    rainfall_pattern: 'Seasonal',
    temperature_c: '26',
    slope_percent: '12',
    species_richness: '14',
    habitat_diversity: 'Low',
    pollution_level: 'low',
    notes: 'Severe edge desiccation and canopy gaps observed across perimeter.'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleApplyPreset = (type) => {
    if (type === 'forest') {
      setFormData({
        ecosystem_type: 'forest',
        land_use: 'Fragmented secondary forest buffer',
        current_crop: 'Hardwood canopy species',
        vegetation_cover: '24',
        fragmentation_index: 'severe',
        deforestation_rate: 'high',
        soc_percent: '0.8',
        soil_ph: '6.2',
        soil_moisture: '20',
        soil_texture: 'Loam',
        rainfall_mm: '850',
        rainfall_pattern: 'Seasonal',
        temperature_c: '24',
        slope_percent: '14',
        species_richness: '8',
        habitat_diversity: 'Low',
        pollution_level: 'low',
        notes: 'High edge tree mortality and severe interior bird isolation.'
      });
    } else if (type === 'urban') {
      setFormData({
        ecosystem_type: 'urban',
        land_use: 'Impervious commercial runoff corridor',
        current_crop: 'Turf grass & roadside trees',
        vegetation_cover: '10',
        fragmentation_index: 'high',
        deforestation_rate: 'moderate',
        soc_percent: '0.6',
        soil_ph: '7.4',
        soil_moisture: '15',
        soil_texture: 'Compacted Fill',
        rainfall_mm: '720',
        rainfall_pattern: 'Convective storm peaks',
        temperature_c: '32',
        slope_percent: '3',
        species_richness: '6',
        habitat_diversity: 'Very Low',
        pollution_level: 'high',
        notes: 'Excessive stormwater runoff, 120 mg/L TSS, and heavy metal wash-off.'
      });
    } else if (type === 'wetland') {
      setFormData({
        ecosystem_type: 'wetland',
        land_use: 'Freshwater marshland basin',
        current_crop: 'Submerged aquatic vegetation',
        vegetation_cover: '15',
        fragmentation_index: 'moderate',
        deforestation_rate: 'low',
        soc_percent: '2.4',
        soil_ph: '7.8',
        soil_moisture: '85',
        soil_texture: 'Hydric Silt',
        rainfall_mm: '620',
        rainfall_pattern: 'Bimodal',
        temperature_c: '25',
        slope_percent: '1',
        species_richness: '12',
        habitat_diversity: 'Moderate',
        pollution_level: 'high',
        notes: 'Severe agricultural nitrate runoff, Microcystis algal blooms, DO 2.1 mg/L.'
      });
    } else {
      // Agricultural
      setFormData({
        ecosystem_type: 'agricultural',
        land_use: 'Rainfed arable cropland',
        current_crop: 'Monoculture wheat',
        vegetation_cover: '20',
        fragmentation_index: 'moderate',
        deforestation_rate: 'low',
        soc_percent: '0.35',
        soil_ph: '6.8',
        soil_moisture: '14',
        soil_texture: 'Sandy Clay Loam',
        rainfall_mm: '320',
        rainfall_pattern: 'Semi-Arid sporadic',
        temperature_c: '30',
        slope_percent: '4',
        species_richness: '5',
        habitat_diversity: 'Low',
        pollution_level: 'moderate',
        notes: 'Severe topsoil erosion, lack of residue cover, high evaporative loss.'
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Construct structured payload
    const payload = {
      ecosystem_type: formData.ecosystem_type,
      land_use: formData.land_use,
      current_crop: formData.current_crop,
      vegetation_cover: parseFloat(formData.vegetation_cover) || undefined,
      fragmentation_index: formData.fragmentation_index,
      deforestation_rate: formData.deforestation_rate,
      soc_percent: parseFloat(formData.soc_percent) || undefined,
      soil_ph: parseFloat(formData.soil_ph) || undefined,
      soil_moisture: parseFloat(formData.soil_moisture) || undefined,
      soil_texture: formData.soil_texture,
      rainfall_mm: parseFloat(formData.rainfall_mm) || undefined,
      rainfall_pattern: formData.rainfall_pattern,
      temperature_c: parseFloat(formData.temperature_c) || undefined,
      slope_percent: parseFloat(formData.slope_percent) || undefined,
      species_richness: parseInt(formData.species_richness, 10) || undefined,
      habitat_diversity: formData.habitat_diversity,
      pollution_level: formData.pollution_level,
      notes: formData.notes
    };

    const summaryText = `Telemetry Assessment Submission: ${formData.ecosystem_type.toUpperCase()} ecosystem. Land use: ${formData.land_use}. SOC: ${formData.soc_percent}%, Rainfall: ${formData.rainfall_mm}mm, Canopy: ${formData.vegetation_cover}%. Notes: ${formData.notes}`;

    onSubmitTelemetry(summaryText, payload);
  };

  return (
    <div className="assessment-container">
      <div className="section-header-box">
        <div>
          <h2>📝 ENVIRONMENTAL ASSESSMENT TELEMETRY FORM</h2>
          <p className="section-subtitle">
            Input verified site parameters across edaphic, climatic, vegetation, and anthropic axes to generate an evidence-gated ecological remediation prescription.
          </p>
        </div>

        <div className="form-preset-strip">
          <span className="preset-strip-lbl">PRE-LOAD ARCHETYPE:</span>
          <button type="button" className="preset-mini-btn" onClick={() => handleApplyPreset('forest')}>🌲 Forest</button>
          <button type="button" className="preset-mini-btn" onClick={() => handleApplyPreset('urban')}>🏙️ Urban</button>
          <button type="button" className="preset-mini-btn" onClick={() => handleApplyPreset('wetland')}>💧 Wetland</button>
          <button type="button" className="preset-mini-btn" onClick={() => handleApplyPreset('ag')}>🌾 Agricultural</button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="assessment-form">
        {/* Section 1: Soil */}
        <div className="form-section-card">
          <div className="form-section-header">
            <span className="section-icon">🌱</span>
            <h4>1. EDAPHIC &amp; SOIL HEALTH PROFILE</h4>
          </div>
          <div className="form-grid-3">
            <div className="form-group">
              <label>Soil Organic Carbon (SOC)</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="0.01"
                  name="soc_percent"
                  value={formData.soc_percent}
                  onChange={handleChange}
                  required
                />
                <span className="unit-tag">%</span>
              </div>
              <span className="field-hint">Target sustainable threshold is &gt;1.20%</span>
            </div>

            <div className="form-group">
              <label>Soil pH (1:1 H2O)</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="0.1"
                  name="soil_ph"
                  value={formData.soil_ph}
                  onChange={handleChange}
                />
                <span className="unit-tag">pH</span>
              </div>
              <span className="field-hint">Optimal biological range 6.0 – 7.2</span>
            </div>

            <div className="form-group">
              <label>Volumetric Soil Moisture</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="1"
                  name="soil_moisture"
                  value={formData.soil_moisture}
                  onChange={handleChange}
                />
                <span className="unit-tag">%</span>
              </div>
              <span className="field-hint">Current topsoil moisture content</span>
            </div>

            <div className="form-group">
              <label>Soil Texture Class</label>
              <select name="soil_texture" value={formData.soil_texture} onChange={handleChange}>
                <option value="Sandy Loam">Sandy Loam</option>
                <option value="Loam">Loam</option>
                <option value="Clay Loam">Clay Loam</option>
                <option value="Silt Loam">Silt Loam</option>
                <option value="Compacted Fill">Compacted Fill / Disturbed</option>
                <option value="Hydric Silt">Hydric Silt (Wetland)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Climate */}
        <div className="form-section-card">
          <div className="form-section-header">
            <span className="section-icon">🌦️</span>
            <h4>2. CLIMATE &amp; HYDROLOGY</h4>
          </div>
          <div className="form-grid-3">
            <div className="form-group">
              <label>Mean Annual Rainfall</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="10"
                  name="rainfall_mm"
                  value={formData.rainfall_mm}
                  onChange={handleChange}
                  required
                />
                <span className="unit-tag">mm/yr</span>
              </div>
              <span className="field-hint">Defines moisture availability class</span>
            </div>

            <div className="form-group">
              <label>Rainfall Distribution</label>
              <select name="rainfall_pattern" value={formData.rainfall_pattern} onChange={handleChange}>
                <option value="Seasonal">Seasonal / Monomodal</option>
                <option value="Bimodal">Bimodal (Two Wet Seasons)</option>
                <option value="Erratic">Erratic Semi-Arid Flash Storms</option>
                <option value="Even">Year-Round Uniform</option>
                <option value="Convective storm peaks">Convective Urban Storm Peaks</option>
              </select>
            </div>

            <div className="form-group">
              <label>Mean Growing Season Temp</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="1"
                  name="temperature_c"
                  value={formData.temperature_c}
                  onChange={handleChange}
                />
                <span className="unit-tag">°C</span>
              </div>
              <span className="field-hint">Affects biological respiration rates</span>
            </div>
          </div>
        </div>

        {/* Section 3: Land & Ecosystem */}
        <div className="form-section-card">
          <div className="form-section-header">
            <span className="section-icon">🌳</span>
            <h4>3. ECOSYSTEM CLASSIFICATION &amp; LAND USE</h4>
          </div>
          <div className="form-grid-3">
            <div className="form-group">
              <label>Primary Ecosystem Matrix</label>
              <select name="ecosystem_type" value={formData.ecosystem_type} onChange={handleChange}>
                <option value="forest">🌲 Forest / Woodland</option>
                <option value="agricultural">🌾 Agricultural Cropland / Rangeland</option>
                <option value="urban">🏙️ Urban / Peri-Urban Catchment</option>
                <option value="wetland">💧 Wetland / Riparian Corridor</option>
              </select>
            </div>

            <div className="form-group">
              <label>Land Use Description</label>
              <input
                type="text"
                name="land_use"
                value={formData.land_use}
                onChange={handleChange}
                placeholder="e.g. Fragmented temperate forest"
                required
              />
            </div>

            <div className="form-group">
              <label>Topography Slope</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="1"
                  name="slope_percent"
                  value={formData.slope_percent}
                  onChange={handleChange}
                />
                <span className="unit-tag">%</span>
              </div>
              <span className="field-hint">&gt;15% triggers high erosion mitigation</span>
            </div>
          </div>
        </div>

        {/* Section 4: Biodiversity & Structure */}
        <div className="form-section-card">
          <div className="form-section-header">
            <span className="section-icon">🧬</span>
            <h4>4. BIODIVERSITY &amp; CANOPY ARCHITECTURE</h4>
          </div>
          <div className="form-grid-3">
            <div className="form-group">
              <label>Canopy Cover / Vegetation Cover</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="1"
                  name="vegetation_cover"
                  value={formData.vegetation_cover}
                  onChange={handleChange}
                />
                <span className="unit-tag">%</span>
              </div>
              <span className="field-hint">Measured structural tree/ground cover</span>
            </div>

            <div className="form-group">
              <label>Landscape Fragmentation Index</label>
              <select name="fragmentation_index" value={formData.fragmentation_index} onChange={handleChange}>
                <option value="severe">Severe (Isolated small patches &lt;10ha)</option>
                <option value="high">High (Perforated edge matrix)</option>
                <option value="moderate">Moderate (Some stepping-stones)</option>
                <option value="low">Low (Contiguous core tracts)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Observed Indicator Species</label>
              <div className="input-with-unit">
                <input
                  type="number"
                  step="1"
                  name="species_richness"
                  value={formData.species_richness}
                  onChange={handleChange}
                />
                <span className="unit-tag">taxa</span>
              </div>
              <span className="field-hint">Avian/pollinator bio-indicator count</span>
            </div>
          </div>
        </div>

        {/* Section 5: Human Threats & Field Notes */}
        <div className="form-section-card">
          <div className="form-section-header">
            <span className="section-icon">⚠️</span>
            <h4>5. THREATS &amp; FIELD OBSERVATIONS</h4>
          </div>
          <div className="form-grid-2">
            <div className="form-group">
              <label>Deforestation / Disturbance Rate</label>
              <select name="deforestation_rate" value={formData.deforestation_rate} onChange={handleChange}>
                <option value="high">High (Active perimeter clearing &amp; invasive pressure)</option>
                <option value="moderate">Moderate (Historical cutting, slow recovery)</option>
                <option value="low">Low / Protected status</option>
              </select>
            </div>

            <div className="form-group">
              <label>Chemical / Runoff Pollution</label>
              <select name="pollution_level" value={formData.pollution_level} onChange={handleChange}>
                <option value="low">Low / Organic baseline</option>
                <option value="moderate">Moderate (Fertilizer/ag runoff)</option>
                <option value="high">High (Heavy metals, raw runoff, excess N/P)</option>
              </select>
            </div>
          </div>

          <div className="form-group" style={{ marginTop: '12px' }}>
            <label>Field Telemetry Notes &amp; Site Observations</label>
            <textarea
              name="notes"
              rows={3}
              value={formData.notes}
              onChange={handleChange}
              placeholder="Describe specific erosion gullies, invasive lianas, or observed wildlife behaviors..."
            />
          </div>
        </div>

        {/* Submit Bar */}
        <div className="form-action-bar">
          <button
            type="submit"
            className="btn-submit-assessment"
            disabled={isProcessing}
          >
            {isProcessing ? '🔬 Evaluating Biophysical Constraints...' : '⚡ Run Diagnostic Environmental Assessment'}
          </button>
        </div>
      </form>
    </div>
  );
}
