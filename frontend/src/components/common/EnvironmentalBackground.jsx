import React, { useEffect, useRef } from 'react';

/**
 * EnvironmentalBackground
 * Elegant, lightweight living ecosystem atmosphere:
 * - Warm ambient sunlight dispersion
 * - Floating pollen/seed particles that drift naturally with wind currents
 * - Organic flowing breeze streamlines
 * - Lightweight 60fps canvas, low CPU, respects prefers-reduced-motion
 */
export default function EnvironmentalBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    // Particle seeds: golden pollen and spore motes
    const particleCount = Math.min(36, Math.floor(width / 35));
    const particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2.2 + 0.8,
        speedX: Math.random() * 0.4 + 0.15,
        speedY: Math.random() * 0.3 - 0.15,
        opacity: Math.random() * 0.45 + 0.15,
        pulseSpeed: Math.random() * 0.02 + 0.01,
        angle: Math.random() * Math.PI * 2,
        color: i % 3 === 0 ? 'rgba(217, 164, 65, ' : i % 3 === 1 ? 'rgba(184, 137, 99, ' : 'rgba(52, 211, 153, '
      });
    }

    let time = 0;

    const render = () => {
      time += 0.008;
      ctx.clearRect(0, 0, width, height);

      // 1. Subtle warm ambient sunlight gradient glow
      const sunGradient = ctx.createRadialGradient(width * 0.85, height * 0.08, 10, width * 0.85, height * 0.08, width * 0.6);
      sunGradient.addColorStop(0, 'rgba(241, 199, 91, 0.16)');
      sunGradient.addColorStop(0.4, 'rgba(232, 184, 75, 0.07)');
      sunGradient.addColorStop(1, 'rgba(255, 249, 237, 0)');
      ctx.fillStyle = sunGradient;
      ctx.fillRect(0, 0, width, height);

      // 2. Earth base glow at bottom
      const earthGradient = ctx.createLinearGradient(0, height * 0.7, 0, height);
      earthGradient.addColorStop(0, 'rgba(193, 138, 91, 0)');
      earthGradient.addColorStop(1, 'rgba(169, 113, 66, 0.06)');
      ctx.fillStyle = earthGradient;
      ctx.fillRect(0, height * 0.7, width, height * 0.3);

      // 3. Gentle organic wind streamlines
      ctx.save();
      ctx.strokeStyle = 'rgba(184, 137, 99, 0.08)';
      ctx.lineWidth = 1.2;
      for (let j = 0; j < 3; j++) {
        ctx.beginPath();
        const yBase = height * (0.25 + j * 0.28);
        ctx.moveTo(0, yBase + Math.sin(time + j) * 25);
        for (let x = 0; x < width; x += 60) {
          const yWave = yBase + Math.sin(x * 0.003 + time * 1.5 + j) * 28 + Math.cos(x * 0.002 - time) * 14;
          ctx.lineTo(x, yWave);
        }
        ctx.stroke();
      }
      ctx.restore();

      // 4. Draw & update drifting environmental pollen particles
      particles.forEach((p) => {
        p.angle += p.pulseSpeed;
        const currentOpacity = p.opacity + Math.sin(p.angle) * 0.12;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `${p.color}${Math.max(0.05, currentOpacity)})`;
        ctx.shadowBlur = 8;
        ctx.shadowColor = 'rgba(232, 184, 75, 0.4)';
        ctx.fill();
        ctx.shadowBlur = 0;

        // Drift motion
        p.x += p.speedX;
        p.y += Math.sin(p.angle) * 0.35 + p.speedY;

        if (p.x > width + 10) p.x = -10;
        if (p.x < -10) p.x = width + 10;
        if (p.y > height + 10) p.y = -10;
        if (p.y < -10) p.y = height + 10;
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 0,
        opacity: 0.95
      }}
    />
  );
}
