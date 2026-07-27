import { useMemo, useState, type ReactNode } from 'react';
import { useDashboardData } from './useDashboardData';
import { StateHoverContext } from './stateHoverContext';

export function StateHoverProvider({ children }: { children: ReactNode }) {
  const [hoveredUf, setHoveredUf] = useState<string | null>(null);
  const { states } = useDashboardData();
  const hoveredState = useMemo(() => states.find((state) => state.uf === hoveredUf) ?? null, [hoveredUf, states]);
  return <StateHoverContext.Provider value={{ hoveredUf, hoveredState, setHoveredUf }}>{children}</StateHoverContext.Provider>;
}
