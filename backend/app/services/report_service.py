"""report_service.py: Lógica para el reporte estadístico (20 ejecuciones)."""
import numpy as np
from typing import Dict, Any
from app.models.scenario_model import ScenarioModel
from app.models.execution_model import ExecutionModel
from app.models.report_model import ReportModel
from app.services.execution_service import ExecutionService

class ReportService:
    @staticmethod
    def trigger_statistical_report(scenario_id: str, base_params: Dict[str, Any]) -> ReportModel:
        """
        Dispara 20 ejecuciones con diferentes semillas.
        Nota: En un MVP estricto, agregamos las ejecuciones al reporte. 
        El cálculo de métricas se haría idealmente en una tarea Celery final, 
        pero para simplificar el flujo síncrono de creación, preparamos la estructura.
        """
        scenario = ScenarioModel.objects.get(id=scenario_id)
        execution_ids = []
        
        for i in range(20):
            params = base_params.copy()
            params["seed"] = i * 42 # Diferentes semillas
            exec_model = ExecutionService.trigger_execution(scenario_id, params)
            execution_ids.append(exec_model.id)
            
        report = ReportModel(
            scenario=scenario,
            executions=execution_ids,
            metrics={},
            convergence_data={}
        ).save()
        
        # Disparar tarea para calcular métricas cuando todas las ejecuciones terminen
        # (En un sistema real, Celery usaría un 'chord' o 'callback', pero mantenemos el MVP simple)
        return report