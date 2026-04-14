import { 
  HomeIcon, 
  BellIcon, 
  MagnifyingGlassIcon, 
   ChartBarIcon, 
  ShieldCheckIcon, 
  CogIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from "@heroicons/react/24/outline";
import { COLORS, THEMES } from "../../constants/colors";

interface SidebarProps {
  theme: typeof THEMES.FRAUDE;
  isCollapsed: boolean;
  setIsCollapsed: (v: boolean) => void;
  activePage: string;
  onNavigate: (page: string) => void;
}

export default function Sidebar({ theme, isCollapsed, setIsCollapsed, activePage, onNavigate }: SidebarProps) {
  const menuItems = [
    { name: "Dashboard", icon: HomeIcon, active: true },
    { name: "Alerts", icon: BellIcon, active: false, badge: "Red" },
    { name: "Investigations", icon: MagnifyingGlassIcon, active: false },
    { name: "Analytics", icon: ChartBarIcon, active: false },
    { name: "Network", icon: ShieldCheckIcon, active: false },
    { name: "Settings", icon: CogIcon, active: false },
  ];

  const sidebarGlassStyle = {
    backgroundImage: `
      linear-gradient(125deg, rgba(16, 22, 36, 0.1) 20%, rgba(16, 22, 36, 0.05) 50%, ${COLORS.glassBase} 100%),
      radial-gradient(circle at top left, ${COLORS.whiteGlow} 0%, rgba(255, 255, 255, 0) 35%),
      radial-gradient(circle at bottom right, ${theme.glow} 0%, rgba(225, 29, 72, 0) 45%)
    `,
    
    // MÁGICA: A borda direita começa transparente no topo para não chocar com o Header
    borderRight: "1px solid",
    borderImageSource: `linear-gradient(to bottom, transparent 0px, transparent 60px, ${COLORS.borderWhite} 60px)`,
    borderImageSlice: 1,
    
    backdropFilter: 'blur(1px)', 
  };

  return (
    <aside 
      style={sidebarGlassStyle} 
      className={`
        relative 
        h-full 
        flex flex-col 
        p-4 
        transition-all duration-500 ease-in-out 
        z-40 
        ${isCollapsed ? 'w-20' : 'w-64'}
      `}
    >
      {/* BOTÃO TOGGLE */}
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-10 w-6 h-6 bg-slate-900 border border-white/10 rounded-full flex items-center justify-center hover:border-white/40 transition-all z-[100] shadow-[0_0_10px_rgba(0,0,0,0.5)]"
        style={{ color: theme.primary }}
      >
        {isCollapsed ? <ChevronRightIcon className="w-4 h-4" /> : <ChevronLeftIcon className="w-4 h-4" />}
      </button>

      {/* MENU SUPERIOR */}
      <nav className="space-y-2 flex-grow overflow-y-auto overflow-x-hidden scrollbar-none pt-10 pb-32">
        {menuItems.map((item) => {
          const isActive = activePage === item.name;
          return (
            <div
              key={item.name}
              onClick={() => onNavigate(item.name)}
              className={`relative flex items-center p-3 rounded-lg cursor-pointer transition-all group border ${
                isCollapsed ? 'justify-center' : 'gap-4 px-4'
              } ${
                isActive 
                  ? "bg-white/5 border-white/10 shadow-lg" 
                  : "bg-transparent border-transparent hover:bg-white/[0.03] hover:border-white/5"
              }`}
              style={isActive ? { borderColor: `${theme.primary}40` } : {}}
            >
              {isActive && (
                <div 
                  className="absolute left-0 top-1/4 bottom-1/4 w-1 rounded-r-full"
                  style={{ 
                    backgroundColor: theme.primary,
                    boxShadow: `0 0 15px ${theme.primary}` 
                  }}
                />
              )}
              <item.icon 
                className="w-5 h-5 min-w-[20px] transition-colors" 
                style={{ color: isActive ? theme.primary : 'rgb(148, 163, 184)' }} 
              />
              <span 
                className={`text-xs font-bold tracking-[0.15em] uppercase transition-all duration-300 whitespace-nowrap ${
                  isCollapsed ? 'w-0 opacity-0 ml-0 overflow-hidden' : 'w-full opacity-100 ml-0'
                }`}
                style={{ color: isActive ? '#f8fafc' : 'rgb(148, 163, 184)' }}
              >
                {item.name}
              </span>
            </div>
          );
        })}
      </nav>

      {/* STATUS DO SISTEMA - FIXED: Fica preso à base do monitor */}
      <div 
        className={`fixed bottom-4 transition-all duration-500 pointer-events-none z-50 ${
          isCollapsed ? 'w-20 left-0 px-5' : 'w-64 left-0 px-4'
        }`}
      >
        <div className={`
          relative overflow-hidden backdrop-blur-md transition-all duration-500
          bg-white/[.03] border border-white/5 rounded-xl pointer-events-auto
          ${isCollapsed ? 'h-10 w-10 flex items-center justify-center' : 'p-4 w-full'}
        `}>
          <div className={`flex flex-col relative z-10 items-start justify-center ${isCollapsed ? 'items-center' : 'gap-1'}`}>
            {!isCollapsed && (
              <span className="text-[10px] text-slate-500 font-bold tracking-[0.2em] uppercase w-full text-left opacity-60">
                System Status
              </span>
            )}
            <div className={`flex items-center gap-2 w-full ${isCollapsed ? 'justify-center' : 'justify-start'}`}>
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(16,185,129,0.4)] shrink-0"></div>
              {!isCollapsed && (
                <span className="text-[11px] text-emerald-500 font-black tracking-widest uppercase italic whitespace-nowrap">
                  Operational
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}