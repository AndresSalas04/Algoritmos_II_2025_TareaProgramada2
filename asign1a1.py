"""
asign1a1.py

Implementación del problema de Asignación 1 a 1.
"""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class SolucionAsigna1a1:
    """Solución al problema de asignación 1 a 1."""
    asignado: List[int]
    ganancia: int
    soluciones_factibles: int = 0


class ProblemaAsigna1a1:
    """Problema de Asignación de 1 a 1."""
    
    def __init__(self, matriz: List[List[int]], tamano: int):
        """
        Inicializa el problema de asignación 1 a 1.
        
        Args:
            matriz: Matriz de ganancias
            tamano: Número de elementos a asignar
        """
        self.matriz = matriz
        self.tamano = tamano
    
    def busqueda_greedy(self) -> SolucionAsigna1a1:
        """
        Búsqueda Greedy: Selecciona la mejor opción local en cada paso.
        
        Returns:
            Solución factible (no necesariamente óptima)
        """
        asignado = [False] * (self.tamano + 1)
        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0
        )
        
        for i in range(1, self.tamano + 1):
            mejor = 1
            while asignado[mejor] and mejor < self.tamano:
                mejor += 1
            
            for j in range(1, self.tamano + 1):
                if (self.matriz[i][j] > self.matriz[i][mejor] and 
                    not asignado[j]):
                    mejor = j
            
            solucion.asignado[i] = mejor
            solucion.ganancia += self.matriz[i][mejor]
            asignado[mejor] = True
        
        return solucion
    
    def busqueda_exhaustiva_pura(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva Pura: Explora todas las soluciones posibles.
        
        Returns:
            Solución óptima
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia = [0]  # Usar lista para modificar en función anidada
        
        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )
        
        def asignacion_exhaustiva(item: int):
            """Función recursiva para explorar todas las asignaciones."""
            for i in range(1, self.tamano + 1):
                if not asignado[i]:
                    asignado[i] = True
                    asignacion[item] = i
                    ganancia[0] += self.matriz[item][i]
                    
                    if item == self.tamano:
                        solucion.soluciones_factibles += 1
                        if ganancia[0] > solucion.ganancia:
                            solucion.ganancia = ganancia[0]
                            solucion.asignado = asignacion[:]
                    else:
                        asignacion_exhaustiva(item + 1)
                    
                    asignado[i] = False
                    ganancia[0] -= self.matriz[item][i]
        
        asignacion_exhaustiva(1)
        return solucion
        
    def busqueda_exhaustiva_ra(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva con Ramificación y Acotamiento.
        
        Ordena las ramas por mejor cota.
        Explora primero las ramas más prometedoras.
        
        Returns:
            La mejor solución encontrada.
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia_actual = [0]
        
        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )
        
        def calcular_cota_superior(nivel: int) -> int:
            """
            Calcula una cota superior optimista para la ganancia posible.
            """
            cota = ganancia_actual[0]
            
            for i in range(nivel, self.tamano + 1):
                mejor_disponible = 0
                for j in range(1, self.tamano + 1):
                    if not asignado[j]:
                        if self.matriz[i][j] > mejor_disponible:
                            mejor_disponible = self.matriz[i][j]
                cota += mejor_disponible
            
            return cota
        
        def asignacion_ra(item: int):
            """
            Función recursiva con ramificación y acotamiento.
            
            Ordena las ramas (opciones de asignación) por su cota superior
            de mayor a menor antes de explorarlas.
            """
            if item > self.tamano:
                # Solución completa encontrada
                solucion.soluciones_factibles += 1
                if ganancia_actual[0] > solucion.ganancia:
                    solucion.ganancia = ganancia_actual[0]
                    solucion.asignado = asignacion.copy()
                return
            
            # OPTIMIZACIÓN: Calcular cotas para todas las opciones disponibles
            opciones_con_cota = []
            
            for j in range(1, self.tamano + 1):
                if not asignado[j]:
                    # Hacer asignación tentativa para calcular cota
                    asignado[j] = True
                    asignacion[item] = j
                    ganancia_actual[0] += self.matriz[item][j]
                    
                    # Calcular cota con esta asignación
                    cota = calcular_cota_superior(item + 1)
                    
                    # Guardar opción con su cota
                    opciones_con_cota.append((j, cota))
                    
                    # Deshacer asignación temporal
                    asignado[j] = False
                    ganancia_actual[0] -= self.matriz[item][j]
            
            # ORDENAR: Explorar primero las ramas con mejor cota (mayor a menor)
            opciones_con_cota.sort(key=lambda x: x[1], reverse=True)
            
            # Explorar opciones en orden de mejor a peor cota
            for j, cota in opciones_con_cota:
                # PODA TEMPRANA: Si esta cota no puede mejorar, las siguientes tampoco
                if cota <= solucion.ganancia:
                    break  # Las siguientes serán peores, no vale la pena explorarlas
                
                # Hacer asignación
                asignado[j] = True
                asignacion[item] = j
                ganancia_actual[0] += self.matriz[item][j]
                
                # Recursión
                asignacion_ra(item + 1)
                
                # Backtrack
                asignado[j] = False
                ganancia_actual[0] -= self.matriz[item][j]
        
        asignacion_ra(1)
        return solucion