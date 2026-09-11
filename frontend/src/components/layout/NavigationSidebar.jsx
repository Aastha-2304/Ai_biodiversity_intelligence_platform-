import React from 'react';

export default function NavigationSidebar({
  activeTab = 'dashboard',
  onSelectTab,
  sessionId = '',
  healthScore = 65,
  ecosystemType = 'agricultural'
}) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊', desc: 'Health & Ecological State' },
    { id: 'biodiversity', label: 'Biodiversity Analysis', icon: '🧬', desc: 'Metrics & 5-Yr Trajectory' },
    { id: 'assessment', label: 'Environmental Assessment', icon: '📝', desc: 'Telemetry & Site Input' },
    { id: 'scientist', label: 'AI Scientist', icon: '🔬', desc: '3-Pane Research Workspace' },
    { id: 'recommendations', label: 'Recommendations', icon: '🎯', desc: 'Evidence-Gated Prescriptions' },
    { id: 'sources', label: 'Scientific Sources', icon: '📚', desc: 'FAO, IPCC & PNAS Evidence' },
    { id: 'history', label: 'Audit History', icon: '📜', desc: 'Session Logs & Memory' },
    { id: 'streamlit', label: 'Streamlit Portal', icon: '⚡', desc: '6-Panel Visual Intelligence' },
  ];

  const getHealthBadge = (score) => {
    if (score < 40) return { label: 'CRITICAL', color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.15)' };
    if (score < 70) return { label: 'VULNERABLE', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' };
    return { label: 'BALANCED', color: '#10b981', bg: 'rgba(16, 185, 129, 0.15)' };
  };

  const badge = getHealthBadge(healthScore);

  return (
    <aside className="nav-sidebar">
      {/* Brand Section */}
      <div className="sidebar-brand">
        <div className="brand-badge-icon">🌿</div>
        <div className="brand-text">
          <div className="brand-title">DARUKAA<span className="brand-highlight">.EARTH</span></div>
          <div className="brand-sub">AI Environmental Intelligence</div>
        </div>
      </div>

      {/* System Telemetry Tag */}
      <div className="sidebar-system-pill">
        <span className="live-dot pulse"></span>
        <span>EVIDENCE-GATED PIPELINE</span>
      </div>

      {/* Navigation List */}
      <nav className="nav-menu">
        <div className="nav-section-label">OPERATIONAL WORKSPACES</div>
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item-btn ${isActive ? 'active' : ''}`}
              onClick={() => onSelectTab(item.id)}
            >
              <span className="nav-item-icon">{item.icon}</span>
              <div className="nav-item-content">
                <div className="nav-item-label">{item.label}</div>
                <div className="nav-item-desc">{item.desc}</div>
              </div>
              {isActive && <div className="nav-active-pip" />}
            </button>
          );
        })}
      </nav>

      {/* Bottom Profile Summary Card */}
      <div className="sidebar-bottom-panel">
        <div className="bottom-card-header">
          <span className="bottom-card-title">SITE STATUS</span>
          <span
            className="bottom-health-chip"
            style={{ color: badge.color, background: badge.bg, borderColor: `${badge.color}40` }}
          >
            {badge.label} ({healthScore})
          </span>
        </div>
        <div className="bottom-card-body">
          <div className="meta-row">
            <span className="meta-lbl">Ecosystem:</span>
            <span className="meta-val capitalize">{ecosystemType}</span>
          </div>
          <div className="meta-row">
            <span className="meta-lbl">Session:</span>
            <span className="meta-val mono">#{sessionId.slice(-6).toUpperCase()}</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
