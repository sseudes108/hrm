import { createContext } from 'react';

export type MapEventCategory = 'CARTAO' | 'INVASAO';
export type MapEventFilter = 'TODOS' | MapEventCategory;
export type MapEventVisualMode = 'NEGADA' | 'FRAUDE' | 'APROVADA' | 'PENDENTE';

export interface MapEvent {
  id: string;
  latitude: number;
  longitude: number;
  ibge: number;
  region: string;
  category: MapEventCategory;
  visualMode: MapEventVisualMode;
  status: string;
  riskScore: number;
}

export interface MapEventsContextValue {
  filter: MapEventFilter;
  setFilter: (filter: MapEventFilter) => void;
  visibleEvents: MapEvent[];
}

export const MapEventsContext = createContext<MapEventsContextValue | null>(null);
