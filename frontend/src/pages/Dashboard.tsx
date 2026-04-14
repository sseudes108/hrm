import { useState } from 'react';
import { AlertTrend } from '../components/Dashboard/AlertTrend';
import { FraudByCategory } from '../components/Dashboard/FraudByCategory';
import { KpiCardsLeft, KpiCardsRight } from '../components/Dashboard/KpiColumns';
import { RecentAlerts } from '../components/Dashboard/RecentAlerts';
import { MainMap } from '../components/Maps/MainMap';
import { THEMES } from '../constants/colors';
import { MapHUD } from '../components/Maps/MainHUD';

interface DashboardProps {
  viewMode: keyof typeof THEMES;
  setViewMode: (mode: keyof typeof THEMES) => void;
  isSidebarCollapsed: boolean;
}

export function Dashboard({ viewMode, setViewMode}: DashboardProps) {
  const [isLocked, setIsLocked] = useState(true);
  const [isFlat, setIsFlat] = useState(false);
  const activeTheme = THEMES[viewMode];

  return (
    <section className="flex-1 p-3 relative z-10 overflow-visible pointer-events-none">
      
      {/* 1. O GLOBO (FIXED) 
          O mouse só interage aqui se isLocked for false e se não estiver clicando em um card/HUD */}
      <div 
        className={`fixed inset-0 z-0 flex items-center justify-center transition-all ${
          isLocked ? 'pointer-events-none' : 'pointer-events-auto'
        }`}
      >
        <div className="w-screen h-screen">
          <MainMap 
            viewMode={viewMode} setViewMode={setViewMode} 
            isLocked={isLocked} 
            isFlat={isFlat}
          />
        </div>
      </div>

      {/* BLOCO SUPERIOR: KPIs + HUD Central */}
      <div className="flex gap-3 h-[540px] max-w mx-auto mb-3 relative z-10 pointer-events-none">
        
        {/* KPI ESQUERDA - Reativamos o clique */}
        <div className="w-[22%] pointer-events-auto">
          <KpiCardsLeft theme={activeTheme} />
        </div>

        {/* CENTRO: HUD (Reativamos o clique apenas no HUD) */}
        <div className="flex-1 relative z-20 flex flex-col items-center pointer-events-none">
          <div className="w-full pt-0 mt-0 pointer-events-auto">
            <MapHUD 
              viewMode={viewMode} 
              setViewMode={setViewMode} 
              isLocked={isLocked} 
              setIsLocked={setIsLocked}
              isFlat={isFlat} 
              setIsFlat={setIsFlat}
            />
          </div>
        </div>

        {/* KPI DIREITA - Reativamos o clique */}
        <div className="w-[22%] pointer-events-auto">
          <KpiCardsRight theme={activeTheme} />
        </div>
      </div>

      {/* BLOCO INFERIOR: Tabela e Gráficos */}
      <div className="flex items-stretch gap-3 mt-3 relative z-10 pointer-events-none">
        
        {/* Tabela Registro - Reativamos o clique */}
        <div className="w-[77%] flex-shrink-0 pointer-events-auto">
          <RecentAlerts theme={activeTheme} />
        </div>

        {/* Coluna de Gráficos - Reativamos o clique */}
        <div className="flex-1 flex flex-col gap-3 pointer-events-auto">
          <div className="flex-1">
            <AlertTrend theme={activeTheme} />
          </div>

          <div className="flex-1">
            <FraudByCategory theme={activeTheme} />
          </div>
        </div>
      </div>
      
    </section>
  );
}