import { useState } from 'react';
import { api } from '../../services/api';
import { useReport } from '../../hooks/useReport';
import { StatsTable } from '../visualization/StatsTable';
import { MultiConvergenceChart } from '../visualization/MultiConvergenceChart';
import type { Scenario, ExecutionParams } from '../../types';

interface ReportPanelProps {
  scenarios: Scenario[];
}

export function ReportPanel({ scenarios }: ReportPanelProps) {
  const [selectedScenario, setSelectedScenario] = useState<string>('');
  const [params, setParams] = useState<ExecutionParams>({
    pop_size: 100,
    generations: 200,
    mutation_rate: 0.2,
  });
  const [reportId, setReportId] = useState<string | null>(null);
  const [isTriggering, setIsTriggering] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { report, loading } = useReport(reportId);

  const handleTriggerReport = async () => {
    if (!selectedScenario) {
      setError('Seleccione un escenario');
      return;
    }
    setIsTriggering(true);
    setError(null);
    try {
      const { report_id } = await api.triggerReport(selectedScenario, params);
      setReportId(report_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al iniciar el reporte');
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Reporte Estadístico (20 Ejecuciones)
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div className="md:col-span-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">Escenario</label>
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Seleccione...</option>
              {scenarios.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Población</label>
            <input
              type="number"
              value={params.pop_size}
              onChange={(e) => setParams({ ...params, pop_size: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Generaciones</label>
            <input
              type="number"
              value={params.generations}
              onChange={(e) => setParams({ ...params, generations: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <button
            onClick={handleTriggerReport}
            disabled={isTriggering || !selectedScenario || !!reportId}
            className="w-full px-4 py-2 bg-purple-600 text-white font-medium rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isTriggering ? 'Iniciando...' : reportId ? 'Reporte en curso' : 'Generar Reporte (20x)'}
          </button>
        </div>
        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      </div>

      {reportId && (
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          {loading || report?.status === 'RUNNING' ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
              <p className="text-gray-600">
                Procesando ejecuciones: <span className="font-semibold text-purple-600">{report?.progress}</span>
              </p>
              <p className="text-xs text-gray-500 mt-2">Esto puede tomar unos minutos dependiendo de los parámetros.</p>
            </div>
          ) : report?.status === 'COMPLETED' && report.metrics && report.convergence_data ? (
            <div className="space-y-8">
              <StatsTable stats={report.metrics} />
              <MultiConvergenceChart data={report.convergence_data} />
            </div>
          ) : (
            <p className="text-center text-red-600">Error al completar el reporte.</p>
          )}
        </div>
      )}
    </div>
  );
}