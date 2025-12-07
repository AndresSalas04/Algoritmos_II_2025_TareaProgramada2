"""
tiempo.py

Módulo para medir el tiempo de ejecución de algoritmos.
"""

import time
from typing import Dict

class MedidorTiempo:
    """
    Medidor de tiempo usando perf_counter_ns().
    """
    def __init__(self):
        """Inicializa el atributo que almacena el tiempo de inicio."""
        self.inicio_ns = 0

    def cargar_tiempo(self):
        """
        Guarda el tiempo actual como tiempo de inicio.
        """
        self.inicio_ns = time.perf_counter_ns()

    def intervalo_tiempo(self) -> Dict[str, float]:
        """
        Calcula el intervalo de tiempo desde cargar_tiempo() hasta ahora.

        Returns: un valor flotante que representa el tiempo en milisegundos
        """

        fin = time.perf_counter_ns()
        ns = fin - self.inicio_ns

        #Para que salga en ms
        ms = ns / 1_000_000 

        return {
            'ms': ms
        }

    def formato_tiempo(self, tiempo: Dict[str, float]) -> str:
        """
        Convierte el tiempo calculado en una cadena legible.

        Returns: str: Tiempo formateado con 3 decimales, en milisegundos.
        """
        return f"{tiempo['ms']:.3f} ms"
