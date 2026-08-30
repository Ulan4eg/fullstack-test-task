import { useState, useEffect } from 'react';
import { IAlertItem } from '../types/alert.types';
import { alertApi } from '../services/alert.api';
import { useToast } from '@/shared/hooks/useToast';
import {EToastType} from "@/shared/hooks/use-toast";

export function useAlerts() {
  const [ alerts, setAlerts ] = useState<IAlertItem[]>([]);
  const [ isLoading, setIsLoading ] = useState(true);
  const [ error, setError ] = useState<string | null>(null);
  const { showToast } = useToast();

  const loadAlerts = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await alertApi.listAlerts();
      setAlerts(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load alerts';
      setError(message);
      showToast(EToastType.ERROR, message);
    } finally {
      setIsLoading(false);
    }
  };

  const getAlertsByFile = async (fileId: string) => {
    try {
      return await alertApi.getAlertsByFile(fileId);
    } catch (err) {
      showToast(EToastType.ERROR, err instanceof Error ? err.message : 'Failed to load alerts for file');
      return [];
    }
  };

  useEffect(() => {
    loadAlerts().then();
  }, [loadAlerts]);

  return {
    alerts,
    isLoading,
    error,
    getAlertsByFile,
    refresh: loadAlerts,
  };
}