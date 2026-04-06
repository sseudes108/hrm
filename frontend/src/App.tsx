import Sidebar from "./components/Sidebar";
import { Header } from "./components/Header";
import { Dashboard } from "./components/Dashboard";
import { useState, useMemo } from 'react';
import { THEMES } from './constants/colors';

const generateStars = (count: number) => {
  let stars = "";
  for (let i = 0; i < count; i++) {
    stars += `${Math.random() * 100}vw ${Math.random() * 100}vh #fff${i === count - 1 ? "" : ","}`;
  }
  return stars;
};

export default function App() {
  const [viewMode, setViewMode] = useState<keyof typeof THEMES>('FRAUDE');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const activeTheme = THEMES[viewMode];

  const starsSmall = useMemo(() => generateStars(600), []);
  const starsMedium = useMemo(() => generateStars(200), []);
  const starsLarge = useMemo(() => generateStars(50), []);

  return (
    <main className="flex flex-col h-screen text-slate-50 overflow-hidden font-sans relative">
      
      {/* 1. ESTRELAS (No fundo do fundo) */}
      <div className="fixed inset-0 pointer-events-none" style={{ zIndex: 0 }}>
        <div className="stars-layer-1 absolute inset-0" style={{ boxShadow: starsSmall, animationDuration: '15s', opacity: 0.3 }} />
        <div className="stars-layer-2 absolute inset-0" style={{ boxShadow: starsMedium, animationDuration: '7s', opacity: 0.5 }} />
        <div className="stars-layer-3 absolute inset-0" style={{ boxShadow: starsLarge, animationDuration: '3s', opacity: 0.8 }} />
      </div>

      {/* 2. CONTEÚDO (Sem div de z-index bloqueando o meio) */}
      <Header theme={activeTheme}/>

      <div className="flex flex-1 overflow-hidden relative">
        <Sidebar 
          theme={activeTheme} 
          isCollapsed={isSidebarCollapsed} 
          setIsCollapsed={setIsSidebarCollapsed} 
        />
        
        {/* O Dashboard e o Mapa estão aqui. 
            Como não há nenhuma div com z-10 cobrindo eles agora, 
            o Portal do mapa consegue capturar o mouse. */}
        <Dashboard viewMode={viewMode} setViewMode={setViewMode} />
      </div>
    </main>
  );
}