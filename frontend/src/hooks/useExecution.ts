import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import type { Execution } from '../types';

export function useExecution(executionId: string | null) {
  const [execution, setExecution] = useState<Execution | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (!executionId) return;

    setLoading(true);
    setError(null);

    const poll = async () => {
      try {
        const data = await api.getExecution(executionId);
        setExecution(data);

        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          setLoading(false);
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error fetching execution');
        setLoading(false);
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      }
    };

    poll();
    intervalRef.current = window.setInterval(poll, 2000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [executionId]);

  return { execution, loading, error };
}