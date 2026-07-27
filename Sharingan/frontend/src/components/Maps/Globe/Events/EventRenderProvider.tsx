import { useMemo, type ReactNode } from 'react';
import { THEMES } from '../../../../constants/colors';
import { useMapEvents } from '../../../../context/useMapEvents';
import { useTheme } from '../../../../context/useTheme';
import { BURST_EMISSION } from './BurstMaterial';
import { EventRenderContext, type EventRenderStyle } from './eventRenderContext';

const STYLES: EventRenderStyle[] = [
  { mode: 'NEGADA', color: THEMES.NEGADA.primary, shape: 'DIAMOND' }, { mode: 'FRAUDE', color: THEMES.FRAUDE.primary, shape: 'HEXAGON' },
  { mode: 'APROVADA', color: THEMES.APROVADA.primary, shape: 'TRIANGLE' }, { mode: 'PENDENTE', color: THEMES.PENDENTE.primary, shape: 'SQUARE' },
];

// Fonte única de eventos para todos os shaders que representam uma emissão.
export function EventRenderProvider({ children }: { children: ReactNode }) {
  const { viewMode } = useTheme(); 
  const { visibleEvents } = useMapEvents();
  const layers = useMemo(() => {
    const styles = viewMode === 'TODOS' ? STYLES : STYLES.filter((style) => style.mode === viewMode);
    return styles.map((style) => ({ style, events: visibleEvents.filter((event) => event.visualMode === style.mode).slice(0, BURST_EMISSION.testEventLimit) }));
  }, [viewMode, visibleEvents]);
  return <EventRenderContext.Provider value={{ layers }}>{children}</EventRenderContext.Provider>;
}
