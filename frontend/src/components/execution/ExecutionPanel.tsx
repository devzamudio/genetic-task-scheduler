import { useState } from 'react';
import { api } from '../../services/api';
import type { Scenario, ExecutionParams } from '../../types';

interface ExecutionPanelProps {
  scenarios: Scenario[];
  onExecutionStarted: (executionId: string) => void;
}

export function ExecutionPanel({ scenarios, onExecutionStarted }: ExecutionPanelProps) {
  const [selectedScenario, setSelectedScenario] = useState<string>('');
  const [params, setParams] = useState<ExecutionParams>({
    pop_size: 100,
    generations: 200,
    mutation_rate: 0.2,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExecute = async () => {
    if (!selectedScenario) {
      setError('Seleccione un escenario');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const { execution_id } = await api.triggerExecution(selectedScenario, params);
      onExecutionStarted(execution_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al iniciar la ejecución');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Ejecutar Algoritmo Genético
      </h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Escenario
          </label>
          <select
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">Seleccione un escenario...</option>
            {scenarios.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.jobs}J / {s.machines}M / {s.ops}Op)
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tamaño de Población
            </label>
            <input
              type="number"
              value={params.pop_size}
              onChange={(e) => setParams({ ...params, pop_size: parseInt(e.target.value) })}
              min="10"
              max="1000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Generaciones
            </label>
            <input
              type="number"
              value={params.generations}
              onChange={(e) => setParams({ ...params, generations: parseInt(e.target.value) })}
              min="10"
              max="2000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tasa de Mutación
            </label>
            <input
              type="number"
              value={params.mutation_rate}
              onChange={(e) => setParams({ ...params, mutation_rate: parseFloat(e.target.value) })}
              min="0"
              max="1"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <button
          onClick={handleExecute}
          disabled={loading || !selectedScenario}
          className="w-full px-4 py-2 bg-primary-600 text-white font-medium rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Iniciando...' : 'Ejecutar AG'}
        </button>
      </div>
    </div>
  );
}