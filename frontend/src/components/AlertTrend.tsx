import { AreaChart, Text } from "@tremor/react";
import { GlassCard } from "./GlassCard";
import { THEMES } from "../constants/colors";

const chartData = [
  { date: "28/03", alerts: 45 },
  { date: "29/03", alerts: 52 },
  { date: "30/03", alerts: 48 },
  { date: "31/03", alerts: 61 },
  { date: "01/04", alerts: 55 },
  { date: "02/04", alerts: 67 },
  { date: "03/04", alerts: 60 },
];

interface TrendProps {
  theme: typeof THEMES.FRAUDE; // ou use a tipagem que preferir
}

export function AlertTrend({ theme }: TrendProps) {
  return (
    <GlassCard theme={theme} className="p-4 flex flex-col h-full">
      <div className="flex justify-between items-start mb-4">
        <div>
          <Text className="text-[10px] font-black text-slate-100 tracking-widest uppercase">Alert Trend</Text>
          <Text className="text-[8px] text-slate-500 uppercase">Last 7 days</Text>
        </div>
        <div className="px-2 py-1 bg-slate-900/50 border border-white/5 rounded text-[8px] text-slate-400 font-mono">
          798 total
        </div>
      </div>
      
      <div className="flex-1 -mx-2">
        <AreaChart
          className="h-full w-full"
          data={chartData}
          index="date"
          categories={["alerts"]}
          colors={[theme.primary]}
          showXAxis={false}
          showYAxis={false}
          showLegend={false}
          showGridLines={false}
          startEndOnly={true}
          style={{ color: theme.primary }}
        />
      </div>
    </GlassCard>
  );
}