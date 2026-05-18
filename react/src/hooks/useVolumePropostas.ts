import { useEffect, useState } from 'react';
import { fetchVolumeConsolidado, fetchVolumeVigente } from '../mocks/volumePropostas';
import type { VolumePropostasResponse } from '../types/volumePropostas';

interface UseVolumePropostasReturn {
  data: VolumePropostasResponse | null;
  isLoading: boolean;
  error: string | null;
}

export const useVolumeVigente = (): UseVolumePropostasReturn => {
  const [data, setData] = useState<VolumePropostasResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    fetchVolumeVigente()
      .then(setData)
      .catch(() => setError('Erro ao carregar dados'))
      .finally(() => setIsLoading(false));
  }, []);

  return { data, isLoading, error };
};

export const useVolumeConsolidado = (): UseVolumePropostasReturn => {
  const [data, setData] = useState<VolumePropostasResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    fetchVolumeConsolidado()
      .then(setData)
      .catch(() => setError('Erro ao carregar dados'))
      .finally(() => setIsLoading(false));
  }, []);

  return { data, isLoading, error };
};