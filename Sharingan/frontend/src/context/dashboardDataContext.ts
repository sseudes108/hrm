import { createContext } from 'react';

export interface StatusMetric { status: string; count: number; total_value: number; average_risk: number }
export interface DashboardSummary { total: number; total_value: number; high_risk_count: number; high_risk_rate: number; by_status: StatusMetric[] }
export interface TrendPoint { period: string; proposals: number; value: number; high_risk: number }
export interface MunicipalityRank { municipio: string; uf: string; proposals: number; value: number; average_risk: number }
export interface Investigation { id: number; cliente: string; valor: number; status: string; risco_score: number; municipio: string; uf: string }
export interface StateSummary { uf: string; state: string; region: string; proposals: number; value: number; frauds: number; high_risk: number }

export interface DashboardDataContextValue {
  summary: DashboardSummary | null;
  trend: TrendPoint[];
  municipalities: MunicipalityRank[];
  investigations: Investigation[];
  states: StateSummary[];
  loading: boolean;
}

export const DashboardDataContext = createContext<DashboardDataContextValue | null>(null);
