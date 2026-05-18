export interface PeriodData {
  qty: number;
  qtyDelta: number;
  sla: number;
  slaDelta: number;
  tma: number;
  tmaDelta: number;
}

export interface QueueRow {
  label: string;
  periods: Record<string, PeriodData>;
}

export interface QueueTableResponse {
  periods: string[];
  rows: QueueRow[];
}