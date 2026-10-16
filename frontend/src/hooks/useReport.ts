import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import type { ReportStatus } from '../types';

export function useReport(reportId: string | null) {
  const [report, setReport] = useState<ReportStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (!reportId) return;

    setLoading(true);

    const poll = async () => {
      try {
        const data = await api.getReport(reportId);
        setReport(data);

        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          setLoading(false);
          if (intervalRef.current) clearInterval(intervalRef.current);
        }
      } catch (err) {
        console.error('Error fetching report:', err);
        if (intervalRef.current) clearInterval(intervalRef.current);
      }
    };

    poll();
    intervalRef.current = window.setInterval(poll, 3000); // Poll cada 3 segundos

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [reportId]);

  return { report, loading };
}