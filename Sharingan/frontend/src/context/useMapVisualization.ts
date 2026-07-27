import { useContext } from 'react';
import { MapVisualizationContext } from './mapVisualizationContext';

export function useMapVisualization() {
  const context = useContext(MapVisualizationContext);

  if (!context) {
    throw new Error('useMapVisualization must be used within a MapVisualizationProvider');
  }

  return context;
}
