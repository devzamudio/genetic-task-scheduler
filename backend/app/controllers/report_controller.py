"""report_controller.py: Endpoints REST para Reportes Estadísticos."""
from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService

report_bp = Blueprint("reports", __name__)

@report_bp.route("", methods=["POST"])
def trigger_report():
    data = request.get_json()
    scenario_id = data.get("scenario_id")
    params = data.get("parameters", {"pop_size": 100, "generations": 200, "mutation_rate": 0.2})
    
    if not scenario_id:
        return jsonify({"error": "scenario_id is required"}), 400
        
    try:
        report = ReportService.trigger_statistical_report(scenario_id, params)
        return jsonify({"report_id": str(report.id), "executions_count": len(report.executions)}), 202
    except Exception as e:
        # Esto nos dirá exactamente qué falló si vuelve a ocurrir
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@report_bp.route("/<report_id>", methods=["GET"])
def get_report(report_id):
    try:
        status = ReportService.get_report_status(report_id)
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener reporte: {str(e)}"}), 500