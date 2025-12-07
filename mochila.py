"""
mochila.py

Implementación del problema de la Mochila 0/1.
"""

from typing import List
from dataclasses import dataclass


@dataclass
class SolucionMochila:
    seleccion: List[int]               # 1 si se tomó, 0 si no (1-based)
    beneficio: int                     # demo.py usa "beneficio"
    peso: int
    soluciones_factibles: int = 0      # demo.py usa "soluciones_factibles"

    # Compatibilidad con demo.py (usa solucion.mochila)
    @property
    def mochila(self):
        return self.seleccion


class ProblemaMochila:

    def __init__(self, pesos: List[int], beneficios: List[int], capacidad: int, n: int):
        # Convertimos a 1-based internamente
        self.pesos = [0] + pesos
        self.beneficios = [0] + beneficios
        self.capacidad = capacidad
        self.n = n

    # ----------------------------------------------------------
    # GREEDY
    # ----------------------------------------------------------
    def busqueda_greedy(self) -> SolucionMochila:
        objetos = list(range(1, self.n + 1))
        objetos.sort(key=lambda i: self.beneficios[i] / self.pesos[i], reverse=True)

        seleccion = [0] * (self.n + 1)
        peso_actual = 0
        beneficio_total = 0
        soluciones = 0

        for i in objetos:
            soluciones += 1
            if peso_actual + self.pesos[i] <= self.capacidad:
                seleccion[i] = 1
                peso_actual += self.pesos[i]
                beneficio_total += self.beneficios[i]

        return SolucionMochila(seleccion, beneficio_total, peso_actual, soluciones)

    # ----------------------------------------------------------
    # EXHAUSTIVA PURA
    # ----------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionMochila:
        seleccion_actual = [0] * (self.n + 1)
        mejor = SolucionMochila([0] * (self.n + 1), 0, 0, 0)

        def bt(i, peso, beneficio):
            if i > self.n:
                mejor.soluciones_factibles += 1
                if peso <= self.capacidad and beneficio > mejor.beneficio:
                    mejor.beneficio = beneficio
                    mejor.peso = peso
                    mejor.seleccion = seleccion_actual[:]
                return

            # No tomar
            seleccion_actual[i] = 0
            bt(i + 1, peso, beneficio)

            # Tomar si cabe
            if peso + self.pesos[i] <= self.capacidad:
                seleccion_actual[i] = 1
                bt(i + 1,
                   peso + self.pesos[i],
                   beneficio + self.beneficios[i])

        bt(1, 0, 0)
        return mejor

    # ----------------------------------------------------------
    # RAMIFICACIÓN Y ACOTAMIENTO
    # ----------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionMochila:
        seleccion_actual = [0] * (self.n + 1)
        mejor = SolucionMochila([0] * (self.n + 1), 0, 0, 0)

        objetos = list(range(1, self.n + 1))
        objetos.sort(key=lambda i: self.beneficios[i] / self.pesos[i], reverse=True)

        pesos_ord = [self.pesos[i] for i in objetos]
        valores_ord = [self.beneficios[i] for i in objetos]

        # Cota estilo knapsack fraccionario
        def cota(k, peso, beneficio):
            if peso > self.capacidad:
                return 0

            cap_rest = self.capacidad - peso
            total = beneficio

            for idx in range(k, len(objetos)):
                p = pesos_ord[idx]
                v = valores_ord[idx]
                if p <= cap_rest:
                    total += v
                    cap_rest -= p
                else:
                    total += v * (cap_rest / p)
                    break

            return total

        def bb(k, peso, beneficio):
            mejor.soluciones_factibles += 1

            # Si ya se asignaron todos
            if k == len(objetos):
                if beneficio > mejor.beneficio:
                    mejor.beneficio = beneficio
                    mejor.peso = peso
                    mejor.seleccion = seleccion_actual[:]
                return

            # Poda
            if cota(k, peso, beneficio) < mejor.beneficio:
                return

            obj = objetos[k]

            # Tomar
            if peso + self.pesos[obj] <= self.capacidad:
                seleccion_actual[obj] = 1
                bb(k + 1,
                   peso + self.pesos[obj],
                   beneficio + self.beneficios[obj])

            # No tomar
            seleccion_actual[obj] = 0
            bb(k + 1, peso, beneficio)

        bb(0, 0, 0)
        return mejor