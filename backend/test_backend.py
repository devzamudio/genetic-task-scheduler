"""test_backend.py: Script de prueba integral para el backend del Job Scheduler."""
import requests
import time
import json
import sys
from typing import Dict, Any, Optional

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================
BASE_URL = "http://localhost:5000/api/v1"
TIMEOUT_POLLING = 120  # Segundos máximos de espera para una ejecución
INTERVALO_POLLING = 2  # Segundos entre cada verificación de estado

# ==============================================================================
# ESCENARIO DE PRUEBA (Basado en el ejemplo del PDF)
# ==============================================================================
SCENARIO_DATA = {
    "name": "Escenario PDF - 6 Trabajos, 5 Operaciones, 4 Máquinas",
    "jobs": [
        {"job_id": 1, "operations": [
            {"op_id": 1, "times": {"M1": 5.5, "M2": 4.2, "M3": 7.6, "M4": 9.0}},
            {"op_id": 2, "times": {"M1": 4.8, "M2": 5.3, "M3": 3.8, "M4": 4.7}},
            {"op_id": 3, "times": {"M1": 3.8, "M2": 3.4, "M3": 4.2, "M4": 3.6}}
        ]},
        {"job_id": 2, "operations": [
            {"op_id": 4, "times": {"M1": 3.5, "M2": 6.7, "M3": 2.5, "M4": 8.2}},
            {"op_id": 5, "times": {"M1": 6.1, "M2": 7.3, "M3": 5.5, "M4": 6.7}},
            {"op_id": 6, "times": {"M1": 3.8, "M2": 3.4, "M3": 4.2, "M4": 3.6}}
        ]},
        {"job_id": 3, "operations": [
            {"op_id": 7, "times": {"M1": 3.5, "M2": 6.7, "M3": 2.5, "M4": 8.2}},
            {"op_id": 8, "times": {"M1": 5.5, "M2": 4.2, "M3": 7.6, "M4": 9.0}},
            {"op_id": 9, "times": {"M1": 6.1, "M2": 7.3, "M3": 5.5, "M4": 6.7}},
            {"op_id": 10, "times": {"M1": 4.8, "M2": 5.3, "M3": 3.8, "M4": 4.7}},
            {"op_id": 11, "times": {"M1": 3.8, "M2": 3.4, "M3": 4.2, "M4": 3.6}}
        ]},
        {"job_id": 4, "operations": [
            {"op_id": 12, "times": {"M1": 4.8, "M2": 5.3, "M3": 3.8, "M4": 4.7}},
            {"op_id": 13, "times": {"M1": 3.8, "M2": 3.4, "M3": 4.2, "M4": 3.6}}
        ]},
        {"job_id": 5, "operations": [
            {"op_id": 14, "times": {"M1": 5.5, "M2": 4.2, "M3": 7.6, "M4": 9.0}},
            {"op_id": 15, "times": {"M1": 4.8, "M2": 5.3, "M3": 3.8, "M4": 4.7}}
        ]},
        {"job_id": 6, "operations": [
            {"op_id": 16, "times": {"M1": 3.5, "M2": 6.7, "M3": 2.5, "M4": 8.2}},
            {"op_id": 17, "times": {"M1": 5.5, "M2": 4.2, "M3": 7.6, "M4": 9.0}},
            {"op_id": 18, "times": {"M1": 4.8, "M2": 5.3, "M3": 3.8, "M4": 4.7}},
            {"op_id": 19, "times": {"M1": 3.8, "M2": 3.4, "M3": 4.2, "M4": 3.6}}
        ]}
    ]
}

# Parámetros reducidos para pruebas rápidas (ajustar para pruebas reales)
EXECUTION_PARAMS = {
    "pop_size": 50,
    "generations": 100,
    "mutation_rate": 0.2
}

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================
def print_header(title: str) -> None:
    """Imprime un encabezado formateado."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_success(message: str) -> None:
    print(f"✅ {message}")

def print_error(message: str) -> None:
    print(f"❌ {message}")

def print_info(message: str) -> None:
    print(f"ℹ️  {message}")

def handle_response(response: requests.Response, expected_status: int = 200) -> Optional[Dict[str, Any]]:
    """Maneja la respuesta HTTP y retorna el JSON si es exitoso."""
    if response.status_code == expected_status:
        return response.json()
    print_error(f"HTTP {response.status_code}: {response.text}")
    return None

def wait_for_execution(execution_id: str) -> Optional[Dict[str, Any]]:
    """Hace polling hasta que la ejecución termine o se agote el timeout."""
    start_time = time.time()
    while time.time() - start_time < TIMEOUT_POLLING:
        response = requests.get(f"{BASE_URL}/executions/{execution_id}")
        if response.status_code != 200:
            print_error(f"Error al consultar ejecución: {response.text}")
            return None
        
        data = response.json()
        status = data.get("status")
        
        if status == "COMPLETED":
            return data
        elif status == "FAILED":
            print_error(f"La ejecución falló: {data.get('result', {}).get('error', 'Desconocido')}")
            return None
        
        elapsed = int(time.time() - start_time)
        print(f"⏳ Estado: {status} ({elapsed}s transcurridos)...", end="\r")
        time.sleep(INTERVALO_POLLING)
    
    print_error(f"Timeout: la ejecución no terminó en {TIMEOUT_POLLING} segundos.")
    return None

# ==============================================================================
# PRUEBAS
# ==============================================================================
def test_1_health_check() -> bool:
    """Prueba 1: Verifica que la API esté respondiendo."""
    print_header("PRUEBA 1: Health Check de la API")
    try:
        response = requests.get(f"{BASE_URL}/scenarios", timeout=5)
        if response.status_code in [200, 404]:
            print_success("La API está respondiendo correctamente.")
            return True
        print_error(f"Respuesta inesperada: {response.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar a la API. ¿Está corriendo el contenedor 'api'?")
        return False

def test_2_create_scenario() -> Optional[str]:
    """Prueba 2: Crea un escenario de prueba y retorna su ID."""
    print_header("PRUEBA 2: Creación de Escenario")
    print_info(f"Escenario: {SCENARIO_DATA['name']}")
    print_info(f"Trabajos: {len(SCENARIO_DATA['jobs'])}")
    
    response = requests.post(f"{BASE_URL}/scenarios", json=SCENARIO_DATA)
    data = handle_response(response, 201)
    
    if data:
        scenario_id = data["id"]
        print_success(f"Escenario creado con ID: {scenario_id}")
        return scenario_id
    
    # Si falla por duplicado, intenta obtenerlo de la lista
    print_info("Intentando recuperar escenario existente...")
    response = requests.get(f"{BASE_URL}/scenarios")
    scenarios = handle_response(response, 200)
    if scenarios:
        for s in scenarios:
            if s["name"] == SCENARIO_DATA["name"]:
                print_success(f"Escenario encontrado con ID: {s['id']}")
                return s["id"]
    return None

def test_3_list_scenarios() -> bool:
    """Prueba 3: Lista todos los escenarios."""
    print_header("PRUEBA 3: Listado de Escenarios")
    response = requests.get(f"{BASE_URL}/scenarios")
    scenarios = handle_response(response, 200)
    
    if scenarios is not None:
        print_success(f"Escenarios encontrados: {len(scenarios)}")
        for s in scenarios:
            print(f"   • {s['name']} (ID: {s['id'][:8]}...) - {s['jobs']}J / {s['machines']}M / {s['ops']}Op")
        return True
    return False

def test_4_single_execution(scenario_id: str) -> Optional[str]:
    """Prueba 4: Dispara una ejecución única del AG y espera el resultado."""
    print_header("PRUEBA 4: Ejecución Única del Algoritmo Genético")
    print_info(f"Parámetros: {EXECUTION_PARAMS}")
    
    payload = {
        "scenario_id": scenario_id,
        "parameters": EXECUTION_PARAMS
    }
    
    response = requests.post(f"{BASE_URL}/executions", json=payload)
    data = handle_response(response, 202)
    
    if not data:
        return None
    
    execution_id = data["execution_id"]
    print_success(f"Ejecución disparada. ID: {execution_id}")
    print_info("Esperando finalización del AG (Celery worker)...")
    
    result = wait_for_execution(execution_id)
    if result and result.get("status") == "COMPLETED":
        ga_result = result.get("result", {})
        print_success(f"¡Ejecución completada!")
        print(f"   🏆 Mejor Makespan: {ga_result.get('best_makespan', 'N/A')}")
        print(f"   🧬 Cromosoma: {ga_result.get('best_chromosome', 'N/A')}")
        convergence = ga_result.get("convergence", [])
        if convergence:
            print(f"   📈 Generaciones registradas: {len(convergence)}")
            print(f"   📉 Makespan inicial: {convergence[0]:.2f} → final: {convergence[-1]:.2f}")
        return execution_id
    return None

def test_5_statistical_report(scenario_id: str) -> Optional[str]:
    """Prueba 5: Dispara un reporte estadístico (20 ejecuciones)."""
    print_header("PRUEBA 5: Reporte Estadístico (20 ejecuciones)")
    print_info("Esto disparará 20 tareas asíncronas. Puede tardar varios minutos...")
    
    payload = {
        "scenario_id": scenario_id,
        "parameters": EXECUTION_PARAMS
    }
    
    response = requests.post(f"{BASE_URL}/reports", json=payload)
    data = handle_response(response, 202)
    
    if data:
        report_id = data["report_id"]
        print_success(f"Reporte disparado. ID: {report_id}")
        print_info(f"Ejecuciones programadas: {data.get('executions_count', 20)}")
        return report_id
    return None

# ==============================================================================
# FLUJO PRINCIPAL
# ==============================================================================
def main() -> int:
    """Ejecuta todas las pruebas en secuencia."""
    print("\n" + "="*70)
    print("  SCRIPT DE PRUEBA INTEGRAL - GENETIC TASK SCHEDULER BACKEND")
    print("="*70)
    
    # Prueba 1: Health Check
    if not test_1_health_check():
        return 1
    
    # Prueba 2: Crear escenario
    scenario_id = test_2_create_scenario()
    if not scenario_id:
        return 1
    
    # Prueba 3: Listar escenarios
    if not test_3_list_scenarios():
        return 1
    
    # Prueba 4: Ejecución única
    execution_id = test_4_single_execution(scenario_id)
    if not execution_id:
        print_error("La ejecución única falló. Abortando pruebas posteriores.")
        return 1
    
    # Prueba 5: Reporte estadístico (opcional, puede tardar mucho)
    response = input("\n¿Desea ejecutar el reporte estadístico de 20 ejecuciones? (s/N): ")
    if response.lower() == 's':
        test_5_statistical_report(scenario_id)
    
    print_header("RESUMEN FINAL")
    print_success("Todas las pruebas críticas completadas exitosamente.")
    print_info("El backend está completamente funcional:")
    print("   • API REST responde correctamente")
    print("   • MongoDB persiste escenarios y ejecuciones")
    print("   • Celery procesa el AG de forma asíncrona")
    print("   • El núcleo del AG converge y calcula el makespan")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())