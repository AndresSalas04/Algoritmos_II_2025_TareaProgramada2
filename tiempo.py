"""
tiempo.py

Módulo para medir el tiempo de ejecución de algoritmos.
"""

import time
from typing import Dict


class MedidorTiempo:
    """Clase para medir intervalos de tiempo de ejecución."""
    
    def __init__(self):
        self.tiempo_inicial: float = 0.0
        self.tiempo_final: float = 0.0
    
    def cargar_tiempo(self) -> None:
        """Guarda el tiempo actual como tiempo inicial."""
        self.tiempo_inicial = time.perf_counter()
    
    def intervalo_tiempo(self) -> Dict[str, int]:
        """
        Calcula el intervalo de tiempo transcurrido.
        
        Returns:
            Diccionario con horas, minutos, segundos y centésimas
        """
        self.tiempo_final = time.perf_counter()
        intervalo = self.tiempo_final - self.tiempo_inicial
        
        horas = int(intervalo // 3600)
        minutos = int((intervalo % 3600) // 60)
        segundos = int(intervalo % 60)
        centesimas = int((intervalo % 1) * 100)
        
        return {
            'horas': horas,
            'minutos': minutos,
            'segundos': segundos,
            'centesimas': centesimas
        }
    
    def formato_tiempo(self, tiempo: Dict[str, int]) -> str:
        """
        Formatea el tiempo en una cadena legible.
        
        Args:
            tiempo: Diccionario con componentes del tiempo
            
        Returns:
            String formateado como "HH:MM:SS,CC"
        """
        return f"{tiempo['horas']:02d}:{tiempo['minutos']:02d}:{tiempo['segundos']:02d},{tiempo['centesimas']:02d}"
