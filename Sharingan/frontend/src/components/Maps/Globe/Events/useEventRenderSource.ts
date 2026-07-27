import { useContext } from 'react';
import { EventRenderContext } from './eventRenderContext';
export function useEventRenderSource() { const context = useContext(EventRenderContext); if (!context) throw new Error('useEventRenderSource must be used within EventRenderProvider'); return context; }
