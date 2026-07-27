import { AreaChart, BarChart, Text } from '@tremor/react';
import { GlassCard } from '../components/Layout/GlassCard';
import { useDashboardData } from '../context/useDashboardData';
import { useTheme } from '../context/useTheme';

export function Analytics() {
  const { trend, municipalities, summary } = useDashboardData();
  const { theme } = useTheme();
  const formatCurrency = (value: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(value);

  return <section className="pointer-events-auto min-h-full p-6 md:p-8">
    <header className="mb-6 flex items-end justify-between">
      <div><Text className="text-xs font-black tracking-[0.25em] text-white uppercase">Analytics</Text><Text className="text-[9px] tracking-widest text-slate-500 uppercase">Tendência operacional · últimos 14 ciclos</Text></div>
      <div className="text-right"><div className="text-[9px] tracking-widest text-slate-500 uppercase">Volume monitorado</div><div className="text-lg font-black" style={{ color: theme.primary }}>{summary?.total.toLocaleString('pt-BR') ?? '—'}</div></div>
    </header>
    <div className="grid gap-4 xl:grid-cols-3">
      <GlassCard className="min-h-[250px] p-5 xl:col-span-2"><Text className="text-[10px] font-black tracking-widest text-white uppercase">Propostas por ciclo</Text><AreaChart className="mt-5 h-48" data={trend} index="period" categories={['proposals']} colors={[theme.primary]} showLegend={false} showGridLines={false} /></GlassCard>
      <GlassCard className="min-h-[250px] p-5"><Text className="text-[10px] font-black tracking-widest text-white uppercase">Alto risco</Text><BarChart className="mt-5 h-48" data={trend} index="period" categories={['high_risk']} colors={[theme.primary]} showLegend={false} showGridLines={false} /></GlassCard>
      <GlassCard className="p-5 xl:col-span-3"><div className="mb-4 flex justify-between"><Text className="text-[10px] font-black tracking-widest text-white uppercase">Ranking geográfico por risco médio</Text><Text className="text-[9px] text-slate-500 uppercase">Base preparada para consulta agregada no PostgreSQL</Text></div><div className="grid gap-2 md:grid-cols-2 xl:grid-cols-4">{municipalities.map((item, index) => <div key={`${item.municipio}-${item.uf}`} className="rounded-lg border border-white/5 bg-black/20 p-3"><div className="flex justify-between text-[9px] text-slate-500"><span>#{index + 1}</span><span>{item.average_risk.toFixed(1)} risco</span></div><div className="mt-1 text-xs font-black text-white">{item.municipio} · {item.uf}</div><div className="mt-2 text-[10px]" style={{ color: theme.primary }}>{formatCurrency(item.value)}</div></div>)}</div></GlassCard>
    </div>
  </section>;
}
