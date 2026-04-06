import type { THEMES } from "../constants/colors";
import { SummaryCard } from "./Cards";
import { GlassCard } from "./GlassCard";
import { RiskScoreCard } from "./RiskScoreCard";

interface KpiProps {
  theme: typeof THEMES.FRAUDE; // ou use a tipagem que preferir
}

export function KpiCardsLeft({ theme }: KpiProps) {
  return (
    <div className="h-full flex flex-col space-y-3">
      <SummaryCard
        theme={theme}
        title="Fraud Alerts" 
        subtitle="This Month" 
        value="427" 
        percentage="12%" 
      />
      
      <SummaryCard
        theme={theme}
        title="High Risk Trans." 
        subtitle="Active" 
        value="1.258" 
        percentage="28.1%" 
      />

      {/* 3. flex-1 faz este GlassCard "comer" todo o espaço que sobrar na base.
      */}
      <GlassCard theme={theme} className="p-4 flex-1 flex flex-col justify-start">
        <span className="text-[9px] text-slate-500 uppercase tracking-widest">Status C</span>
        <div className="text-xl font-bold text-white mt-1">54000</div>
        
        {/* Dica: Você pode colocar um gráfico ou info extra aqui no futuro 
            já que ele terá bastante espaço vertical agora */}
      </GlassCard>
    </div>
  );
}

export function KpiCardsRight({ theme }: KpiProps) {
  return (
    <div className="h-full flex flex-col space-y-3">
      <SummaryCard 
        theme={theme}
        title="Total Losses" 
        subtitle="Estimated" 
        value="R$ 3.560.900" 
        percentage="30.1%" 
      />
      
    {/* Linha de baixo dividida em dois */}
      <div className="grid grid-cols-2 gap-4">
        <GlassCard theme={theme} className="p-4">
          <span className="text-[9px] text-slate-500 uppercase">Status A</span>
          <div className="text-xl font-bold text-white">89%</div>
        </GlassCard>

        <GlassCard theme={theme} className="p-4">
          <span className="text-[9px] text-slate-500 uppercase">Status B</span>
          <div className="text-xl font-bold text-white">12ms</div>
        </GlassCard>
      </div>
      
      <RiskScoreCard theme={theme} />
    </div>
  );
}