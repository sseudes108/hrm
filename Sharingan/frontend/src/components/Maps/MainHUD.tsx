import { THEMES, type ThemeMode } from '../../constants/colors';
import { useTheme } from '../../context/useTheme';
import { useMapEvents } from '../../context/useMapEvents';
import { useMapVisualization } from '../../context/useMapVisualization';
import type { MapEventFilter } from '../../context/mapEventsContext';
import { Lock, Unlock, ChevronDown, Filter, Map, Globe as GlobeIcon, Radio, Flame, Circle } from 'lucide-react';

interface MapHUDProps {
  isLocked: boolean;
  setIsLocked: (locked: boolean) => void;
  isFlat: boolean;
  setIsFlat: (flat: boolean) => void; // Corrigido o nome do parâmetro para 'flat'
}

const themeModes = Object.keys(THEMES) as ThemeMode[];

export function MapHUD({ isLocked, setIsLocked, isFlat, setIsFlat }: MapHUDProps) {
  const { viewMode, setViewMode } = useTheme();
  const { filter, setFilter } = useMapEvents();
  const { visualizationMode, setVisualizationMode } = useMapVisualization();
  return (
    <div className="relative w-full pointer-events-none flex items-start justify-between px-1">
      
      {/* 1. SEÇÃO ESQUERDA: FILTRO SLIM */}
      <div className="flex items-center bg-black/60 backdrop-blur-md border border-white/5 rounded-md pointer-events-auto h-7">
        <div className="px-2 border-r border-white/5 h-full flex items-center">
          <Filter size={10} className="text-white/40" />
        </div>
        <div className="relative group px-2">
          <select
            value={filter}
            onChange={(event) => setFilter(event.target.value as MapEventFilter)}
            className="appearance-none bg-transparent text-white text-[7.5px] font-bold uppercase tracking-widest pr-4 py-1 cursor-pointer focus:outline-none"
          >
            <option value="TODOS" className="bg-zinc-950">FILTRAR</option>
            <option value="CARTAO" className="bg-zinc-950">CARTÃO</option>
            <option value="INVASAO" className="bg-zinc-950">INVASÃO</option>
          </select>
          <ChevronDown className="absolute right-0 top-1/2 -translate-y-1/2 text-white/20" size={8} />
        </div>
      </div>

      {/* 2. SEÇÃO CENTRAL: STATUS MICRO */}
      <div className="flex items-center p-0.5 bg-black/60 backdrop-blur-md border border-white/5 rounded-full pointer-events-auto h-7">
        <div className="relative flex bg-white/5 rounded-full p-0.5 h-full items-center">
          <div 
            className="absolute h-[calc(100%-4px)] bg-white rounded-full transition-all duration-500 ease-out shadow-[0_0_8px_rgba(255,255,255,0.3)]"
            style={{
              width: '55px',
              left: `${themeModes.indexOf(viewMode) * 55 + 2}px`, 
            }}
          />

          {themeModes.map((mode) => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              className={`relative z-10 min-w-[55px] px-1 text-[7px] font-black tracking-[0.15em] transition-colors duration-500 uppercase ${
                viewMode === mode ? 'text-black' : 'text-white/30 hover:text-white'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
      </div>

      {/* 3. SEÇÃO DIREITA: CONTROLES (Flat Map + Lock) */}
      <div className="flex items-center gap-1.5 pointer-events-auto">
        <div className="flex h-7 items-center rounded-md border border-white/5 bg-black/60 p-0.5 backdrop-blur-md">
          <button
            onClick={() => setVisualizationMode('BURSTS')}
            className={`flex h-full w-7 items-center justify-center rounded transition-all duration-300 ${
              visualizationMode === 'BURSTS' ? 'bg-white/15 text-white' : 'text-white/30 hover:text-white'
            }`}
            title="Emissões geométricas"
          >
            <Radio size={12} strokeWidth={2.5} />
          </button>
          <button
            onClick={() => setVisualizationMode('HEATMAP')}
            className={`flex h-full w-7 items-center justify-center rounded transition-all duration-300 ${
              visualizationMode === 'HEATMAP' ? 'bg-white/15 text-white' : 'text-white/30 hover:text-white'
            }`}
            title="Mapa de calor"
          >
            <Flame size={12} strokeWidth={2.5} />
          </button>
          <button
            onClick={() => setVisualizationMode('SPHERES')}
            className={`flex h-full w-7 items-center justify-center rounded transition-all duration-300 ${
              visualizationMode === 'SPHERES' ? 'bg-white/15 text-white' : 'text-white/30 hover:text-white'
            }`}
            title="Esferas agregadas"
          >
            <Circle size={12} strokeWidth={2.5} />
          </button>
        </div>
        
        {/* NOVO BOTÃO: FLAT MAP TOGGLE */}
        <button 
          onClick={() => setIsFlat(!isFlat)}
          className={`flex items-center justify-center w-7 h-7 rounded-md border transition-all duration-500 ${
            isFlat 
            ? 'bg-amber-500/20 border-amber-500/50 text-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.2)]' 
            : 'bg-black/60 border-white/5 text-white/30 hover:bg-white/10'
          }`}
          title={isFlat ? "Modo Globo" : "Modo Plano"}
        >
          {isFlat ? (
            <GlobeIcon size={12} strokeWidth={2.5} />
          ) : (
            <Map size={12} strokeWidth={2.5} />
          )}
        </button>

        {/* BOTÃO LOCK ORIGINAL */}
        <button 
          onClick={() => setIsLocked(!isLocked)}
          className={`flex items-center justify-center w-7 h-7 rounded-md border transition-all duration-500 ${
            isLocked 
            ? 'bg-rose-600/20 border-rose-500/50 text-rose-500 shadow-[0_0_15px_rgba(225,29,72,0.3)]' 
            : 'bg-black/60 border-white/5 text-white/30 hover:bg-white/10'
          }`}
        >
          {isLocked ? (
            <Lock size={12} strokeWidth={2.5} />
          ) : (
            <Unlock size={12} strokeWidth={2.5} />
          )}
        </button>
      </div>

    </div>
  );
}
