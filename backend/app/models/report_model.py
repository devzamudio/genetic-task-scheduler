"""report_model.py: Documento MongoDB para Reportes Estadísticos."""
from mongoengine import Document, ReferenceField, ListField, DictField, StringField
from app.models.scenario_model import ScenarioModel
from app.models.execution_model import ExecutionModel

class ReportModel(Document):
    scenario = ReferenceField(ScenarioModel, required=True)
    executions = ListField(ReferenceField(ExecutionModel), required=True)
    # CAMPO AÑADIDO: Para rastrear si las 20 ejecuciones ya terminaron
    status = StringField(choices=["RUNNING", "COMPLETED", "FAILED"], default="RUNNING")
    metrics = DictField() 
    convergence_data = DictField() 
    meta = {"collection": "reports"}