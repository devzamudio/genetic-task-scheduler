"""ga_core.py: Motor del Algoritmo Genético implementado desde cero con NumPy."""
import numpy as np
import numpy.typing as npt
from typing import Dict, Any
from app.core.models import Scenario

def evaluate_makespan(population: npt.NDArray[np.int32], scenario: Scenario) -> npt.NDArray[np.float32]:
    """
    Evalúa el makespan (fitness) de cada individuo en la población.
    Respeta la precedencia de operaciones por trabajo (procesando por niveles) 
    y la capacidad de las máquinas.
    """
    pop_size = population.shape[0]
    makespans = np.zeros(pop_size, dtype=np.float32)

    for c in range(pop_size):
        chromosome = population[c]
        job_end_times = np.zeros(scenario.num_jobs, dtype=np.float32)
        machine_end_times = np.zeros(scenario.num_machines, dtype=np.float32)

        # Procesamos por niveles de secuencia para garantizar precedencia de trabajos
        for level_ops in scenario.ops_by_level:
            for op_idx in level_ops:
                job_idx = scenario.op_to_job[op_idx]
                machine_idx = chromosome[op_idx]
                proc_time = scenario.proc_times[op_idx, machine_idx]

                # El inicio es el máximo entre la disponibilidad del trabajo y de la máquina
                start_time = max(job_end_times[job_idx], machine_end_times[machine_idx])
                end_time = start_time + proc_time

                job_end_times[job_idx] = end_time
                machine_end_times[machine_idx] = end_time

        makespans[c] = np.max(machine_end_times)
        
    return makespans

def tournament_selection(population: npt.NDArray[np.int32], fitnesses: npt.NDArray[np.float32], k: int = 3) -> npt.NDArray[np.int32]:
    """Selección por torneo. Vectorizada para máxima eficiencia."""
    pop_size = population.shape[0]
    # Generamos índices aleatorios para los torneos (filas: pop_size, columnas: k)
    contestants = np.random.randint(0, pop_size, size=(pop_size, k))
    contestant_fitnesses = fitnesses[contestants]
    
    # CORRECCIÓN: np.arange(pop_size) selecciona la fila, np.argmin selecciona la columna ganadora
    winners_idx = contestants[np.arange(pop_size), np.argmin(contestant_fitnesses, axis=1)]
    return population[winners_idx]

def uniform_crossover(parents: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
    """Cruza uniforme vectorizada. (Filosofía: codificado de forma compacta y legible)."""
    pop_size, n_ops = parents.shape
    mask = np.random.rand(pop_size // 2, n_ops) < 0.5
    p1, p2 = parents[0::2], parents[1::2]
    return np.vstack((np.where(mask, p1, p2), np.where(~mask, p1, p2)))

def load_balanced_mutation(population: npt.NDArray[np.int32], scenario: Scenario, mutation_rate: float) -> npt.NDArray[np.int32]:
    """
    Mutación sesgada por balance de carga.
    Identifica la máquina cuello de botella (mayor carga) y reasigna sus operaciones 
    a la máquina con menor carga, promoviendo el equilibrio y minimizando el makespan.
    """
    pop_size, n_ops = population.shape
    mutated_pop = population.copy()
    
    # Calculamos la carga de trabajo (tiempo total) por máquina para cada individuo
    machine_loads = np.zeros((pop_size, scenario.num_machines), dtype=np.float32)
    for c in range(pop_size):
        for m in range(scenario.num_machines):
            ops_on_m = population[c] == m
            machine_loads[c, m] = np.sum(scenario.proc_times[ops_on_m, m])

    mutate_mask = np.random.rand(pop_size) < mutation_rate
    individuals_to_mutate = np.where(mutate_mask)[0]

    for c in individuals_to_mutate:
        bottleneck_machine = np.argmax(machine_loads[c])
        least_loaded_machine = np.argmin(machine_loads[c])
        
        if bottleneck_machine == least_loaded_machine:
            continue
            
        ops_on_bottleneck = np.where(population[c] == bottleneck_machine)[0]
        
        if len(ops_on_bottleneck) > 0:
            op_to_move = np.random.choice(ops_on_bottleneck)
            mutated_pop[c, op_to_move] = least_loaded_machine

    return mutated_pop

def run_ga(scenario: Scenario, params: Dict[str, Any]) -> Dict[str, Any]:
    """Bucle principal del Algoritmo Genético."""
    pop_size = params.get("pop_size", 100)
    generations = params.get("generations", 200)
    mutation_rate = params.get("mutation_rate", 0.2)
    seed = params.get("seed", 42)
    
    np.random.seed(seed)
    
    # Inicialización aleatoria de la población (Codificación Entera)
    population = np.random.randint(
        0, scenario.num_machines, 
        size=(pop_size, scenario.num_operations), 
        dtype=np.int32
    )
    
    best_makespan_history = []
    global_best_chromosome = None
    global_best_makespan = np.inf

    for _ in range(generations):
        fitnesses = evaluate_makespan(population, scenario)
        
        current_best_idx = np.argmin(fitnesses)
        if fitnesses[current_best_idx] < global_best_makespan:
            global_best_makespan = fitnesses[current_best_idx]
            global_best_chromosome = population[current_best_idx].copy()
        best_makespan_history.append(global_best_makespan)

        parents = tournament_selection(population, fitnesses)
        offspring = uniform_crossover(parents)
        population = load_balanced_mutation(offspring, scenario, mutation_rate)

    return {
        "best_makespan": float(global_best_makespan),
        "best_chromosome": global_best_chromosome.tolist(),
        "convergence": best_makespan_history
    }