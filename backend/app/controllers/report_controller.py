"""report_controller.py: Endpoints REST para Reportes Estadísticos."""
from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService
from app.models.report_model import ReportModel

report_bp = Blueprint("reports", __name__)

@report_bp.route("", methods=["POST"])
def trigger_report():
    data = request.get_json()
    scenario_id = data.get("scenario_id")
    params = data.get("parameters", {"pop_size": 100, "generations": 200, "mutation_rate": 0.2})
    
    if not scenario_id:
        return jsonify({"error": "scenario_id is required"}), 400
        
    report = ReportService.trigger_statistical_report(scenario_id, params)
    return jsonify({"report_id": str(report.id), "executions_count": len(report.executions)}), 202