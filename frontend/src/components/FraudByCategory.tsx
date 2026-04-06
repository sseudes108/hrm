import { Text } from "@tremor/react";
import { GlassCard } from "./GlassCard";
import { THEMES } from "../constants/colors";

interface FraudCategoryProps {
  theme: typeof THEMES.FRAUDE; // ou use a tipagem que preferir
}

export function FraudByCategory({ theme }: FraudCategoryProps) {
  const categories = [
    { label: "Card Fraud", value: 49, color: theme.primary },
    { label: "Account Takeover", value: 28, color: theme.primary + "aa" }, // Mais suave
    { label: "Wire Fraud", value: 13, color: theme.primary + "50" }, // Bem suave
  ];

  return (
    <GlassCard theme={theme} className="p-4 flex flex-col h-full">
      <div className="flex justify-between items-center mb-6">
        <Text className="text-[10px] font-black text-slate-100 tracking-widest uppercase">Fraud by Category</Text>
        <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: theme.primary }} />
      </div>

      <div className="space-y-5">
        {categories.map((cat) => (
          <div key={cat.label}>
            <div className="flex justify-between items-center mb-1">
              <Text className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">{cat.label}</Text>
              <Text className="text-[9px] font-black text-white italic">{cat.value}%</Text>
            </div>
            <div className="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000 shadow-[0_0_10px_rgba(225,29,72,0.4)]"
                  style={{ 
                    width: `${cat.value}%`, 
                    backgroundColor: theme.primary,
                    filter: `brightness(${1.2 - (categories.indexOf(cat) * 0.2)})` // Diminui o brilho conforme desce
                  }}
                />
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}