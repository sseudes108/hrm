export interface SlaDataPoint {
  dia: string;
  sla: number;
}

export interface SlaResponse {
  data: SlaDataPoint[];
  total: number;   // média geral no período
  meta: number;    // linha horizontal
  subtitle: string;
  refLineV: string;
}