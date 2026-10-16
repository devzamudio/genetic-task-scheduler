"""execution_service.py: Lógica de negocio para ejecuciones del AG."""
from typing import Dict, Any
from app.models.scenario_model import ScenarioModel
from app.models.execution_model import ExecutionModel
from app.tasks.ga_tasks import run_ga_task

class ExecutionService:
    @staticmethod
    def trigger_execution(scenario_id: str, params: Dict[str, Any]) -> ExecutionModel:
        """Crea el registro de ejecución y dispara la tarea asíncrona en Celery."""
        scenario = ScenarioModel.objects.get(id=scenario_id)
        
        execution = ExecutionModel(
            scenario=scenario,
            parameters=params,
            status="PENDING"
        ).save()
        
        # Disparar tarea Celery (se ejecuta en background)
        run_ga_task.delay(str(execution.id), str(scenario.id), params)
        
        return execution