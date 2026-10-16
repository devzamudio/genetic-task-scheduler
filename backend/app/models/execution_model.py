"""execution_model.py: Documento MongoDB para Ejecuciones del AG."""
from mongoengine import Document, ObjectIdField, DictField, StringField, ReferenceField
from app.models.scenario_model import ScenarioModel

class ExecutionModel(Document):
    scenario = ReferenceField(ScenarioModel, required=True)
    parameters = DictField(required=True)
    status = StringField(choices=["PENDING", "RUNNING", "COMPLETED", "FAILED"], default="PENDING")
    result = DictField() # best_makespan, best_chromosome, convergence
    meta = {"collection": "executions"}