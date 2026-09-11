import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadialLinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Doughnut, Bar, Radar, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadialLinearScale,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

/**
 * Empty/Fallback state when environmental telemetry is insufficient
 */
export function EmptyChartState({ message = "Provide additional environmental measurements to visualize this trend." }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '36px 20px',
      background: 'rgba(255, 252, 246, 0.8)',
      border: '1.5px dashed rgba(169, 113, 66, 0.25)',
      borderRadius: '12px',
      textAlign: 'center',
      minHeight: '200px'
    }}>
      <div style={{ fontSize: '28px', marginBottom: '8px' }}>📡</div>
      <div style={{ color: '#62452F', fontSize: '13px', fontWeight: 700 }}>Not enough data</div>
      <div style={{ color: '#856852', fontSize: '12px', marginTop: '4px', maxWidth: '320px' }}>{message}</div>
    </div>
  );
}

/**
 * 1. Semi-Doughnut Environmental Health Score Gauge (0 - 100)
 */
export function EnvironmentalScoreGauge({ score = 65, statusLabel = "Moderate Stability" }) {
  const cleanScore = Math.max(0, Math.min(100, Math.round(score || 50)));
  const remaining = 100 - cleanScore;

  // Scientific contrasting colors:
  const primaryColor = cleanScore < 40 ? '#e11d48' : cleanScore < 70 ? '#d97706' : '#059669';
  const glowColor = cleanScore < 40 ? 'rgba(225, 29, 72, 0.12)' : cleanScore < 70 ? 'rgba(217, 119, 6, 0.12)' : 'rgba(5, 150, 105, 0.12)';

  const data = {
    labels: ['Health Score', 'Deficit'],
    datasets: [
      {
        data: [cleanScore, remaining],
        backgroundColor: [primaryColor, 'rgba(214, 195, 174, 0.45)'],
        borderColor: [primaryColor, 'rgba(184, 137, 99, 0.3)'],
        borderWidth: 1.5,
        circumference: 240,
        rotation: 240,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '78%',
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false }
    }
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '190px', display: 'flex', justifyContent: 'center' }}>
      <Doughnut data={data} options={options} />
      <div style={{
        position: 'absolute',
        top: '48%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '38px', fontWeight: 900, color: primaryColor, lineHeight: 1 }}>
          {cleanScore}
        </div>
        <div style={{ fontSize: '11px', color: '#856852', textTransform: 'uppercase', letterSpacing: '1px', marginTop: '4px', fontWeight: 700 }}>
          / 100 INDEX
        </div>
        <div style={{
          marginTop: '6px',
          display: 'inline-block',
          fontSize: '11px',
          fontWeight: 700,
          color: primaryColor,
          background: glowColor,
          padding: '2px 10px',
          borderRadius: '12px',
          border: `1px solid ${primaryColor}40`
        }}>
          {statusLabel}
        </div>
      </div>
    </div>
  );
}

/**
 * 2. Multi-Metric Ecological Threshold Comparison (Radar Chart)
 */
export function EcologicalBalanceRadarChart({ profile = {}, ruleMetrics = {} }) {
  const eco = (profile.ecosystem_type || ruleMetrics.ecosystem_type || 'agricultural').toLowerCase();

  let labels = ['Soil Carbon', 'Available Moisture', 'Canopy Cover', 'Infiltration', 'Biodiversity Index'];
  let currentValues = [35, 45, 30, 40, 32];
  let targetValues = [85, 80, 85, 90, 80];

  if (eco === 'forest') {
    labels = ['Canopy Cover', 'Core Area %', 'Interior Birds', 'Moisture Buffer', 'Corridor Link'];
    const canopy = profile.vegetation_cover || 24;
    currentValues = [canopy, 30, 28, 35, 22];
    targetValues = [85, 75, 80, 85, 80];
  } else if (eco === 'urban') {
    labels = ['Infiltration %', 'TSS Interception', 'Cooling Canopy', 'Permeable Cover', 'Pollinator Paths'];
    const p = profile.pervious_area_percent || 15;
    currentValues = [p, 25, 20, p, 30];
    targetValues = [80, 90, 75, 75, 75];
  } else if (eco === 'wetland') {
    labels = ['Dissolved O2', 'Nitrate Strip %', 'Macrophyte Cover', 'Benthic Index', 'Littoral Depth'];
    currentValues = [28, 20, 25, 30, 35];
    targetValues = [85, 90, 80, 80, 85];
  } else {
    // Agricultural
    const soc = profile.soc_percent || 0.35;
    const socNorm = Math.min(100, Math.round((soc / 1.5) * 100));
    currentValues = [socNorm, 40, 25, 38, 28];
    targetValues = [85, 80, 75, 85, 75];
  }

  const data = {
    labels,
    datasets: [
      {
        label: 'Current Field Baseline',
        data: currentValues,
        backgroundColor: 'rgba(225, 29, 72, 0.22)',
        borderColor: '#e11d48',
        pointBackgroundColor: '#e11d48',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#e11d48',
        borderWidth: 2,
      },
      {
        label: 'Healthy Ecological Target (3-5 Yr)',
        data: targetValues,
        backgroundColor: 'rgba(5, 150, 105, 0.22)',
        borderColor: '#059669',
        pointBackgroundColor: '#059669',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#059669',
        borderWidth: 2,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: { color: 'rgba(169, 113, 66, 0.2)' },
        grid: { color: 'rgba(169, 113, 66, 0.18)' },
        pointLabels: {
          color: '#4A3324',
          font: { size: 11, family: 'Inter', weight: 600 }
        },
        ticks: { display: false, max: 100, min: 0 }
      }
    },
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#4A3324',
          font: { size: 11.5, family: 'Inter', weight: 600 },
          boxWidth: 12,
          padding: 14
        }
      },
      tooltip: {
        backgroundColor: '#382417',
        titleColor: '#fcd34d',
        bodyColor: '#fff',
        borderColor: 'rgba(217, 164, 65, 0.4)',
        borderWidth: 1
      }
    }
  };

  return (
    <div style={{ height: '260px', width: '100%' }}>
      <Radar data={data} options={options} />
    </div>
  );
}

/**
 * 3. 5-Year Quantitative Recovery Trajectory (Line Chart)
 */
export function FiveYearRecoveryTrajectoryChart({ profile = {}, ruleMetrics = {} }) {
  const eco = (profile.ecosystem_type || ruleMetrics.ecosystem_type || 'agricultural').toLowerCase();

  let metricName = "Soil Organic Carbon (SOC %)";
  let baseline = profile.soc_percent ? parseFloat(profile.soc_percent) : 0.35;
  let target = 0.88;
  let yMin = 0.2;
  let yMax = 1.0;
  let unit = "%";

  if (eco === 'forest') {
    metricName = "Canopy & Structural Corridors (%)";
    baseline = profile.vegetation_cover ? parseFloat(profile.vegetation_cover) : 24.0;
    target = 78.0;
    yMin = 15;
    yMax = 90;
    unit = "%";
  } else if (eco === 'urban') {
    metricName = "Stormwater Infiltration & Heavy Metal Filter (%)";
    baseline = profile.pervious_area_percent ? parseFloat(profile.pervious_area_percent) : 15.0;
    target = 82.0;
    yMin = 10;
    yMax = 95;
    unit = "%";
  } else if (eco === 'wetland') {
    metricName = "Water Dissolved Oxygen (mg/L)";
    baseline = 2.1;
    target = 7.1;
    yMin = 1.5;
    yMax = 8.5;
    unit = " mg/L";
  }

  // Trajectory points: Year 0, Year 1, Year 2, Year 3, Year 4, Year 5
  const step = (target - baseline) / 5;
  const dataPoints = [
    baseline,
    Number((baseline + step * 0.7).toFixed(2)),
    Number((baseline + step * 1.7).toFixed(2)),
    Number((baseline + step * 2.9).toFixed(2)),
    Number((baseline + step * 4.1).toFixed(2)),
    Number((target).toFixed(2))
  ];

  const data = {
    labels: ['Year 0 (Baseline)', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5 (Climax)'],
    datasets: [
      {
        label: metricName,
        data: dataPoints,
        borderColor: '#059669',
        backgroundColor: 'rgba(5, 150, 105, 0.12)',
        pointBackgroundColor: '#047857',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        fill: true,
        tension: 0.35,
        borderWidth: 2.5
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        grid: { color: 'rgba(169, 113, 66, 0.15)' },
        ticks: { color: '#62452F', font: { size: 10.5, family: 'Inter', weight: 500 } }
      },
      y: {
        min: yMin,
        max: yMax,
        grid: { color: 'rgba(169, 113, 66, 0.15)' },
        ticks: {
          color: '#62452F',
          font: { size: 10.5, family: 'Inter', weight: 500 },
          callback: (val) => `${val}${unit}`
        }
      }
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: { color: '#4A3324', font: { size: 11.5, weight: 600 } }
      },
      tooltip: {
        backgroundColor: '#382417',
        titleColor: '#fcd34d',
        bodyColor: '#fff',
        borderColor: 'rgba(217, 164, 65, 0.4)',
        borderWidth: 1,
        callbacks: {
          label: (context) => `${context.dataset.label}: ${context.parsed.y}${unit}`
        }
      }
    }
  };

  return (
    <div style={{ height: '240px', width: '100%' }}>
      <Line data={data} options={options} />
    </div>
  );
}

/**
 * 4. Grouped Comparative Bar Chart: Current vs Healthy Target
 */
export function MetricComparisonBarChart({ profile = {}, ruleMetrics = {} }) {
  const eco = (profile.ecosystem_type || ruleMetrics.ecosystem_type || 'agricultural').toLowerCase();

  let labels = ['SOC %', 'Infiltration (mm/h)', 'Moisture Cap.', 'Mycorrhiza'];
  let current = [0.35, 8, 45, 15];
  let target = [1.20, 35, 90, 75];

  if (eco === 'forest') {
    labels = ['Canopy %', 'Core Area %', 'Interior Birds', 'Connectivity %'];
    current = [profile.vegetation_cover || 24, 18, 8, 22];
    target = [75, 65, 28, 70];
  } else if (eco === 'urban') {
    labels = ['Infiltration %', 'TSS Removal %', 'Canopy %', 'Green Space %'];
    current = [profile.pervious_area_percent || 15, 20, 8, 12];
    target = [75, 88, 30, 45];
  } else if (eco === 'wetland') {
    labels = ['Dissolved O2', 'Nitrate Strip %', 'Macrophyte %', 'Benthic Index'];
    current = [2.1, 15, 10, 18];
    target = [7.2, 88, 55, 65];
  }

  const data = {
    labels,
    datasets: [
      {
        label: 'Current Baseline',
        data: current,
        backgroundColor: 'rgba(225, 29, 72, 0.85)',
        borderColor: '#e11d48',
        borderWidth: 1,
        borderRadius: 4
      },
      {
        label: 'Ecological Threshold Target',
        data: target,
        backgroundColor: 'rgba(5, 150, 105, 0.85)',
        borderColor: '#059669',
        borderWidth: 1,
        borderRadius: 4
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: '#4A3324', font: { size: 11, family: 'Inter', weight: 600 } }
      },
      y: {
        grid: { color: 'rgba(169, 113, 66, 0.15)' },
        ticks: { color: '#62452F', font: { size: 10.5 } }
      }
    },
    plugins: {
      legend: {
        position: 'top',
        labels: { color: '#4A3324', font: { size: 11, weight: 600 }, boxWidth: 12 }
      },
      tooltip: {
        backgroundColor: '#382417',
        titleColor: '#fcd34d',
        bodyColor: '#fff',
        borderColor: 'rgba(217, 164, 65, 0.4)',
        borderWidth: 1
      }
    }
  };

  return (
    <div style={{ height: '230px', width: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  );
}
