import { createContext } from 'react';

export type MapVisualizationMode = 'BURSTS' | 'HEATMAP' | 'SPHERES';

export interface MapVisualizationContextValue {
  visualizationMode: MapVisualizationMode;
  setVisualizationMode: (mode: MapVisualizationMode) => void;
}

export const MapVisualizationContext = createContext<MapVisualizationContextValue | null>(null);
