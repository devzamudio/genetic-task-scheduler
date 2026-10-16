"""scenario_service.py: Lógica de negocio para gestión de escenarios."""
from typing import Dict, Any, List
import numpy as np
from app.models.scenario_model import ScenarioModel
from app.core.models import Scenario

class ScenarioService:
    @staticmethod
    def create_scenario(data: Dict[str, Any]) -> ScenarioModel:
        """Valida, guarda en Mongo y retorna el modelo de escenario."""
        jobs = data.get("jobs", [])
        machines_set = set()
        total_ops = 0
        
        # Validación básica y extracción de máquinas
        for job in jobs:
            for op in job["operations"]:
                machines_set.update(op["times"].keys())
                total_ops += 1
                
        machines = sorted(list(machines_set))
        
        model = ScenarioModel(
            name=data["name"],
            num_jobs=len(jobs),
            num_machines=len(machines),
            num_operations=total_ops,
            raw_data=data
        ).save()
        return model

    @staticmethod
    def build_core_scenario(model: ScenarioModel) -> Scenario:
        """
        Reconstruye el dataclass Scenario (Core) desde el modelo de Mongo.
        Calcula dinámicamente los niveles de precedencia (ops_by_level).
        """
        data = model.raw_data
        jobs = data["jobs"]
        machines = sorted(list(set(m for job in jobs for op in job["operations"] for m in op["times"].keys())))
        machine_to_idx = {m: i for i, m in enumerate(machines)}
        
        op_to_job = []
        proc_times = []
        ops_by_level = []
        
        # Mapeo de operaciones globales
        global_op_idx = 0
        job_ops_indices = [] # Para calcular niveles
        
        for j_idx, job in enumerate(jobs):
            current_job_ops = []
            for op in job["operations"]:
                op_to_job.append(j_idx)
                times = [op["times"].get(m, 0.0) for m in machines]
                proc_times.append(times)
                current_job_ops.append(global_op_idx)
                global_op_idx += 1
            job_ops_indices.append(current_job_ops)
            
        # Construcción de ops_by_level (Precedencia estricta del PDF)
        max_ops_in_job = max(len(ops) for ops in job_ops_indices)
        for level in range(max_ops_in_job):
            level_ops = []
            for job_ops in job_ops_indices:
                if level < len(job_ops):
                    level_ops.append(job_ops[level])
            if level_ops:
                ops_by_level.append(np.array(level_ops, dtype=np.int32))

        return Scenario(
            num_jobs=model.num_jobs,
            num_machines=model.num_machines,
            num_operations=model.num_operations,
            op_to_job=np.array(op_to_job, dtype=np.int32),
            proc_times=np.array(proc_times, dtype=np.float32),
            ops_by_level=ops_by_level
        )