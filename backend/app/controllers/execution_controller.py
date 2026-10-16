"""execution_controller.py: Endpoints REST para Ejecuciones."""
from flask import Blueprint, request, jsonify
from app.services.execution_service import ExecutionService
from app.models.execution_model import ExecutionModel

execution_bp = Blueprint("executions", __name__)

@execution_bp.route("", methods=["POST"])
def trigger_execution():
    data = request.get_json()
    scenario_id = data.get("scenario_id")
    params = data.get("parameters", {"pop_size": 100, "generations": 200, "mutation_rate": 0.2})
    
    if not scenario_id:
        return jsonify({"error": "scenario_id is required"}), 400
        
    execution = ExecutionService.trigger_execution(scenario_id, params)
    return jsonify({"execution_id": str(execution.id), "status": execution.status}), 202

@execution_bp.route("/<execution_id>", methods=["GET"])
def get_execution(execution_id):
    try:
        execution = ExecutionModel.objects.get(id=execution_id)
        result = {
            "id": str(execution.id),
            "status": execution.status,
            "parameters": execution.parameters,
            "result": execution.result
        }
        return jsonify(result), 200
    except ExecutionModel.DoesNotExist:
        return jsonify({"error": "Execution not found"}), 404