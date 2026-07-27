import { useState, type ReactNode } from 'react';
import {
  MapVisualizationContext,
  type MapVisualizationMode,
} from './mapVisualizationContext';

export function MapVisualizationProvider({ children }: { children: ReactNode }) {
  const [visualizationMode, setVisualizationMode] = useState<MapVisualizationMode>('BURSTS');

  return (
    <MapVisualizationContext.Provider value={{ visualizationMode, setVisualizationMode }}>
      {children}
    </MapVisualizationContext.Provider>
  );
}
