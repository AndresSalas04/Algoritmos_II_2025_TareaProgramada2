"""
vendedor.py

Implementación del problema del Vendedor Viajero (TSP).
"""

from typing import List
from dataclasses import dataclass


@dataclass
class SolucionVendedor:
    """Representa una solución del TSP."""
    camino: List[int]
    costo: int
    soluciones_factibles: int = 0


class ProblemaVendedor:
    """Problema del Vendedor Viajero (TSP)."""

    def __init__(self, matriz: List[List[int]], tamano: int):
        self.matriz = matriz
        self.tamano = tamano

    # ----------------------------------------------------------------------
    #  GREEDY: Vecino más cercano
    # ----------------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionVendedor:
        visitado = [False] * (self.tamano + 1)
        camino = [0] * (self.tamano + 1)
        costo_total = 0

        actual = 1
        camino[1] = 1
        visitado[1] = True

        for pos in range(2, self.tamano + 1):
            mejor = -1
            costo_mejor = float("inf")

            for ciudad in range(1, self.tamano + 1):
                if not visitado[ciudad]:
                    costo = self.matriz[actual][ciudad]
                    if costo < costo_mejor:
                        costo_mejor = costo
                        mejor = ciudad

            camino[pos] = mejor
            visitado[mejor] = True
            costo_total += self.matriz[actual][mejor]
            actual = mejor

        # regresa a la ciudad inicial
        costo_total += self.matriz[actual][1]

        return SolucionVendedor(camino=camino, costo=costo_total)

    # ----------------------------------------------------------------------
    #  EXHAUSTIVA PURA
    # ----------------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionVendedor:
        visitado = [False] * (self.tamano + 1)
        camino_actual = [0] * (self.tamano + 1)
        costo_actual = [0]

        mejor_sol = SolucionVendedor(
            camino=[0] * (self.tamano + 1),
            costo=float("inf"),
            soluciones_factibles=0
        )

        camino_actual[1] = 1
        visitado[1] = True

        def tsp(pos: int):
            if pos > self.tamano:
                mejor_sol.soluciones_factibles += 1
                costo_final = costo_actual[0] + self.matriz[camino_actual[self.tamano]][1]

                if costo_final < mejor_sol.costo:
                    mejor_sol.costo = costo_final
                    mejor_sol.camino = camino_actual[:]

                return

            for ciudad in range(2, self.tamano + 1):
                if not visitado[ciudad]:
                    visitado[ciudad] = True
                    camino_actual[pos] = ciudad

                    costo_actual[0] += self.matriz[camino_actual[pos - 1]][ciudad]
                    tsp(pos + 1)

                    costo_actual[0] -= self.matriz[camino_actual[pos - 1]][ciudad]
                    visitado[ciudad] = False

        tsp(2)
        return mejor_sol

    # ----------------------------------------------------------------------
    #  RAMIFICACIÓN Y ACOTAMIENTO
    # ----------------------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionVendedor:
        visitado = [False] * (self.tamano + 1)
        camino_actual = [0] * (self.tamano + 1)
        costo_actual = [0]

        mejor_sol = SolucionVendedor(
            camino=[0] * (self.tamano + 1),
            costo=float("inf"),
            soluciones_factibles=0
        )

        camino_actual[1] = 1
        visitado[1] = True

        # Cota inferior optimista
        def calcular_cota_inferior(nivel: int) -> int:
            cota = costo_actual[0]

            for ciudad in range(1, self.tamano + 1):
                if not visitado[ciudad] or ciudad == camino_actual[nivel - 1]:
                    minimo = min(
                        self.matriz[ciudad][j]
                        for j in range(1, self.tamano + 1)
                        if j != ciudad
                    )
                    cota += minimo

            return cota

        def tsp_ra(pos: int):
            if pos > self.tamano:
                mejor_sol.soluciones_factibles += 1
                costo_final = costo_actual[0] + self.matriz[camino_actual[self.tamano]][1]

                if costo_final < mejor_sol.costo:
                    mejor_sol.costo = costo_final
                    mejor_sol.camino = camino_actual[:]
                return

            opciones = []

            for ciudad in range(2, self.tamano + 1):
                if not visitado[ciudad]:
                    visitado[ciudad] = True
                    camino_actual[pos] = ciudad
                    costo_actual[0] += self.matriz[camino_actual[pos - 1]][ciudad]

                    cota = calcular_cota_inferior(pos)
                    opciones.append((ciudad, cota))

                    costo_actual[0] -= self.matriz[camino_actual[pos - 1]][ciudad]
                    visitado[ciudad] = False

            opciones.sort(key=lambda x: x[1])

            for ciudad, cota in opciones:
                if cota >= mejor_sol.costo:
                    break

                visitado[ciudad] = True
                camino_actual[pos] = ciudad
                costo_actual[0] += self.matriz[camino_actual[pos - 1]][ciudad]

                tsp_ra(pos + 1)

                costo_actual[0] -= self.matriz[camino_actual[pos - 1]][ciudad]
                visitado[ciudad] = False

        tsp_ra(2)
        return mejor_sol