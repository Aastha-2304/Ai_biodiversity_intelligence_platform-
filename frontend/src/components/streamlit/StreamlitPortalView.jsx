import React, { useState, useRef } from 'react';

export default function StreamlitPortalView() {
  const [iframeKey, setIframeKey] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const containerRef = useRef(null);

  const handleReload = () => {
    setIframeKey((prev) => prev + 1);
  };

  const handleToggleFullscreen = () => {
    if (!document.fullscreenElement) {
      if (containerRef.current?.requestFullscreen) {
        containerRef.current.requestFullscreen();
        setIsFullscreen(true);
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
        setIsFullscreen(false);
      }
    }
  };

  return (
    <div
      ref={containerRef}
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: isFullscreen ? '100vh' : 'calc(100vh - 100px)',
        background: '#FFFDF8',
        borderRadius: isFullscreen ? '0' : '16px',
        border: '1.5px solid rgba(169, 113, 66, 0.25)',
        boxShadow: '0 8px 30px rgba(139, 94, 60, 0.12)',
        overflow: 'hidden',
        margin: isFullscreen ? '0' : '0 4px',
        transition: 'all 0.3s ease'
      }}
    >
      {/* Top Controls Toolbar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '10px 18px',
          background: 'linear-gradient(90deg, #FDF8ED 0%, #FFFDF8 100%)',
          borderBottom: '1px solid rgba(169, 113, 66, 0.22)',
          flexShrink: 0
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #10b981, #059669)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '16px',
              color: '#fff',
              boxShadow: '0 2px 8px rgba(16, 185, 129, 0.35)'
            }}
          >
            ⚡
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontWeight: 800, fontSize: '15px', color: '#382417', letterSpacing: '-0.01em' }}>
                Streamlit 6-Panel Visual Intelligence Platform
              </span>
              <span
                style={{
                  background: 'rgba(16, 185, 129, 0.12)',
                  color: '#059669',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  padding: '2px 8px',
                  borderRadius: '12px',
                  fontSize: '11px',
                  fontWeight: 700
                }}
              >
                ● LIVE ENGINE :8501
              </span>
            </div>
            <div style={{ fontSize: '12px', color: '#8B5E3C' }}>
              Deterministic biophysical rules, 3D/radar graphs & biome-gated RAG explorer
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            onClick={handleReload}
            title="Reload Streamlit Engine Session"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '8px',
              border: '1px solid rgba(169, 113, 66, 0.3)',
              background: '#FFFDF8',
              color: '#5C381E',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            🔄 Refresh Frame
          </button>

          <button
            onClick={handleToggleFullscreen}
            title="Toggle Fullscreen"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '8px',
              border: '1px solid rgba(169, 113, 66, 0.3)',
              background: '#FFFDF8',
              color: '#5C381E',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            ⛶ Fullscreen
          </button>

          <a
            href="http://localhost:8501"
            target="_blank"
            rel="noopener noreferrer"
            title="Open in standalone tab"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '8px',
              border: '1px solid #C18A5B',
              background: 'linear-gradient(135deg, #D9A441, #C18A5B)',
              color: '#382417',
              fontSize: '12px',
              fontWeight: 700,
              textDecoration: 'none',
              cursor: 'pointer',
              boxShadow: '0 2px 6px rgba(193, 138, 91, 0.25)'
            }}
          >
            ↗ Standalone Window
          </a>
        </div>
      </div>

      {/* Embedded Streamlit Frame */}
      <div style={{ flex: 1, width: '100%', height: '100%', position: 'relative' }}>
        <iframe
          key={iframeKey}
          src="http://localhost:8501/?embedded=true"
          title="Streamlit 6-Panel Ecological Intelligence"
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            display: 'block'
          }}
          allow="camera; microphone; fullscreen; clipboard-read; clipboard-write"
        />
      </div>
    </div>
  );
}
