import { useEffect, useRef } from 'react';
import { Box } from '@mui/material';

export default function UnderConstruction() {
  const pctRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    // Barra de progresso
    const targets: [number, number][] = [[2800, 72], [4200, 72], [5000, 78]];
    let start: number | null = null;
    let raf: number;

    const animate = (ts: number) => {
      if (!start) start = ts;
      const elapsed = ts - start;
      let val = 0;
      for (const [t, v] of targets) { if (elapsed >= t) val = v; }
      if (elapsed < targets[0][0]) {
        val = Math.round((elapsed / targets[0][0]) * 72);
      }
      if (pctRef.current) pctRef.current.textContent = val + '%';
      if (elapsed < 5200) raf = requestAnimationFrame(animate);
    };
    raf = requestAnimationFrame(animate);

    // Dots
    const dots = document.querySelectorAll<HTMLElement>('.uc-dot');
    let d = 0;
    const interval = setInterval(() => {
      dots.forEach(x => x.classList.remove('active'));
      d = (d + 1) % dots.length;
      dots[d].classList.add('active');
    }, 900);

    return () => {
      cancelAnimationFrame(raf);
      clearInterval(interval);
    };
  }, []);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap');

        .uc-wrap {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 3rem 2rem;
          font-family: 'DM Mono', monospace;
        }
        .uc-badge {
          font-size: 11px;
          letter-spacing: 0.18em;
          color: rgba(255,255,255,0.3);
          text-transform: uppercase;
          margin-bottom: 2.5rem;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .uc-badge::before, .uc-badge::after {
          content: '';
          display: block;
          width: 40px;
          height: 0.5px;
          background: rgba(255,255,255,0.12);
        }
        .uc-title {
          font-size: 42px;
          font-weight: 500;
          color: rgba(255,255,255,0.9);
          letter-spacing: -0.03em;
          line-height: 1.1;
          text-align: center;
          margin-bottom: 1rem;
        }
        .uc-title span {
          color: rgba(255,255,255,0.25);
        }
        .uc-sub {
          font-size: 13px;
          color: rgba(255,255,255,0.35);
          text-align: center;
          margin-bottom: 3rem;
          letter-spacing: 0.02em;
          line-height: 1.7;
        }
        .uc-bar-wrap {
          width: 280px;
          height: 3px;
          background: rgba(255,255,255,0.07);
          border-radius: 999px;
          margin-bottom: 0.75rem;
          overflow: hidden;
        }
        .uc-bar-fill {
          height: 100%;
          width: 0%;
          background: rgba(255,255,255,0.85);
          border-radius: 999px;
          animation: uc-fill 2.8s cubic-bezier(0.4,0,0.2,1) forwards;
        }
        @keyframes uc-fill {
          0%   { width: 0% }
          60%  { width: 72% }
          85%  { width: 72% }
          100% { width: 78% }
        }
        .uc-bar-label {
          font-size: 11px;
          color: rgba(255,255,255,0.25);
          letter-spacing: 0.08em;
          display: flex;
          justify-content: space-between;
          width: 280px;
        }
        .uc-log {
          margin-top: 2.5rem;
          width: 280px;
        }
        .uc-log-line {
          font-size: 11px;
          color: rgba(255,255,255,0.3);
          letter-spacing: 0.04em;
          padding: 5px 0;
          border-bottom: 0.5px solid rgba(255,255,255,0.05);
          opacity: 0;
          animation: uc-fadein 0.4s forwards;
        }
        .uc-log-line:last-child { border-bottom: none; }
        .uc-log-line .ok   { color: #5eead4; margin-right: 8px; }
        .uc-log-line .pend { color: #facc15; margin-right: 8px; }
        .uc-log-line:nth-child(1) { animation-delay: 0.3s }
        .uc-log-line:nth-child(2) { animation-delay: 0.9s }
        .uc-log-line:nth-child(3) { animation-delay: 1.5s }
        .uc-log-line:nth-child(4) { animation-delay: 2.2s }
        @keyframes uc-fadein { to { opacity: 1 } }

        .uc-dots {
          display: flex;
          gap: 6px;
          margin-top: 2rem;
        }
        .uc-dot {
          width: 5px;
          height: 5px;
          border-radius: 50%;
          background: rgba(255,255,255,0.15);
          transition: background 0.3s;
        }
        .uc-dot.active {
          background: rgba(255,255,255,0.8);
        }
      `}</style>

      <Box className="uc-wrap">
        <div className="uc-badge">em desenvolvimento</div>

        <h1 className="uc-title">
          Algo está<br /><span>sendo construído</span><br />aqui.
        </h1>

        <p className="uc-sub">
          Esta página ainda não está disponível.<br />Volte em breve.
        </p>

        <div className="uc-bar-wrap">
          <div className="uc-bar-fill" />
        </div>
        <div className="uc-bar-label">
          <span>progresso</span>
          <span ref={pctRef}>0%</span>
        </div>

        <div className="uc-log">
          <div className="uc-log-line"><span className="ok">✓</span>estrutura base</div>
          <div className="uc-log-line"><span className="ok">✓</span>componentes principais</div>
          <div className="uc-log-line"><span className="pend">~</span>integrações pendentes</div>
          <div className="uc-log-line"><span className="pend">~</span>testes finais</div>
        </div>

        <div className="uc-dots">
          <div className="uc-dot active" />
          <div className="uc-dot" />
          <div className="uc-dot" />
        </div>
      </Box>
    </>
  );
}