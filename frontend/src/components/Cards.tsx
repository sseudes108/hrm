import { Text, Metric } from "@tremor/react";
import { CurrencyDollarIcon } from "@heroicons/react/24/outline";
import { GlassCard } from "./GlassCard";
import { THEMES } from "../constants/colors"; 

interface CardProps {
  title: string;
  subtitle: string;
  value: string;
  percentage: string;
  theme: typeof THEMES.FRAUDE;
}

export function SummaryCard({ theme, title, subtitle, value, percentage }: CardProps) {
  return (
    <GlassCard theme={theme} className="group relative transition-all duration-700 hover:scale-[1.01]">
      
      <div className="relative z-20">
        <div className="flex justify-between items-start mb-6">
          <div>
            <Text className="text-slate-100 font-bold tracking-[0.2em] uppercase text-[10px]">
              {title}
            </Text>
            <Text className="text-slate-500 font-mono text-[9px] uppercase mt-1 tracking-widest opacity-60">
              {subtitle}
            </Text>
          </div>
          
          {/* AJUSTE 1: A borda do ícone agora usa theme.primary com 40% de opacidade */}
          <div 
            className="p-2 bg-slate-950/80 border rounded-xl transition-all"
            style={{ 
               borderColor: `${theme.primary}66`, // Injetamos a cor do tema aqui
               boxShadow: `inset 0 0 12px ${theme.primary}22` 
            }}
          >
            <CurrencyDollarIcon 
              className="w-5 h-5 transition-colors duration-500" 
              style={{ color: theme.primary }} // Ícone segue o tema
            />
          </div>
        </div>

        <div className="mb-4">
          {/* AJUSTE 2: O Valor principal (Metric) ganha a cor e o drop-shadow do tema */}
          <Metric 
            className="font-black text-2xl tracking-tighter transition-all duration-500"
            style={{ 
              color: theme.primary,
              filter: `drop-shadow(0 0 15px ${theme.primary}44)` 
            }}
          >
            {value}
          </Metric>
        </div>

        <div className="flex items-center gap-2">
          {/* AJUSTE 3: Seta e porcentagem seguem o tema */}
          <span style={{ color: theme.primary }} className="text-xs transition-colors duration-500">▲</span>
          <span 
            className="font-bold text-xs tracking-widest transition-colors duration-500" 
            style={{ color: theme.primary }}
          >
            {percentage}
          </span>
          <span className="text-slate-600 text-[9px] font-medium uppercase ml-1 tracking-tighter italic">
            vs last month
          </span>
        </div>
      </div>

      {/* AJUSTE 4: O Gráfico de Fundo (SVG) */}
      <div className="absolute bottom-0 left-0 w-full h-16 pointer-events-none overflow-hidden rounded-b-2xl z-0">
        <svg className="w-full h-full opacity-10 group-hover:opacity-30 transition-opacity duration-700" preserveAspectRatio="none">
          <path 
            d="M0 60 L40 55 L80 58 L120 40 L160 50 L200 30 L240 45 L280 25 L320 50 V60 H0 Z" 
            stroke={theme.primary} // Linha do gráfico segue o tema
            strokeWidth="0.5" 
            fill={`url(#grad-${theme.primary.replace('#', '')})`} // ID único para o gradiente
          />
          <defs>
            {/* Criamos um gradiente dinâmico baseado na cor do tema */}
            <linearGradient id={`grad-${theme.primary.replace('#', '')}`} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" style={{ stopColor: theme.primary, stopOpacity: 0.5 }} />
              <stop offset="100%" style={{ stopColor: theme.primary, stopOpacity: 0 }} />
            </linearGradient>
          </defs>
        </svg>
      </div>

    </GlassCard>
  );
}