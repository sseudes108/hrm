import type { VolumePropostasResponse } from '../types/volumePropostas';

const mockVolumeVigente: VolumePropostasResponse = {
  subtitle: 'Março 2025',
  total: 1735,
  media: 64,
  refLineH: 65,
  refLineV: '13',
  data: [
    { xAxis: '01', yAxis: 45 },
    { xAxis: '02', yAxis: 62 },
    { xAxis: '03', yAxis: 38 },
    { xAxis: '04', yAxis: 71 },
    { xAxis: '05', yAxis: 55 },
    { xAxis: '06', yAxis: 85 },
    { xAxis: '07', yAxis: 43 },
    { xAxis: '08', yAxis: 67 },
    { xAxis: '09', yAxis: 90 },
    { xAxis: '10', yAxis: 52 },
    { xAxis: '11', yAxis: 48 },
    { xAxis: '12', yAxis: 76 },
    { xAxis: '13', yAxis: 61 },
    { xAxis: '14', yAxis: 58 },
    { xAxis: '15', yAxis: 83 },
    { xAxis: '16', yAxis: 47 },
    { xAxis: '17', yAxis: 69 },
    { xAxis: '18', yAxis: 74 },
    { xAxis: '19', yAxis: 55 },
    { xAxis: '20', yAxis: 91 },
    { xAxis: '21', yAxis: 40 },
    { xAxis: '22', yAxis: 66 },
    { xAxis: '23', yAxis: 78 },
    { xAxis: '24', yAxis: 53 },
    { xAxis: '25', yAxis: 85 },
    { xAxis: '26', yAxis: 49 },
    { xAxis: '27', yAxis: 72 },
  ],
};

// simula latência de rede
export const fetchVolumeVigente = (): Promise<VolumePropostasResponse> =>
  new Promise(resolve => setTimeout(() => resolve(mockVolumeVigente), 600));

const mockVolumeConsolidado: VolumePropostasResponse = {
  subtitle: 'Jan26 - Mai/26',
  total: 17350,
  media: 648,
  refLineH: 384,
  refLineV: '13',
  data: [
    { xAxis: '01', yAxis: 455 },
    { xAxis: '02', yAxis: 626 },
    { xAxis: '03', yAxis: 389 },
    { xAxis: '04', yAxis: 718 },
    { xAxis: '05', yAxis: 551 }
  ],
};


// simula latência de rede
export const fetchVolumeConsolidado = (): Promise<VolumePropostasResponse> =>
  new Promise(resolve => setTimeout(() => resolve(mockVolumeConsolidado), 600));