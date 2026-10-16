export interface Operation {
  op_id: number;
  times: Record<string, number>;
}

export interface Job {
  job_id: number;
  operations: Operation[];
}

export interface Scenario {
  id: string;
  name: string;
  jobs: number;
  machines: number;
  ops: number;
}

export interface ScenarioData {
  name: string;
  jobs: Job[];
}

export interface ExecutionParams {
  pop_size: number;
  generations: number;
  mutation_rate: number;
}

export interface Execution {
  id: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  parameters: ExecutionParams;
  result?: ExecutionResult;
}

export interface GanttTask {
  job_id: number;
  op_id: number;
  machine: string;
  start_time: number;
  end_time: number;
  duration: number;
}

export interface ExecutionResult {
  best_makespan: number;
  best_chromosome: number[];
  gantt_data: GanttTask[]; // <-- AÑADIDO
  convergence: number[];
}
// ... (el resto de sus tipos permanecen igual)

export interface StatisticalReport {
  best_makespan: number;
  worst_makespan: number;
  average_makespan: number;
  std_dev: number;
}

export interface ConvergenceData {
  best: number[];
  worst: number[];
  avg: number[];
}

export interface ReportStatus {
  id: string;
  status: 'RUNNING' | 'COMPLETED' | 'FAILED';
  progress: string;
  metrics: StatisticalReport | null;
  convergence_data: ConvergenceData | null;
}