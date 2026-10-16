"""models.py: Definición de estructuras de datos inmutables para el escenario."""
from dataclasses import dataclass
import numpy as np
import numpy.typing as npt

@dataclass(frozen=True)
class Scenario:
    """
    Representa un escenario del Job Scheduling Problem.
    Inmutable para garantizar la integridad de los datos durante la evaluación del AG.
    """
    num_jobs: int
    num_machines: int
    num_operations: int
    
    # Mapeo del índice global de la operación a su ID de trabajo (0 a num_jobs-1)
    op_to_job: npt.NDArray[np.int32]
    
    # Matriz de tiempos de procesamiento: shape (num_operations, num_machines)
    proc_times: npt.NDArray[np.float32]
    
    # Lista de arreglos. Cada arreglo contiene los índices globales de las operaciones 
    # que pertenecen al mismo nivel de secuencia (ej. todas las 1ras operaciones, luego las 2das).
    # Esto permite decodificar el makespan respetando la precedencia de trabajos en O(N).
    ops_by_level: list[npt.NDArray[np.int32]]