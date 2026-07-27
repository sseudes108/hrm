import { createContext } from 'react';
import type { MapEvent } from '../../../../context/mapEventsContext';
import type { BurstShape } from './BurstMaterial';

export interface EventRenderStyle { mode: 'NEGADA' | 'FRAUDE' | 'APROVADA' | 'PENDENTE'; color: string; shape: BurstShape }
export interface EventRenderLayer { style: EventRenderStyle; events: MapEvent[] }
export const EventRenderContext = createContext<{ layers: EventRenderLayer[] } | null>(null);
