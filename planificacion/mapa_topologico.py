# clases/mapa_topologico.py

import numpy as np
from typing import List, Tuple, Set
from clases.obstaculo import Obstaculo


class VisibilityGraph:
    """
    Construye un grafo de visibilidad para planificación de movimientos
    """

    def __init__(self, obstaculos: List[Obstaculo], limites: Tuple[int, int]):
        self.obstaculos = obstaculos
        self.limites = limites
        self.grafo = {}  # {nodo: [vecinos visibles]}
        self.construir_grafo()

    def obtener_vertices_obstaculos(self) -> List[Tuple[int, int]]:
        """
        Obtiene todos los vértices de los obstáculos cuadrados
        """
        vertices = []
        for obs in self.obstaculos:
            x, y = obs.pos
            tam = obs.tam / 2

            # 4 esquinas del obstáculo cuadrado
            vertices.extend([
                (int(x - tam), int(y - tam)),  # inferior izquierda
                (int(x + tam), int(y - tam)),  # inferior derecha
                (int(x + tam), int(y + tam)),  # superior derecha
                (int(x - tam), int(y + tam))  # superior izquierda
            ])

        return vertices

    def es_visible(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        """
        Verifica si dos puntos son visibles entre sí (sin obstáculos en medio)
        Usa el algoritmo de Bresenham para trazar la línea
        """
        x1, y1 = p1
        x2, y2 = p2

        # Algoritmo de Bresenham
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy
        x, y = x1, y1

        while True:
            # Verificar si el punto actual colisiona con algún obstáculo
            for obs in self.obstaculos:
                if obs.in_collission(x, y):
                    # Permitir si es el punto inicial o final (vértice del obstáculo)
                    if (x, y) not in [p1, p2]:
                        return False

            if x == x2 and y == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return True

    def construir_grafo(self):
        """
        Construye el grafo de visibilidad conectando vértices visibles
        """
        vertices = self.obtener_vertices_obstaculos()

        # Inicializar el grafo
        for v in vertices:
            self.grafo[v] = []

        # Conectar vértices que son visibles entre sí
        for i, v1 in enumerate(vertices):
            for v2 in vertices[i + 1:]:
                if self.es_visible(v1, v2):
                    self.grafo[v1].append(v2)
                    self.grafo[v2].append(v1)

    def agregar_punto_temporal(self, punto: Tuple[int, int]):
        """
        Agrega un punto temporal al grafo (posición de Pac-Man o fantasmas)
        """
        self.grafo[punto] = []

        for vertice in list(self.grafo.keys()):
            if vertice != punto and self.es_visible(punto, vertice):
                self.grafo[punto].append(vertice)
                self.grafo[vertice].append(punto)

    def eliminar_punto_temporal(self, punto: Tuple[int, int]):
        """
        Elimina un punto temporal del grafo
        """
        if punto in self.grafo:
            # Eliminar conexiones de otros nodos hacia este punto
            for vecinos in self.grafo.values():
                if punto in vecinos:
                    vecinos.remove(punto)

            # Eliminar el nodo
            del self.grafo[punto]