"""
recursos.py

Problema de Distribución de Recursos:
matriz[i][j] = ganancia de asignar i recursos al ítem j.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SolucionRecursos:
    distribucion: List[int]   # recursos asignados por ítem (1-based)
    ganancia: int
    soluciones_factibles: int = 0


class DistribucionRecursos:

    def __init__(self, matriz: List[List[int]], recursos_totales: int, itemes: int):
        """
        matriz[i][j] = ganancia por asignar i recursos al ítem j
        recursos_totales = R
        itemes = cantidad de ítems (n)
        """
        self.matriz = matriz
        self.R = recursos_totales
        self.n = itemes

    # ---------------------------------------------------------------
    # GREEDY
    # ---------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionRecursos:
        """
        Greedy básico: para cada ítem elige el k con mayor ganancia directa
        sin considerar futuras restricciones.
        """
        distrib = [0] * (self.n + 1)
        gan_total = 0
        recursos_rest = self.R

        for j in range(1, self.n + 1):
            mejor_k = 0
            mejor_g = 0

            # probar con los recursos disponibles
            for k in range(0, recursos_rest + 1):
                if self.matriz[k][j] > mejor_g:
                    mejor_g = self.matriz[k][j]
                    mejor_k = k

            distrib[j] = mejor_k
            gan_total += mejor_g
            recursos_rest -= mejor_k

        return SolucionRecursos(distrib, gan_total)

    # ---------------------------------------------------------------
    # EXHAUSTIVA PURA
    # ---------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionRecursos:
        """
        Backtracking sobre la decisión:
        A cada ítem j se le asigna k recursos, con sum(k_j) <= R.
        """
        mejor = SolucionRecursos([0] * (self.n + 1), 0, 0)
        actual = [0] * (self.n + 1)

        def back(j, recursos_disp, gan_actual):
            # Caso final
            if j > self.n:
                mejor.soluciones_factibles += 1
                if gan_actual > mejor.ganancia:
                    mejor.ganancia = gan_actual
                    mejor.distribucion = actual[:]
                return

            # Probar asignar k al ítem j
            for k in range(0, recursos_disp + 1):
                actual[j] = k
                back(j + 1,
                     recursos_disp - k,
                     gan_actual + self.matriz[k][j])

        back(1, self.R, 0)
        return mejor
    
    # ---------------------------------------------------------------
    # RAMIFICACIÓN Y ACOTAMIENTO
    # ---------------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionRecursos:
        """
        Backtracking con poda usando cota superior:
        Máxima ganancia posible asignando lo mejor de cada ítem con
        los recursos disponibles.
        """

        mejor = SolucionRecursos([0] * (self.n + 1), 0, 0)
        actual = [0] * (self.n + 1)

        # Cota superior optimista:
        # Para los ítems que faltan, sumar la mejor ganancia posible
        def cota_superior(j, recursos_disp, gan_actual):
            gan_max = gan_actual

            # Para cada ítem desde j hasta n, asumir que se le asignan
            # los recursos que más ganancia le dan (hasta recursos_disp)
            for x in range(j, self.n + 1):
                mejor_g = 0
                # Se puede asignar desde 0 hasta recursos_disp
                for k in range(0, recursos_disp + 1):
                    if self.matriz[k][x] > mejor_g:
                        mejor_g = self.matriz[k][x]
                gan_max += mejor_g

            return gan_max

        def back(j, recursos_disp, gan_actual):
            # Caso final
            if j > self.n:
                mejor.soluciones_factibles += 1
                if gan_actual > mejor.ganancia:
                    mejor.ganancia = gan_actual
                    mejor.distribucion = actual[:]
                return

            # Evaluar cota superior
            if cota_superior(j, recursos_disp, gan_actual) <= mejor.ganancia:
                return  # PODA

            # Probar asignar k recursos al ítem j
            for k in range(0, recursos_disp + 1):
                actual[j] = k
                back(j + 1,
                     recursos_disp - k,
                     gan_actual + self.matriz[k][j])

        back(1, self.R, 0)
        return mejor