import { MainMap } from './MainMap';

interface MapStageProps {
  isLocked: boolean;
  isFlat: boolean;
}

export function MapStage({ isLocked, isFlat }: MapStageProps) {
  return (
    <div className="absolute inset-0 z-10 overflow-visible">
      <MainMap isLocked={isLocked} isFlat={isFlat} />
    </div>
  );
}
