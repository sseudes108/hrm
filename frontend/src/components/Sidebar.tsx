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
import { COLORS, THEMES } from "../constants/colors";

interface SidebarProps {
  theme: typeof THEMES.FRAUDE;
  isCollapsed: boolean;
  setIsCollapsed: (v: boolean) => void;
}

export default function Sidebar({ theme, isCollapsed, setIsCollapsed }: SidebarProps) {
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
    borderRight: `1px solid ${COLORS.borderWhite}`,
    backdropFilter: 'blur(1px)', 
  };

  return (
    <aside 
      style={sidebarGlassStyle} 
      className={`relative h-full transition-all duration-500 ease-in-out z-50 flex flex-col p-4 ${isCollapsed ? 'w-20' : 'w-64'}`}
    >
      {/* BOTÃO TOGGLE - Estilo Sharingan */}
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-10 w-6 h-6 bg-slate-900 border border-white/10 rounded-full flex items-center justify-center hover:border-white/40 transition-all z-[100] shadow-[0_0_10px_rgba(0,0,0,0.5)]"
        style={{ color: theme.primary }}
      >
        {isCollapsed ? <ChevronRightIcon className="w-4 h-4" /> : <ChevronLeftIcon className="w-4 h-4" />}
      </button>

      {/* MENU SUPERIOR */}
      <nav className="space-y-2">
        {menuItems.map((item) => (
          <div
            key={item.name}
            className={`relative flex items-center p-3 rounded-lg cursor-pointer transition-all group border ${
              isCollapsed ? 'justify-center' : 'gap-4 px-4'
            } ${
              item.active 
                ? "bg-white/5 border-white/10 shadow-lg" 
                : "bg-transparent border-transparent hover:bg-white/[0.03] hover:border-white/5"
            }`}
            style={item.active ? { borderColor: `${theme.primary}40` } : {}}
          >
            {/* Linha indicadora lateral dinâmica */}
            {item.active && (
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
              style={{ color: item.active ? theme.primary : 'rgb(148, 163, 184)' }} 
            />
            
            {/* TEXTO: Ocupa 0 de largura e fica invisível no modo colapsado */}
            <span 
              className={`text-xs font-bold tracking-[0.15em] uppercase transition-all duration-300 overflow-hidden whitespace-nowrap ${
                isCollapsed ? 'w-0 opacity-0 ml-0' : 'w-full opacity-100'
              }`}
              style={{ color: item.active ? '#f8fafc' : 'rgb(148, 163, 184)' }}
            >
              {item.name}
            </span>

            {/* Tooltip flutuante quando colapsado */}
            {isCollapsed && (
              <div className="absolute left-16 bg-slate-900 border border-white/10 px-2 py-1 rounded text-[10px] uppercase tracking-tighter opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-[110] whitespace-nowrap">
                {item.name}
              </div>
            )}
          </div>
        ))}
      </nav>

      {/* STATUS DO SISTEMA - Compacto quando colapsado */}
      <div className={`mt-auto p-4 bg-white/[.06] border border-white/10 rounded-xl relative overflow-hidden backdrop-blur-sm transition-all duration-500 ${isCollapsed ? 'p-2' : 'p-4'}`}>
        <div className="flex flex-col gap-1 relative z-10 items-center justify-center">
          {!isCollapsed && <span className="text-[10px] text-slate-500 font-bold tracking-widest uppercase w-full text-left">System Status</span>}
          
          <div className="flex items-center gap-2 w-full justify-start">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)] shrink-0"></div>
            {!isCollapsed && <span className="text-[11px] text-emerald-500 font-black tracking-widest uppercase">Operational</span>}
          </div>
        </div>
        
        <div 
          className="absolute -bottom-4 -right-4 w-12 h-12 blur-2xl rounded-full opacity-10"
          style={{ backgroundColor: theme.primary }}
        />
      </div>
    </aside>
  );
}