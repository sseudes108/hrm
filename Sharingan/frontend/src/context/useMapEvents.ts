import { useContext } from 'react';
import { MapEventsContext } from './mapEventsContext';

export function useMapEvents() {
  const context = useContext(MapEventsContext);

  if (!context) {
    throw new Error('useMapEvents must be used within a MapEventsProvider');
  }

  return context;
}
