"""scenario_controller.py: Endpoints REST para Escenarios."""
from flask import Blueprint, request, jsonify
from app.services.scenario_service import ScenarioService
from app.models.scenario_model import ScenarioModel

scenario_bp = Blueprint("scenarios", __name__)

@scenario_bp.route("", methods=["POST"])
def create_scenario():
    data = request.get_json()
    if not data or "jobs" not in data:
        return jsonify({"error": "Invalid payload. 'jobs' array is required."}), 400
    try:
        model = ScenarioService.create_scenario(data)
        return jsonify({"id": str(model.id), "name": model.name, "status": "created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scenario_bp.route("", methods=["GET"])
def list_scenarios():
    scenarios = ScenarioModel.objects.all()
    result = [{"id": str(s.id), "name": s.name, "jobs": s.num_jobs, "machines": s.num_machines, "ops": s.num_operations} for s in scenarios]
    return jsonify(result), 200