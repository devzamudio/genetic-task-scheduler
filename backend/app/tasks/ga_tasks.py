"""ga_tasks.py: Tareas Celery para ejecutar el AG en background."""
import numpy as np
from mongoengine import connect, disconnect
from mongoengine.connection import get_db
from app.config import Config
from app.extensions import celery_app
from app.models.scenario_model import ScenarioModel
from app.models.execution_model import ExecutionModel
from app.services.scenario_service import ScenarioService
from app.core.ga_core import run_ga

def ensure_mongo_connection():
    """Garantiza que exista una conexión válida a MongoDB en el proceso actual."""
    try:
        get_db()
    except Exception:
        try:
            disconnect()
        except Exception:
            pass
        connect(host=Config.MONGO_URI)

def convert_numpy_to_python(obj):
    """
    Convierte recursivamente tipos de NumPy a tipos nativos de Python
    para que sean serializables por MongoDB/BSON.
    """
    if isinstance(obj, dict):
        return {k: convert_numpy_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_python(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return [convert_numpy_to_python(item) for item in obj.tolist()]
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    else:
        return obj

@celery_app.task(bind=True, name="app.tasks.run_ga_task")
def run_ga_task(self, execution_id: str, scenario_id: str, params: dict):
    """Ejecuta el Algoritmo Genético y actualiza el estado en MongoDB."""
    ensure_mongo_connection()
    
    try:
        execution = ExecutionModel.objects.get(id=execution_id)
        execution.update(status="RUNNING")
        
        scenario_model = ScenarioModel.objects.get(id=scenario_id)
        core_scenario = ScenarioService.build_core_scenario(scenario_model)
        
        result = run_ga(core_scenario, params)
        
        # CLAVE: Convertir tipos de NumPy a Python nativos antes de guardar
        result_python = convert_numpy_to_python(result)
        
        execution.update(status="COMPLETED", result=result_python)
        return result_python
        
    except Exception as e:
        ExecutionModel.objects(id=execution_id).update_one(status="FAILED", result={"error": str(e)})
        raise e