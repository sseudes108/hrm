import { useMemo, useState } from 'react';
import { THEMES } from './constants/colors';
import { Header } from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import { Dashboard } from './pages/Dashboard';

// Mock de outras páginas para teste
const AlertsPage = () => <div className="p-10 text-white">Alerts Content - Fundo Customizado aqui</div>;
const SettingsPage = () => <div className="p-10 text-white">Settings Content - Fundo Customizado aqui</div>;

const generateStars = (count: number) => {
  let stars = "";
  for (let i = 0; i < count; i++) {
    const x = Math.random() * 120 - 10; 
    const y = Math.random() * 120 - 10;
    stars += `${x}vw ${y}vh #fff${i === count - 1 ? "" : ","}`;
  }
  return stars;
};

export default function App() {
  const [viewMode, setViewMode] = useState<keyof typeof THEMES>('FRAUDE');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [activePage, setActivePage] = useState('Dashboard'); 

  const activeTheme = THEMES[viewMode];

  const starsSmall = useMemo(() => generateStars(600), []);
  const starsMedium = useMemo(() => generateStars(200), []);
  const starsLarge = useMemo(() => generateStars(50), []);

  const renderPage = () => {
    switch (activePage) {
      case 'Dashboard':
        return <Dashboard viewMode={viewMode} setViewMode={setViewMode} isSidebarCollapsed={isSidebarCollapsed}/>;
      case 'Alerts':
        return <AlertsPage />;
      case 'Settings':
        return <SettingsPage />;
      default:
        return <Dashboard viewMode={viewMode} setViewMode={setViewMode} isSidebarCollapsed={isSidebarCollapsed}/>;
    }
  };

  return (
      <div className="flex flex-col h-screen w-screen overflow-hidden relative font-sans text-slate-50 bg-[#020408]">
    
        {/* ESTRELAS */}
        <div className="fixed -inset-[10%] pointer-events-none z-0 overflow-hidden">
          <div className="stars-layer-1" style={{ boxShadow: starsSmall, opacity: 0.3 }} />
          <div className="stars-layer-2" style={{ boxShadow: starsMedium, opacity: 0.5 }} />
          <div className="stars-layer-3" style={{ boxShadow: starsLarge, opacity: 0.8 }} />
        </div>

        {/* UI SHELL */}
        <div className="flex flex-col h-full w-full relative z-10 bg-transparent pointer-events-none">
          
          <div className="pointer-events-auto shrink-0">
            <Header theme={activeTheme} />
          </div>

          {/* ÁREA CENTRAL: Adicionado h-full e overflow-hidden para travar a Sidebar */}
          <div className="flex flex-1 overflow-hidden relative bg-transparent">
            
            <div className="pointer-events-auto h-full flex-shrink-0">
              <Sidebar 
                theme={activeTheme} 
                isCollapsed={isSidebarCollapsed} 
                setIsCollapsed={setIsSidebarCollapsed}
                activePage={activePage}
                onNavigate={setActivePage}
              />
            </div>
            
            <main className="flex-1 h-full overflow-y-auto overflow-x-hidden relative custom-scrollbar bg-transparent pointer-events-none">
              {renderPage()}
            </main>
          </div>
        </div>
      </div>
    );
  }