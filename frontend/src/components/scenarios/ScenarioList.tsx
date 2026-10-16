import type { Scenario } from '../../types';

interface ScenarioListProps {
  scenarios: Scenario[];
  selectedScenarioId?: string;
  onSelectScenario?: (scenarioId: string) => void;
}

export function ScenarioList({ scenarios, selectedScenarioId, onSelectScenario }: ScenarioListProps) {
  if (scenarios.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Escenarios Disponibles</h2>
        <div className="text-center py-8">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No hay escenarios</h3>
          <p className="mt-1 text-sm text-gray-500">Cargue un archivo JSON para comenzar.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Escenarios Disponibles ({scenarios.length})</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {scenarios.map((scenario) => {
          const isSelected = selectedScenarioId === scenario.id;
          return (
            <div
              key={scenario.id}
              onClick={() => onSelectScenario?.(scenario.id)}
              className={`p-4 border rounded-lg cursor-pointer transition-all ${
                isSelected ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-500' : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-sm font-semibold text-gray-900 line-clamp-2">{scenario.name}</h3>
                {isSelected && (
                  <svg className="h-5 w-5 text-primary-600 flex-shrink-0 ml-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="space-y-2">
                <div className="flex items-center text-xs text-gray-600">
                  <span className="font-medium">{scenario.jobs}</span><span className="ml-1">trabajos</span>
                </div>
                <div className="flex items-center text-xs text-gray-600">
                  <span className="font-medium">{scenario.machines}</span><span className="ml-1">máquinas</span>
                </div>
                <div className="flex items-center text-xs text-gray-600">
                  <span className="font-medium">{scenario.ops}</span><span className="ml-1">operaciones</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}