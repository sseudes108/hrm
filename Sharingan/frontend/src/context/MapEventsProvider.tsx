import { useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  MapEventsContext,
  type MapEvent,
  type MapEventCategory,
  type MapEventFilter,
  type MapEventVisualMode,
} from './mapEventsContext';

interface ProposalResponse {
  id: number;
  status: string;
  lat: number;
  lng: number;
  risco_score: number;
  ibge: number;
  regiao: string;
}

const MAX_VISIBLE_EVENTS_PER_MODE = 80;
const API = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';
const FALLBACK_EVENTS: MapEvent[] = [
  { id: 'fallback-1', latitude: -23.5505, longitude: -46.6333, ibge: 3550308, region: 'Sudeste', category: 'CARTAO', visualMode: 'FRAUDE', status: 'Fraude', riskScore: 96 },
  { id: 'fallback-2', latitude: -22.9068, longitude: -43.1729, ibge: 3304557, region: 'Sudeste', category: 'INVASAO', visualMode: 'NEGADA', status: 'Reprovada', riskScore: 72 },
  { id: 'fallback-3', latitude: -19.9167, longitude: -43.9345, ibge: 3106200, region: 'Sudeste', category: 'CARTAO', visualMode: 'APROVADA', status: 'Aprovada', riskScore: 55 },
  { id: 'fallback-4', latitude: -15.7939, longitude: -47.8828, ibge: 5300108, region: 'Centro-Oeste', category: 'INVASAO', visualMode: 'PENDENTE', status: 'Pendenciada', riskScore: 64 },
  { id: 'fallback-5', latitude: -8.0476, longitude: -34.8770, ibge: 2304400, region: 'Nordeste', category: 'CARTAO', visualMode: 'FRAUDE', status: 'Fraude', riskScore: 88 },
  { id: 'fallback-6', latitude: -3.7319, longitude: -38.5267, ibge: 4106902, region: 'Sul', category: 'INVASAO', visualMode: 'NEGADA', status: 'Reprovada', riskScore: 68 },
];

function toMapEvent(proposal: ProposalResponse): MapEvent | null {
  const visualModes: Record<string, MapEventVisualMode> = {
    Reprovada: 'NEGADA',
    Fraude: 'FRAUDE',
    Aprovada: 'APROVADA',
    Pendenciada: 'PENDENTE',
  };
  const visualMode = visualModes[proposal.status];

  if (!visualMode) return null;

  const category: MapEventCategory = visualMode === 'FRAUDE' || visualMode === 'APROVADA'
    ? 'CARTAO'
    : 'INVASAO';

  return {
    id: String(proposal.id),
    latitude: proposal.lat,
    longitude: proposal.lng,
    ibge: proposal.ibge,
    region: proposal.regiao,
    category,
    visualMode,
    status: proposal.status,
    riskScore: proposal.risco_score,
  };
}

function balanceEventsByVisualMode(events: MapEvent[]) {
  const counts: Record<MapEventVisualMode, number> = {
    NEGADA: 0,
    FRAUDE: 0,
    APROVADA: 0,
    PENDENTE: 0,
  };

  return events.filter((event) => {
    if (counts[event.visualMode] >= MAX_VISIBLE_EVENTS_PER_MODE) return false;
    counts[event.visualMode] += 1;
    return true;
  });
}

export function MapEventsProvider({ children }: { children: ReactNode }) {
  const [filter, setFilter] = useState<MapEventFilter>('TODOS');
  const [events, setEvents] = useState<MapEvent[]>(FALLBACK_EVENTS);

  useEffect(() => {
    const controller = new AbortController();

    async function loadEvents() {
      try {
        const response = await fetch(`${API}/propostas?limit=2000`, {
          signal: controller.signal,
        });
        if (!response.ok) return;

        const proposals: ProposalResponse[] = await response.json();
        const mappedEvents = proposals
          .map(toMapEvent)
          .filter((event): event is MapEvent => event !== null)
        const balancedEvents = balanceEventsByVisualMode(mappedEvents);

        if (balancedEvents.length > 0) {
          setEvents(balancedEvents);
        }
      } catch (error) {
        if (!(error instanceof DOMException && error.name === 'AbortError')) {
          setEvents(FALLBACK_EVENTS);
        }
      }
    }

    void loadEvents();
    return () => controller.abort();
  }, []);

  const visibleEvents = useMemo(
    () => events.filter((event) => filter === 'TODOS' || event.category === filter),
    [events, filter],
  );

  return (
    <MapEventsContext.Provider value={{ filter, setFilter, visibleEvents }}>
      {children}
    </MapEventsContext.Provider>
  );
}
