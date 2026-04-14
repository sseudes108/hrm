import { useMemo } from 'react';
import { THEMES } from '../../constants/colors';
import { Globe } from './Globe/Globe';

interface MainMapProps {
  viewMode: keyof typeof THEMES;
  setViewMode: (mode: keyof typeof THEMES) => void;
  isLocked: boolean; // Recebe o estado do Dashboard
  isFlat: boolean;
}

export function MainMap({ viewMode, isLocked, isFlat}: MainMapProps) {
  const activeTheme = useMemo(() => THEMES[viewMode], [viewMode]);

  return (
    <div 
      className="relative w-full h-full flex items-center justify-center overflow-visible"
      style={{ touchAction: 'none' }}
    >
      <div
        className="absolute w-full h-full z-0"
        style={{ 
          pointerEvents: isLocked ? 'none' : 'auto',
        }}
      >
        <Globe 
          activeTheme={activeTheme}
          isLocked={isLocked}
          isFlat={isFlat}
        />
      </div>
    </div>
  );
}