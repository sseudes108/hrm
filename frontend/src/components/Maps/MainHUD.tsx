import { THEMES } from '../../constants/colors';

interface MapHUDProps {
  viewMode: keyof typeof THEMES;
  setViewMode: (mode: keyof typeof THEMES) => void;
  isLocked: boolean;
  setIsLocked: (locked: boolean) => void;
}

export function MapHUD({ viewMode, setViewMode, isLocked, setIsLocked }: MapHUDProps) {
  return (
    <div className="fixed top-24 right-[23%] z-[9999] flex items-stretch gap-3 h-9 pointer-events-auto">
      {/* SELETOR DE TEMAS */}
      <div className="relative flex p-1 bg-black/40 backdrop-blur-md border border-white/10 rounded-full shadow-xl overflow-hidden">
        <div 
          className="absolute h-[calc(100%-8px)] top-1 bg-white rounded-full transition-all duration-500 ease-in-out shadow-[0_0_15px_rgba(255,255,255,0.3)]"
          style={{
            width: '100px',
            left: `${Object.keys(THEMES).indexOf(viewMode) * 100 + 4}px`, 
          }}
        />

        {Object.keys(THEMES).map((mode) => (
          <button
            key={mode}
            onClick={() => setViewMode(mode as any)}
            className={`relative z-10 min-w-[100px] px-4 py-1.5 rounded-full text-[9px] font-bold tracking-widest transition-colors duration-500 ${
              viewMode === mode ? 'text-black' : 'text-white/40 hover:text-white'
            }`}
          >
            {mode}
          </button>
        ))}
      </div>

      {/* BOTÃO LOCK */}
      <button 
        onClick={() => setIsLocked(!isLocked)}
        className={`min-w-[100px] h-full px-4 border text-[9px] uppercase font-bold rounded-full transition-all duration-500 shadow-lg ${
          isLocked 
          ? 'bg-rose-600/20 border-rose-500 text-rose-500 shadow-[0_0_15px_rgba(225,29,72,0.3)]' 
          : 'bg-white/10 border-white text-white hover:bg-white/20'
        }`}
      >
        {isLocked ? 'LOCK: ON' : 'LOCK: OFF'}
      </button>
    </div>
  );
}