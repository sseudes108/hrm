import { GlassCard } from "./../Layout/GlassCard";
import { COLORS, THEMES } from "../../constants/colors";

interface AlertProps {
  theme: typeof THEMES.FRAUDE; // ou use a tipagem que preferir
}

const alerts = [
  { id: "AL-9345", time: "10:24:32", type: "CARD FRAUD", location: "SÃO PAULO - SP", account: "**** 7734", amount: "R$ 4.200,00", risk: 92, status: "INVESTIGATING", statusColor: COLORS.anbuRed },
  { id: "AL-8275", time: "00:15:08", type: "ACCOUNT TAKEOVER", location: "RIO DE JANEIRO - RJ", account: "**** 5521", amount: "R$ 9.800,00", risk: 86, status: "HIGH RISK", statusColor: COLORS.anbuRed },
  { id: "AL-7451", time: "05:47:19", type: "WIRE FRAUD", location: "BRASÍLIA - DF", account: "**** 1235", amount: "R$ 15.300,00", risk: 95, status: "PENDING", statusColor: "#3b82f6" },
  { id: "AL-5893", time: "01:33:44", type: "PHISHING", location: "FORTALEZA - CE", account: "**** 7912", amount: "R$ 2.750,00", risk: 66, status: "BLOCKED", statusColor: "#3b82f6" },
  { id: "AL-5592", time: "11:13:32", type: "IDENTITY THEFT", location: "CURITIBA - PR", account: "**** 3001", amount: "R$ 5.100,00", risk: 60, status: "UNDER REVIEW", statusColor: "#3b82f6" },
];

export function RecentAlerts({ theme }: AlertProps) {
  return (
    <GlassCard theme={theme} className="col-span-12 lg:col-span-9 p-0 overflow-hidden">
      {/* HEADER DA TABELA */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-white/5">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: COLORS.anbuRed }} />
          <h2 className="text-[11px] font-black tracking-[0.2em] text-white uppercase">Recent Fraud Alerts</h2>
        </div>
        <button className="text-[9px] font-bold text-slate-500 hover:text-white transition-colors tracking-widest uppercase">View All ▾</button>
      </div>

      {/* TABELA REAL */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-white/5">
              {["ID", "TIME", "TYPE", "LOCATION", "ACCOUNT", "AMOUNT", "RISK SCORE", "STATUS"].map((head) => (
                <th key={head} className="px-6 py-4 text-[9px] font-bold text-slate-500 tracking-widest uppercase">
                  {head}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.02]">
            {alerts.map((alert, i) => (
              <tr key={i} className="group hover:bg-white/[0.03] transition-colors cursor-pointer">
                <td className="px-6 py-4 text-[10px] font-mono text-slate-400">{alert.id}</td>
                <td className="px-6 py-4 text-[10px] font-mono text-slate-500">{alert.time}</td>
                <td className="px-6 py-4 text-[10px] font-bold tracking-wider" style={{ color: alert.statusColor }}>{alert.type}</td>
                <td className="px-6 py-4 text-[10px] font-medium text-slate-400">{alert.location}</td>
                <td className="px-6 py-4 text-[10px] font-mono text-slate-500">{alert.account}</td>
                <td className="px-6 py-4 text-[10px] font-black text-white">{alert.amount}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-black text-white italic">{alert.risk}</span>
                    <div className="flex gap-0.5">
                      {[1, 2, 3].map((dot) => (
                        <div key={dot} className={`w-1 h-1 rounded-full ${alert.risk > 80 ? "bg-rose-600" : "bg-slate-700"}`} />
                      ))}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span 
                    className="px-3 py-1 rounded border text-[9px] font-black tracking-tighter transition-all group-hover:scale-105"
                    style={{ 
                      color: alert.statusColor, 
                      borderColor: `${alert.statusColor}40`,
                      backgroundColor: `${alert.statusColor}10`,
                      boxShadow: `inset 0 0 10px ${alert.statusColor}20`
                    }}
                  >
                    {alert.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassCard>
  );
}