import { THEMES } from '../constants/colors';
import { AlertTrend } from "./AlertTrend";
import { FraudByCategory } from "./FraudByCategory";
import { KpiCardsLeft, KpiCardsRight } from "./KpiColumns";
import { MainMap } from './Maps/MainMap';
import { RecentAlerts } from "./RecentAlerts";

interface DashboardProps {
  viewMode: keyof typeof THEMES;
  setViewMode: (mode: keyof typeof THEMES) => void;
}

export function Dashboard({ viewMode, setViewMode }: DashboardProps) {
  // Movemos o estado para cá para controlar o Dashboard inteiro
  const activeTheme = THEMES[viewMode];

  return (
    <section className="flex-1 p-3 overflow-y-auto relative z-10 pointer-events-none">
      
      <div className="flex gap-3 h-[540px] max-w mx-auto mb-3">
        {/* Fraud / Risk Transaction / Status C*/}
        <div className="w-[22%] pointer-events-auto">
          <KpiCardsLeft theme={activeTheme} />
        </div>

        {/* Mapa */}
        <div className="flex-1 bg-transparent border-none flex items-center justify-center overflow-hidden">
          <MainMap viewMode={viewMode} setViewMode={setViewMode} />
        </div>

        {/* Total Loss / Status A / Status B / Risk Score Dist. */}
        <div className="w-[22%] pointer-events-auto">
          <KpiCardsRight theme={activeTheme} />
        </div>
      </div>

      <div className="flex items-stretch gap-3 mt-3 ">
        {/* Tabela Registro */}
        <div className="w-[77%] flex-shrink-0 pointer-events-auto">
          <RecentAlerts theme={activeTheme} />
        </div>

        <div className="flex-1 flex flex-col gap-3 pointer-events-auto">
          {/* Alert Trend */}
          <div className="flex-1">
            <AlertTrend theme={activeTheme} />
          </div>

          {/* Category */}
          <div className="flex-1">
            <FraudByCategory theme={activeTheme} />
          </div>
        </div>
      </div>
      
    </section>
  );
}