import { useEffect, useState } from 'react';
import { fetchQueueTable } from '../mocks/queueTable';
import type { QueueTableResponse } from '../types/queueTable';

export const useQueueTable = () => {
  const [data, setData] = useState<QueueTableResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    fetchQueueTable()
      .then(setData)
      .catch(() => setError('Erro ao carregar tabela'))
      .finally(() => setIsLoading(false));
  }, []);

  return { data, isLoading, error };
};