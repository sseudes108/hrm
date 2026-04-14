import { Text } from "@tremor/react";
import { GlassCard } from "./../Layout/GlassCard";
import { THEMES } from "../../constants/colors";

interface RiskScoreProps {
  theme: typeof THEMES.FRAUDE;
}

const gravityNodes = [
  { x: 10, y: 70 },
  { x: 25, y: 55 },
  { x: 40, y: 35, gravity: true },
  { x: 55, y: 50 },
  { x: 70, y: 25, gravity: true },
  { x: 85, y: 45 },
  { x: 100, y: 30, gravity: true },
  { x: 115, y: 55 },
  { x: 130, y: 70, gravity: true },
  { x: 145, y: 50 },
  { x: 160, y: 75, gravity: true },
  { x: 175, y: 60 },
  { x: 190, y: 65 },
];

const generateWirePath = (nodes: typeof gravityNodes, deviation: number) => {
  return nodes.map((d, i) => {
    const jitter = d.gravity ? 0 : (Math.random() - 0.5) * deviation;
    return `${i === 0 ? "M" : "L"} ${d.x} ${d.y + jitter}`;
  }).join(" ");
};

export function RiskScoreCard({ theme }: RiskScoreProps) {
  const wire1 = generateWirePath(gravityNodes, 18);
  const wire2 = generateWirePath(gravityNodes, 12);
  const wire3 = generateWirePath(gravityNodes, 6);
  const wire4 = generateWirePath(gravityNodes, 22);

  return (
    <GlassCard theme={theme} className="group relative overflow-hidden h-full flex flex-col">
      {/* TÍTULO */}
      <Text className="text-slate-100 font-bold tracking-[0.2em] uppercase text-[10px] mb-4 relative z-10">
        Risk Score Distribution
      </Text>

      {/* CONTAINER DO CONTEÚDO */}
      <div className="flex items-center justify-between w-full flex-1 gap-2">
        
        {/* 1. CÍRCULO DE PROGRESSO (Empurrado para a esquerda) */}
        <div className="relative flex-shrink-0 w-32 h-32 flex items-center justify-center -ml-5">
          <svg className="w-full h-full -rotate-90 transform">
            <circle 
              cx="64" cy="64" r="36" 
              stroke="currentColor" 
              strokeWidth="8" 
              fill="transparent" 
              className="text-slate-900/30" 
            />
            <circle
              cx="64" cy="64" r="36"
              stroke={theme.primary}
              strokeWidth="8"
              strokeDasharray={226}
              style={{ 
                strokeDashoffset: 226 * (1 - 0.77),
                filter: `drop-shadow(0 0 12px ${theme.primary}aa)`,
                transition: 'stroke-dashoffset 1.5s ease-in-out'
              }}
              strokeLinecap="round" 
              fill="transparent"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center italic font-black text-white text-2xl mt-3">
            <span className="leading-none">77</span>
            <span style={{ color: theme.primary }} className="text-[10px] not-italic tracking-widest -mt-1 opacity-80">%</span>
          </div>
        </div>

        {/* 2. SISTEMA DE FIOS (Ocupa o centro) */}
        <div className="flex-1 h-24 relative overflow-hidden">
          <svg className="w-full h-full" viewBox="0 0 200 100" preserveAspectRatio="none">
            <defs>
              <filter id="glow-wire-mesh">
                <feGaussianBlur stdDeviation="1" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {[wire1, wire2, wire3, wire4].map((path, idx) => (
              <path
                key={idx}
                d={path}
                fill="transparent"
                stroke={theme.primary}
                strokeWidth={idx === 2 ? "0.8" : "0.3"}
                className={`transition-opacity duration-1000 ${idx % 2 === 0 ? "opacity-10 animate-pulse" : "opacity-30"}`}
                filter="url(#glow-wire-mesh)"
              />
            ))}

            {gravityNodes.filter(n => n.gravity).map((n, i) => (
              <g key={i}>
                <circle cx={n.x} cy={n.y} r="4" fill={theme.primary} className="opacity-10 animate-ping" />
                <circle
                  cx={n.x} cy={n.y} r="1.5"
                  fill="#ffffff"
                  style={{ filter: `drop-shadow(0 0 4px ${theme.primary})` }}
                />
              </g>
            ))}
          </svg>
        </div>

        {/* 3. LEGENDA (Fixa na direita) */}
        <div className="flex-shrink-0 space-y-4 pl-3 border-l border-white/5 pr-1">
          <div className="flex items-center gap-3 justify-end">
            <span className="text-[10px] font-mono text-slate-400 font-bold">26%</span>
            <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: theme.primary, boxShadow: `0 0 8px ${theme.primary}` }} />
          </div>
          <div className="flex items-center gap-3 justify-end opacity-20">
            <span className="text-[10px] font-mono text-slate-500">18%</span>
            <div className="w-1.5 h-1.5 rounded-full border border-slate-700" />
          </div>
        </div>

      </div>
    </GlassCard>
  );
}