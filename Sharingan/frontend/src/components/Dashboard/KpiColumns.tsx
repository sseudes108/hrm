import { SummaryCard } from "./../Layout/Cards";
import { GlassCard } from "./../Layout/GlassCard";
import { RiskScoreCard } from "./RiskScoreCard";
import { useDashboardData } from '../../context/useDashboardData';

const formatNumber = (value: number) => new Intl.NumberFormat('pt-BR').format(value);
const formatCurrency = (value: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(value);

function statusCount(statuses: { status: string; count: number }[], status: string) {
  return statuses.find((item) => item.status === status)?.count ?? 0;
}

export function KpiCardsLeft() {
  const { summary } = useDashboardData();
  const statuses = summary?.by_status ?? [];
  const frauds = statusCount(statuses, 'Fraude');
  const pending = statusCount(statuses, 'Pendenciada');
  const total = summary?.total ?? 0;
  return (
    <div className="h-full flex flex-col space-y-3">
      <SummaryCard
        title="Fraud Alerts" 
        subtitle="This Month" 
        value={formatNumber(frauds)}
        percentage={total ? `${((frauds / total) * 100).toFixed(1)}%` : '—'}
      />
      
      <SummaryCard
        title="High Risk Trans." 
        subtitle="Active" 
        value={formatNumber(summary?.high_risk_count ?? 0)}
        percentage={summary ? `${summary.high_risk_rate}%` : '—'}
      />

      {/* 3. flex-1 faz este GlassCard "comer" todo o espaço que sobrar na base.
      */}
      <GlassCard className="p-4 flex-1 flex flex-col justify-start">
        <span className="text-[9px] text-slate-500 uppercase tracking-widest">Pendentes</span>
        <div className="text-xl font-bold text-white mt-1">{formatNumber(pending)}</div>
        
        {/* Dica: Você pode colocar um gráfico ou info extra aqui no futuro 
            já que ele terá bastante espaço vertical agora */}
      </GlassCard>
    </div>
  );
}

export function KpiCardsRight() {
  const { summary } = useDashboardData();
  const statuses = summary?.by_status ?? [];
  const total = summary?.total ?? 0;
  const approved = statusCount(statuses, 'Aprovada');
  const denied = statusCount(statuses, 'Reprovada');
  return (
    <div className="h-full flex flex-col space-y-3">
      <SummaryCard 
        title="Total Losses" 
        subtitle="Estimated" 
        value={formatCurrency(summary?.total_value ?? 0)}
        percentage={`${formatNumber(summary?.total ?? 0)} propostas`}
      />
      
    {/* Linha de baixo dividida em dois */}
      <div className="grid grid-cols-2 gap-4">
        <GlassCard className="p-4">
          <span className="text-[9px] text-slate-500 uppercase">Aprovadas</span>
          <div className="text-xl font-bold text-white">{total ? `${((approved / total) * 100).toFixed(1)}%` : '—'}</div>
        </GlassCard>

        <GlassCard className="p-4">
          <span className="text-[9px] text-slate-500 uppercase">Reprovadas</span>
          <div className="text-xl font-bold text-white">{formatNumber(denied)}</div>
        </GlassCard>
      </div>
      
      <RiskScoreCard />
    </div>
  );
}
