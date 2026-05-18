// Atom Material Icons

import type { SlaResponse } from '../types/sla';

const mockResponse: SlaResponse = {
  subtitle: 'Março 2025',
  total: 74,
  meta: 80,
  refLineV: '13',
  data: [
    { dia: '01', sla: 82 },
    { dia: '02', sla: 75 },
    { dia: '03', sla: 68 },
    { dia: '04', sla: 91 },
    { dia: '05', sla: 70 },
    { dia: '06', sla: 85 },
    { dia: '07', sla: 60 },
    { dia: '08', sla: 78 },
    { dia: '09', sla: 95 },
    { dia: '10', sla: 65 },
    { dia: '11', sla: 72 },
    { dia: '12', sla: 88 },
    { dia: '13', sla: 76 },
    { dia: '14', sla: 81 },
    { dia: '15', sla: 69 },
    { dia: '16', sla: 90 },
    { dia: '17', sla: 74 },
    { dia: '18', sla: 83 },
    { dia: '19', sla: 58 },
    { dia: '20', sla: 92 },
    { dia: '21', sla: 77 },
    { dia: '22', sla: 86 },
    { dia: '23', sla: 71 },
    { dia: '24', sla: 63 },
    { dia: '25', sla: 89 },
    { dia: '26', sla: 79 },
    { dia: '27', sla: 84 },
  ],
};

export const fetchSlaDiario = (): Promise<SlaResponse> =>
  new Promise(resolve => setTimeout(() => resolve(mockResponse), 600));