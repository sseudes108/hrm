import { createContext } from 'react';
import type { StateSummary } from './dashboardDataContext';

export interface StateHoverContextValue { hoveredUf: string | null; hoveredState: StateSummary | null; setHoveredUf: (uf: string | null) => void }
export const StateHoverContext = createContext<StateHoverContextValue | null>(null);
