"""report_model.py: Documento MongoDB para Reportes Estadísticos."""
from mongoengine import Document, ReferenceField, ListField, DictField
from app.models.scenario_model import ScenarioModel
from app.models.execution_model import ExecutionModel

class ReportModel(Document):
    scenario = ReferenceField(ScenarioModel, required=True)
    executions = ListField(ReferenceField(ExecutionModel), required=True)
    metrics = DictField() # best, worst, avg, std_dev
    convergence_data = DictField() # Historial para gráficas
    meta = {"collection": "reports"}