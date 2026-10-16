import type { Scenario, ScenarioData, Execution, ExecutionParams, ReportStatus } from '../types';

const API_BASE_URL = 'http://localhost:5000/api/v1';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  // Escenarios
  async createScenario(data: ScenarioData): Promise<{ id: string; name: string }> {
    const response = await fetch(`${API_BASE_URL}/scenarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  async listScenarios(): Promise<Scenario[]> {
    const response = await fetch(`${API_BASE_URL}/scenarios`);
    return handleResponse(response);
  },

  // Ejecuciones
  async triggerExecution(scenarioId: string, params: ExecutionParams): Promise<{ execution_id: string }> {
    const response = await fetch(`${API_BASE_URL}/executions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: scenarioId, parameters: params }),
    });
    return handleResponse(response);
  },

  async getExecution(executionId: string): Promise<Execution> {
    const response = await fetch(`${API_BASE_URL}/executions/${executionId}`);
    return handleResponse(response);
  },

  async triggerReport(scenarioId: string, params: ExecutionParams): Promise<{ report_id: string }> {
    const response = await fetch(`${API_BASE_URL}/reports`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: scenarioId, parameters: params }),
    });
    return handleResponse(response);
  },

  async getReport(reportId: string): Promise<ReportStatus> {
    const response = await fetch(`${API_BASE_URL}/reports/${reportId}`);
    return handleResponse(response);
  },
};