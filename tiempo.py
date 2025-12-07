"""
tiempo.py

Módulo para medir el tiempo de ejecución de algoritmos.
"""

import time
from typing import Dict

class MedidorTiempo:
    
    def __init__(self):
        self.inicio_ns = 0

    def cargar_tiempo(self):
        self.inicio_ns = time.perf_counter_ns()

    def intervalo_tiempo(self) -> Dict[str, float]:
        fin = time.perf_counter_ns()
        ns = fin - self.inicio_ns

        #Para que salga en ms
        ms = ns / 1_000_000 

        return {
            'ms': ms
        }

    def formato_tiempo(self, tiempo: Dict[str, float]) -> str:
        return f"{tiempo['ms']:.3f} ms"
