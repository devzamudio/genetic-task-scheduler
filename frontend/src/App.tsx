import { useState, useEffect } from 'react';
import { Layout } from './components/layout/Layout';
import { ScenarioLoader } from './components/scenarios/ScenarioLoader';
import { ScenarioList } from './components/scenarios/ScenarioList';
import { ExecutionPanel } from './components/execution/ExecutionPanel';
import { ReportPanel } from './components/reports/ReportPanel';
import { GanttChart } from './components/visualization/GanttChart';
import { ConvergenceChart } from './components/visualization/ConvergenceChart';
import { useExecution } from './hooks/useExecution';
import { api } from './services/api';
import type { Scenario, GanttTask } from './types';

function App() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);
  const [currentExecutionId, setCurrentExecutionId] = useState<string | null>(null);
  
  // Hook para monitorear el estado de la ejecución única
  const { execution, loading: executionLoading } = useExecution(currentExecutionId);

  // Cargar escenarios al montar el componente
  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      const data = await api.listScenarios();
      setScenarios(data);
    } catch (err) {
      console.error('Error al cargar escenarios:', err);
    }
  };

  const handleExecutionStarted = (executionId: string) => {
    setCurrentExecutionId(executionId);
  };

  // USAR DATOS REALES DEL BACKEND
  const ganttTasks = execution?.result?.gantt_data || [];
  
  // Extraer máquinas únicas del resultado para el eje Y del Gantt
  const machines = Array.from(new Set(ganttTasks.map((t: GanttTask) => t.machine))).sort();

  return (
    <Layout>
      <div className="space-y-8">
        
        {/* 1. Carga de Escenarios */}
        <section>
          <h2 className="text-xl font-bold text-gray-800 mb-4">1. Carga de Datos</h2>
          <ScenarioLoader onScenarioCreated={loadScenarios} />
        </section>

        {/* 2. Lista de Escenarios Disponibles */}
        <section>
          <h2 className="text-xl font-bold text-gray-800 mb-4">2. Escenarios Disponibles</h2>
          <ScenarioList 
            scenarios={scenarios}
            selectedScenarioId={selectedScenarioId || undefined}
            onSelectScenario={setSelectedScenarioId}
          />
        </section>

        {/* 3. Panel de Ejecución Única */}
        <section>
          <h2 className="text-xl font-bold text-gray-800 mb-4">3. Ejecución del Algoritmo Genético</h2>
          <ExecutionPanel 
            scenarios={scenarios} 
            onExecutionStarted={handleExecutionStarted}
          />
        </section>

        {/* 4. Estado y Visualización de Ejecución Única */}
        {currentExecutionId && (
          <section className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Estado de la Ejecución
              </h2>
              {executionLoading && (
                <div className="flex items-center space-x-3">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
                  <span className="text-sm text-gray-600">
                    El Algoritmo Genético está optimizando el makespan...
                  </span>
                </div>
              )}
              {execution && !executionLoading && (
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Estado:</span>{' '}
                    <span className={`font-semibold ${
                      execution.status === 'COMPLETED' ? 'text-green-600' :
                      execution.status === 'FAILED' ? 'text-red-600' :
                      'text-yellow-600'
                    }`}>
                      {execution.status}
                    </span>
                  </p>
                  {execution.status === 'FAILED' && execution.result?.error && (
                    <p className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                      Error: {execution.result.error}
                    </p>
                  )}
                  {execution.status === 'COMPLETED' && execution.result && (
                    <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
                      <p className="text-sm font-medium text-green-900">
                        🏆 Mejor Makespan Alcanzado: {execution.result.best_makespan.toFixed(2)}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Visualizaciones solo si la ejecución fue exitosa y hay datos */}
            {execution?.status === 'COMPLETED' && execution.result && ganttTasks.length > 0 && (
              <div className="space-y-6">
                <GanttChart tasks={ganttTasks} machines={machines} />
                <ConvergenceChart convergence={execution.result.convergence} />
              </div>
            )}
          </section>
        )}

        {/* 5. Análisis Estadístico (Fase 5 - Requisito del PDF) */}
        <section className="border-t border-gray-200 pt-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            4. Análisis Estadístico (20 Ejecuciones)
          </h2>
          <p className="text-sm text-gray-600 mb-6">
            Ejecuta el algoritmo 20 veces con diferentes semillas para generar la estadística descriptiva 
            y la gráfica de convergencia comparativa (mejor, peor y promedio) solicitada en el reto.
          </p>
          <ReportPanel scenarios={scenarios} />
        </section>

      </div>
    </Layout>
  );
}

export default App;