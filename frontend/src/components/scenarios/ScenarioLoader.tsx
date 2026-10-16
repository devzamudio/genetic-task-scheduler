import { useState } from 'react';
import { api } from '../../services/api';
import type { ScenarioData } from '../../types';

interface ScenarioLoaderProps {
  onScenarioCreated: () => void;
}

export function ScenarioLoader({ onScenarioCreated }: ScenarioLoaderProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const text = await file.text();
      const data: ScenarioData = JSON.parse(text);
      
      await api.createScenario(data);
      setSuccess(`Escenario "${data.name}" cargado exitosamente`);
      onScenarioCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al cargar el escenario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Cargar Escenario
      </h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Archivo JSON del escenario
          </label>
          <input
            type="file"
            accept=".json"
            onChange={handleFileUpload}
            disabled={loading}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 disabled:opacity-50"
          />
        </div>
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
        {success && (
          <div className="p-3 bg-green-50 border border-green-200 rounded-md">
            <p className="text-sm text-green-800">{success}</p>
          </div>
        )}
      </div>
    </div>
  );
}