import { useEffect, useState, type ReactNode } from 'react';
import { DashboardDataContext, type DashboardDataContextValue } from './dashboardDataContext';

const API = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';
const EMPTY: DashboardDataContextValue = { summary: null, trend: [], municipalities: [], investigations: [], states: [], loading: true };

export function DashboardDataProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<DashboardDataContextValue>(EMPTY);

  useEffect(() => {
    const controller = new AbortController();
    const fetchJson = async (url: string) => {
      const response = await fetch(url, { signal: controller.signal });
      if (!response.ok) throw new Error(`API indisponível: ${response.status}`);
      return response.json();
    };
    Promise.allSettled([
      fetchJson(`${API}/analytics`),
      fetchJson(`${API}/investigations?limit=30`),
      fetchJson(`${API}/states/summary`),
    ]).then(([analyticsResult, investigationsResult, statesResult]) => {
      const analytics = analyticsResult.status === 'fulfilled' ? analyticsResult.value : null;
      const investigations = investigationsResult.status === 'fulfilled' ? investigationsResult.value : [];
      const states = statesResult.status === 'fulfilled' ? statesResult.value : [];
      setData({
        summary: analytics?.summary ?? null,
        trend: analytics?.trend ?? [],
        municipalities: analytics?.top_municipalities ?? [],
        investigations: Array.isArray(investigations) ? investigations : [],
        states: Array.isArray(states) ? states : [],
        loading: false,
      });
    }).catch(() => setData((current) => ({ ...current, loading: false })));
    return () => controller.abort();
  }, []);

  return <DashboardDataContext.Provider value={data}>{children}</DashboardDataContext.Provider>;
}
