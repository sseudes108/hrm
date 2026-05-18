export interface DataPoint {
  xAxis: string;
  yAxis: number;
}

export interface VolumePropostasResponse {
  data: DataPoint[];
  total: number;
  media: number;
  subtitle: string;
  refLineH: number;
  refLineV: string;
}