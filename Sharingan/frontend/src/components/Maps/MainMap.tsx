import { Globe } from './Globe/Globe';

interface MainMapProps {
  isLocked: boolean; // Recebe o estado do Dashboard
  isFlat: boolean;
}

export function MainMap({ isLocked, isFlat}: MainMapProps) {
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
          isLocked={isLocked}
          isFlat={isFlat}
        />
      </div>
    </div>
  );
}
