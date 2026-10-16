"""test_ga.py: Pruebas unitarias para el núcleo del AG."""
import pytest
import numpy as np
from app.core.models import Scenario
from app.core.ga_core import (
    evaluate_makespan, 
    uniform_crossover, 
    load_balanced_mutation, 
    run_ga
)

@pytest.fixture
def dummy_scenario() -> Scenario:
    """
    Escenario de prueba: 2 trabajos, 2 máquinas, 4 operaciones totales.
    J1: O0, O1 (Nivel 0, Nivel 1)
    J2: O2, O3 (Nivel 0, Nivel 1)
    """
    op_to_job = np.array([0, 0, 1, 1], dtype=np.int32)
    proc_times = np.array([
        [2.0, 5.0], # O0 (J1)
        [3.0, 1.0], # O1 (J1)
        [4.0, 2.0], # O2 (J2)
        [1.0, 4.0]  # O3 (J2)
    ], dtype=np.float32)
    
    # Nivel 0: O0, O2. Nivel 1: O1, O3
    ops_by_level = [np.array([0, 2]), np.array([1, 3])]
    
    return Scenario(
        num_jobs=2, num_machines=2, num_operations=4,
        op_to_job=op_to_job, proc_times=proc_times, ops_by_level=ops_by_level
    )

def test_evaluate_makespan_precedence(dummy_scenario):
    """Verifica que el cálculo del makespan respete precedencias y máquinas."""
    # Cromosoma: O0->M0(2.0), O1->M1(1.0), O2->M0(4.0), O3->M1(4.0)
    # M0: O0(0-2), O2(2-6). 
    # M1: O1(2-3) [Espera a O0 en J1], O3(6-10) [Espera a O2 en J2 por precedencia, no solo a M1].
    # Makespan esperado: 10.0
    population = np.array([[0, 1, 0, 1]], dtype=np.int32)
    makespans = evaluate_makespan(population, dummy_scenario)
    assert makespans[0] == pytest.approx(10.0)

def test_uniform_crossover_shape_and_bounds():
    """Verifica que la cruza uniforme mantenga las dimensiones y límites."""
    parents = np.array([[0, 1, 0, 1], [1, 0, 1, 0]], dtype=np.int32)
    offspring = uniform_crossover(parents)
    assert offspring.shape == parents.shape
    assert np.all((offspring >= 0) & (offspring <= 1))

def test_load_balanced_mutation(dummy_scenario):
    """Verifica que la mutación mueva operaciones de la máquina sobrecargada."""
    # Población donde M0 está sobrecargada (O0:2.0, O1:3.0, O2:4.0 = 9.0 vs M1: 0.0)
    population = np.array([[0, 0, 0, 0]], dtype=np.int32) 
    mutated = load_balanced_mutation(population, dummy_scenario, mutation_rate=1.0)
    
    # Al menos una operación debería haberse movido a M1 para balancear
    assert np.any(mutated[0] == 1)

def test_run_ga_convergence_and_structure(dummy_scenario):
    """Verifica que el AG complete y retorne una estructura de datos válida."""
    params = {"pop_size": 20, "generations": 10, "mutation_rate": 0.2, "seed": 123}
    result = run_ga(dummy_scenario, params)
    
    assert "best_makespan" in result
    assert "best_chromosome" in result
    assert "convergence" in result
    assert len(result["convergence"]) == 10
    assert result["best_makespan"] > 0
    assert len(result["best_chromosome"]) == dummy_scenario.num_operations