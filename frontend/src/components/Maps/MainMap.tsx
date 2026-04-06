import { useState, useMemo } from 'react';
import ReactDOM from 'react-dom';
import { THEMES } from '../../constants/colors';

import { MapHUD } from './MainHUD';
import { BrazilCanvas } from './BrazilMap/BrazilCanvas';
import { Globe } from './Globe/Globe';

interface MainMapProps {
  viewMode: keyof typeof THEMES;
  setViewMode: (mode: keyof typeof THEMES) => void;
}

export function MainMap({ viewMode, setViewMode }: MainMapProps) {
  // O estado de Lock agora controla diretamente o comportamento do Canvas
  const [isLocked, setIsLocked] = useState(true);

  // O tema ativo baseado no viewMode (Fraude, Aprovada, etc)
  const activeTheme = useMemo(() => THEMES[viewMode], [viewMode]);

  return ReactDOM.createPortal(
    <>
      {/* 1. Interface de Usuário (Z-Index alto para ficar sobre o mapa) */}
      <div style={{ position: 'relative', zIndex: 10 }}>
        <MapHUD 
          viewMode={viewMode} 
          setViewMode={setViewMode} 
          isLocked={isLocked} 
          setIsLocked={setIsLocked} 
        />
      </div>

      {/* 2. Camada do Mapa (Ocupa o fundo) */}
      <div 
        className="fixed inset-0 overflow-hidden" 
        style={{ 
          zIndex: 1, 
          // Se estiver travado, os cliques passam "através" do canvas para a UI abaixo
          // Se estiver destravado, o canvas captura o mouse para girar o globo
          pointerEvents: isLocked ? 'none' : 'auto' 
        }}
      >
        {/* <Globe 
          activeTheme={activeTheme}
          isLocked={isLocked}
        /> */}
        <BrazilCanvas
          activeTheme={activeTheme}
          isLocked={isLocked}
        />
      </div>
    </>,
    document.body
  );
}