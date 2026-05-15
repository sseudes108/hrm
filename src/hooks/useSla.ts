import { useEffect, useState } from 'react';
import { fetchSlaDiario } from '../mocks/slaDiario';
import type { SlaResponse } from '../types/sla';

interface UseSlaDiarioReturn {
  data: SlaResponse | null;
  isLoading: boolean;
  error: string | null;
}

export const useSlaDiario = (): UseSlaDiarioReturn => {
  const [data, setData] = useState<SlaResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    fetchSlaDiario()
      .then(setData)
      .catch(() => setError('Erro ao carregar SLA'))
      .finally(() => setIsLoading(false));
  }, []);

  return { data, isLoading, error };
};