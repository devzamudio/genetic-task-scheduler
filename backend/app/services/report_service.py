"""report_service.py: Lógica para el reporte estadístico (20 ejecuciones)."""
import numpy as np
from typing import Dict, Any, Optional
from app.models.scenario_model import ScenarioModel
from app.models.execution_model import ExecutionModel
from app.models.report_model import ReportModel
from app.services.execution_service import ExecutionService

class ReportService:
    @staticmethod
    def trigger_statistical_report(scenario_id: str, base_params: Dict[str, Any]) -> ReportModel:
        scenario = ScenarioModel.objects.get(id=scenario_id)
        execution_ids = []
        
        for i in range(20):
            params = base_params.copy()
            params["seed"] = 42 + i  # Semillas diferentes
            exec_model = ExecutionService.trigger_execution(scenario_id, params)
            execution_ids.append(exec_model.id)
            
        report = ReportModel(
            scenario=scenario,
            executions=execution_ids,
            status="RUNNING",
            metrics={},
            convergence_data={}
        ).save()
        return report

    @staticmethod
    def get_report_status(report_id: str) -> Dict[str, Any]:
        """Obtiene el estado del reporte y calcula estadísticas si las 20 ejecuciones finalizaron."""
        report = ReportModel.objects.get(id=report_id)
        
        # CORRECCIÓN: Extraer los IDs de las referencias antes de consultar
        execution_ids = [str(e.id) for e in report.executions]
        
        # Consultar todas las ejecuciones en una sola query
        executions = ExecutionModel.objects(id__in=execution_ids)
        
        completed_execs = [e for e in executions if e.status == "COMPLETED"]
        failed_execs = [e for e in executions if e.status == "FAILED"]
        
        total = len(report.executions)
        completed_count = len(completed_execs)
        
        if completed_count < total:
            return {
                "id": str(report.id),
                "status": "RUNNING",
                "progress": f"{completed_count}/{total} ejecuciones completadas",
                "metrics": None,
                "convergence_data": None
            }
            
        # Calcular estadísticas descriptivas
        makespans = [e.result["best_makespan"] for e in completed_execs]
        convergences = [e.result["convergence"] for e in completed_execs]
        
        # Asegurar que todas las convergencias tengan la misma longitud (tomar el mínimo)
        min_gens = min(len(c) for c in convergences)
        convergences_trimmed = [c[:min_gens] for c in convergences]
        
        # Calcular mejor, peor y promedio por generación
        best_per_gen = [min(c[i] for c in convergences_trimmed) for i in range(min_gens)]
        worst_per_gen = [max(c[i] for c in convergences_trimmed) for i in range(min_gens)]
        avg_per_gen = [sum(c[i] for c in convergences_trimmed) / completed_count for i in range(min_gens)]
        
        metrics = {
            "best_makespan": float(np.min(makespans)),
            "worst_makespan": float(np.max(makespans)),
            "average_makespan": float(np.mean(makespans)),
            "std_dev": float(np.std(makespans))
        }
        
        convergence_data = {
            "best": best_per_gen,
            "worst": worst_per_gen,
            "avg": avg_per_gen
        }
        
        # Actualizar el documento en MongoDB
        report.update(
            status="COMPLETED",
            metrics=metrics,
            convergence_data=convergence_data
        )
        
        return {
            "id": str(report.id),
            "status": "COMPLETED",
            "progress": f"{completed_count}/{total}",
            "metrics": metrics,
            "convergence_data": convergence_data
        }