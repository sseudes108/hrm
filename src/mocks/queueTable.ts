import type { QueueTableResponse } from '../types/queueTable';

export const mockQueueTable: QueueTableResponse = {
  periods: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
  rows: [
    {
      label: 'Suporte Técnico',
      periods: {
        'Jan': { qty: 340, qtyDelta: 0,   sla: 82, slaDelta: 0,    tma: 4.2, tmaDelta: 0 },
        'Fev': { qty: 380, qtyDelta: 40,  sla: 79, slaDelta: -3,   tma: 4.8, tmaDelta: 0.6 },
        'Mar': { qty: 310, qtyDelta: -70, sla: 85, slaDelta: 6,    tma: 3.9, tmaDelta: -0.9 },
        'Abr': { qty: 420, qtyDelta: 110, sla: 78, slaDelta: -7,   tma: 5.1, tmaDelta: 1.2 },
        'Mai': { qty: 390, qtyDelta: -30, sla: 88, slaDelta: 10,   tma: 4.0, tmaDelta: -1.1 },
        'Jun': { qty: 450, qtyDelta: 60,  sla: 91, slaDelta: 3,    tma: 3.7, tmaDelta: -0.3 },
        'Jul': { qty: 410, qtyDelta: -40, sla: 86, slaDelta: -5,   tma: 4.3, tmaDelta: 0.6 },
        'Ago': { qty: 470, qtyDelta: 60,  sla: 93, slaDelta: 7,    tma: 3.5, tmaDelta: -0.8 },
      },
    },
    {
      label: 'Financeiro',
      periods: {
        'Jan': { qty: 280, qtyDelta: 0,   sla: 71, slaDelta: 0,    tma: 6.1, tmaDelta: 0 },
        'Fev': { qty: 260, qtyDelta: -20, sla: 74, slaDelta: 3,    tma: 5.8, tmaDelta: -0.3 },
        'Mar': { qty: 290, qtyDelta: 30,  sla: 69, slaDelta: -5,   tma: 6.4, tmaDelta: 0.6 },
        'Abr': { qty: 310, qtyDelta: 20,  sla: 72, slaDelta: 3,    tma: 6.0, tmaDelta: -0.4 },
        'Mai': { qty: 275, qtyDelta: -35, sla: 76, slaDelta: 4,    tma: 5.5, tmaDelta: -0.5 },
        'Jun': { qty: 320, qtyDelta: 45,  sla: 80, slaDelta: 4,    tma: 5.2, tmaDelta: -0.3 },
        'Jul': { qty: 295, qtyDelta: -25, sla: 77, slaDelta: -3,   tma: 5.7, tmaDelta: 0.5 },
        'Ago': { qty: 340, qtyDelta: 45,  sla: 83, slaDelta: 6,    tma: 5.0, tmaDelta: -0.7 },
      },
    },
    {
      label: 'Comercial',
      periods: {
        'Jan': { qty: 210, qtyDelta: 0,   sla: 90, slaDelta: 0,    tma: 3.1, tmaDelta: 0 },
        'Fev': { qty: 195, qtyDelta: -15, sla: 88, slaDelta: -2,   tma: 3.3, tmaDelta: 0.2 },
        'Mar': { qty: 230, qtyDelta: 35,  sla: 92, slaDelta: 4,    tma: 2.9, tmaDelta: -0.4 },
        'Abr': { qty: 215, qtyDelta: -15, sla: 87, slaDelta: -5,   tma: 3.4, tmaDelta: 0.5 },
        'Mai': { qty: 245, qtyDelta: 30,  sla: 94, slaDelta: 7,    tma: 2.7, tmaDelta: -0.7 },
        'Jun': { qty: 260, qtyDelta: 15,  sla: 91, slaDelta: -3,   tma: 3.0, tmaDelta: 0.3 },
        'Jul': { qty: 240, qtyDelta: -20, sla: 89, slaDelta: -2,   tma: 3.2, tmaDelta: 0.2 },
        'Ago': { qty: 275, qtyDelta: 35,  sla: 95, slaDelta: 6,    tma: 2.6, tmaDelta: -0.6 },
      },
    },
    {
      label: 'Logística',
      periods: {
        'Jan': { qty: 195, qtyDelta: 0,   sla: 65, slaDelta: 0,    tma: 8.2, tmaDelta: 0 },
        'Fev': { qty: 210, qtyDelta: 15,  sla: 62, slaDelta: -3,   tma: 8.8, tmaDelta: 0.6 },
        'Mar': { qty: 185, qtyDelta: -25, sla: 68, slaDelta: 6,    tma: 7.9, tmaDelta: -0.9 },
        'Abr': { qty: 225, qtyDelta: 40,  sla: 60, slaDelta: -8,   tma: 9.1, tmaDelta: 1.2 },
        'Mai': { qty: 200, qtyDelta: -25, sla: 70, slaDelta: 10,   tma: 7.5, tmaDelta: -1.6 },
        'Jun': { qty: 235, qtyDelta: 35,  sla: 73, slaDelta: 3,    tma: 7.2, tmaDelta: -0.3 },
        'Jul': { qty: 215, qtyDelta: -20, sla: 67, slaDelta: -6,   tma: 8.0, tmaDelta: 0.8 },
        'Ago': { qty: 250, qtyDelta: 35,  sla: 75, slaDelta: 8,    tma: 7.0, tmaDelta: -1.0 },
      },
    },
    {
      label: 'RH',
      periods: {
        'Jan': { qty: 160, qtyDelta: 0,   sla: 95, slaDelta: 0,    tma: 2.1, tmaDelta: 0 },
        'Fev': { qty: 145, qtyDelta: -15, sla: 97, slaDelta: 2,    tma: 1.9, tmaDelta: -0.2 },
        'Mar': { qty: 170, qtyDelta: 25,  sla: 93, slaDelta: -4,   tma: 2.3, tmaDelta: 0.4 },
        'Abr': { qty: 155, qtyDelta: -15, sla: 96, slaDelta: 3,    tma: 2.0, tmaDelta: -0.3 },
        'Mai': { qty: 180, qtyDelta: 25,  sla: 94, slaDelta: -2,   tma: 2.2, tmaDelta: 0.2 },
        'Jun': { qty: 165, qtyDelta: -15, sla: 98, slaDelta: 4,    tma: 1.8, tmaDelta: -0.4 },
        'Jul': { qty: 175, qtyDelta: 10,  sla: 95, slaDelta: -3,   tma: 2.1, tmaDelta: 0.3 },
        'Ago': { qty: 190, qtyDelta: 15,  sla: 99, slaDelta: 4,    tma: 1.7, tmaDelta: -0.4 },
      },
    },
  ],
};

export const fetchQueueTable = (): Promise<QueueTableResponse> =>
  new Promise(resolve => setTimeout(() => resolve(mockQueueTable), 600));