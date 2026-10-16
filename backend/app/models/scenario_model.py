"""scenario_model.py: Documento MongoDB para Escenarios."""
from mongoengine import Document, StringField, IntField, DictField, ListField

class ScenarioModel(Document):
    name = StringField(required=True, unique=True)
    num_jobs = IntField(required=True)
    num_machines = IntField(required=True)
    num_operations = IntField(required=True)
    # Almacenamos los datos crudos en JSON para reconstruir el Scenario del Core cuando sea necesario
    raw_data = DictField(required=True) 
    meta = {"collection": "scenarios"}