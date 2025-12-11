"""
Algoritmos de búsqueda sobre el grafo topológico
"""
from typing import List, Tuple, Optional, Dict
import numpy as np


class BusquedaEnGrafo:
    """
    Algoritmos de búsqueda sobre el grafo topológico
    """

    @staticmethod
    def distancia_euclidiana(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Calcula la distancia euclidiana entre dos puntos"""
        return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    @staticmethod
    def reconstruir_camino(padres: Dict, inicio: Tuple, objetivo: Tuple) -> List[Tuple[int, int]]:
        """Reconstruye el camino desde inicio hasta objetivo"""
        camino = []
        actual = objetivo

        while actual != inicio:
            camino.append(actual)
            if actual not in padres:
                return None  # No hay camino
            actual = padres[actual]

        camino.append(inicio)
        camino.reverse()
        return camino

    @staticmethod
    def a_estrella_grafo(grafo: Dict, inicio: Tuple[int, int], objetivo: Tuple[int, int]) -> Optional[
        List[Tuple[int, int]]]:
        """
        A* sobre el grafo de visibilidad
        """
        if inicio not in grafo or objetivo not in grafo:
            return None

        if inicio == objetivo:
            return [inicio]

        abiertos = [inicio]
        cerrados = set()

        g_score = {inicio: 0}
        f_score = {inicio: BusquedaEnGrafo.distancia_euclidiana(inicio, objetivo)}
        padres = {}

        while abiertos:
            # Nodo con menor f_score
            actual = min(abiertos, key=lambda n: f_score.get(n, float('inf')))

            if actual == objetivo:
                return BusquedaEnGrafo.reconstruir_camino(padres, inicio, objetivo)

            abiertos.remove(actual)
            cerrados.add(actual)

            for vecino in grafo[actual]:
                if vecino in cerrados:
                    continue

                g_tentativo = g_score[actual] + BusquedaEnGrafo.distancia_euclidiana(actual, vecino)

                if vecino not in abiertos:
                    abiertos.append(vecino)
                elif g_tentativo >= g_score.get(vecino, float('inf')):
                    continue

                padres[vecino] = actual
                g_score[vecino] = g_tentativo
                f_score[vecino] = g_tentativo + BusquedaEnGrafo.distancia_euclidiana(vecino, objetivo)

        return None

    @staticmethod
    def bpa_grafo(grafo: Dict, inicio: Tuple[int, int], objetivo: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Búsqueda Primero en Anchura sobre el grafo
        """
        if inicio not in grafo or objetivo not in grafo:
            return None

        if inicio == objetivo:
            return [inicio]

        visitados = set()
        cola = [(inicio, [inicio])]

        while cola:
            actual, camino = cola.pop(0)

            if actual == objetivo:
                return camino

            if actual in visitados:
                continue

            visitados.add(actual)

            for vecino in grafo[actual]:
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))

        return None

    @staticmethod
    def greedy_grafo(grafo: Dict, inicio: Tuple[int, int], objetivo: Tuple[int, int]) -> Optional[
        List[Tuple[int, int]]]:
        """
        Búsqueda Greedy sobre el grafo
        """
        if inicio not in grafo or objetivo not in grafo:
            return None

        if inicio == objetivo:
            return [inicio]

        visitados = set()
        abiertos = [(inicio, [inicio])]

        while abiertos:
            # Ordenar por heurística (distancia al objetivo)
            abiertos.sort(key=lambda x: BusquedaEnGrafo.distancia_euclidiana(x[0], objetivo))
            actual, camino = abiertos.pop(0)

            if actual == objetivo:
                return camino

            if actual in visitados:
                continue

            visitados.add(actual)

            for vecino in grafo[actual]:
                if vecino not in visitados:
                    abiertos.append((vecino, camino + [vecino]))

        return None