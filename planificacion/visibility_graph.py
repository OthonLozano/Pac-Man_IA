"""
Construye un grafo de visibilidad para planificación de movimientos
"""
import numpy as np
from typing import List, Tuple, Set, Dict
from clases.obstaculo import Obstaculo


class VisibilityGraph:
    """
    Construye un grafo de visibilidad para planificación de movimientos
    """

    def __init__(self, obstaculos: List[Obstaculo], limites: Tuple[int, int]):
        self.obstaculos = obstaculos
        self.limites = limites
        self.grafo: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
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

    def punto_en_segmento(self, p: Tuple[int, int], q: Tuple[int, int], r: Tuple[int, int]) -> bool:
        """
        Verifica si el punto q está en el segmento pr
        """
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    def orientacion(self, p: Tuple[int, int], q: Tuple[int, int], r: Tuple[int, int]) -> int:
        """
        Encuentra la orientación de la terna ordenada (p, q, r)
        Retorna:
        0 --> p, q y r son colineales
        1 --> Sentido horario
        2 --> Sentido antihorario
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def segmentos_se_intersectan(self, p1: Tuple[int, int], q1: Tuple[int, int],
                                 p2: Tuple[int, int], q2: Tuple[int, int]) -> bool:
        """
        Verifica si el segmento p1q1 y p2q2 se intersectan
        """
        o1 = self.orientacion(p1, q1, p2)
        o2 = self.orientacion(p1, q1, q2)
        o3 = self.orientacion(p2, q2, p1)
        o4 = self.orientacion(p2, q2, q1)

        # Caso general
        if o1 != o2 and o3 != o4:
            return True

        # Casos especiales (colineales)
        if o1 == 0 and self.punto_en_segmento(p1, p2, q1):
            return True
        if o2 == 0 and self.punto_en_segmento(p1, q2, q1):
            return True
        if o3 == 0 and self.punto_en_segmento(p2, p1, q2):
            return True
        if o4 == 0 and self.punto_en_segmento(p2, q1, q2):
            return True

        return False

    def linea_cruza_obstaculo(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        """
        Verifica si la línea entre p1 y p2 cruza algún obstáculo
        """
        for obs in self.obstaculos:
            x, y = obs.pos
            tam = obs.tam / 2

            # Los 4 lados del obstáculo
            esquinas = [
                (int(x - tam), int(y - tam)),  # inferior izquierda
                (int(x + tam), int(y - tam)),  # inferior derecha
                (int(x + tam), int(y + tam)),  # superior derecha
                (int(x - tam), int(y + tam))  # superior izquierda
            ]

            # Verificar intersección con cada lado del obstáculo
            for i in range(4):
                lado_inicio = esquinas[i]
                lado_fin = esquinas[(i + 1) % 4]

                # Si p1 o p2 son vértices del obstáculo, permitir
                if p1 in esquinas or p2 in esquinas:
                    continue

                if self.segmentos_se_intersectan(p1, p2, lado_inicio, lado_fin):
                    return True

        return False

    def es_visible(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        """
        Verifica si dos puntos son visibles entre sí (sin obstáculos en medio)
        Usa verificación geométrica de intersección de segmentos
        """
        # No puede haber visibilidad con uno mismo
        if p1 == p2:
            return False

        # Verificar si la línea cruza algún obstáculo
        return not self.linea_cruza_obstaculo(p1, p2)

    def construir_grafo(self):
        """
        Construye el grafo de visibilidad conectando vértices visibles
        """
        vertices = self.obtener_vertices_obstaculos()

        # Agregar las 4 esquinas del mapa como nodos adicionales
        lim_x, lim_y = self.limites
        esquinas_mapa = [
            (-lim_x, -lim_y),  # esquina inferior izquierda
            (lim_x, -lim_y),  # esquina inferior derecha
            (lim_x, lim_y),  # esquina superior derecha
            (-lim_x, lim_y)  # esquina superior izquierda
        ]

        vertices.extend(esquinas_mapa)

        # Eliminar duplicados
        vertices = list(set(vertices))

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
        if punto in self.grafo:
            return  # Ya existe

        self.grafo[punto] = []

        # Conectar con todos los nodos visibles
        for vertice in list(self.grafo.keys()):
            if vertice != punto and self.es_visible(punto, vertice):
                self.grafo[punto].append(vertice)
                self.grafo[vertice].append(punto)

    def eliminar_punto_temporal(self, punto: Tuple[int, int]):
        """
        Elimina un punto temporal del grafo
        """
        if punto not in self.grafo:
            return  # No existe

        # Eliminar conexiones de otros nodos hacia este punto
        for vecinos in self.grafo.values():
            if punto in vecinos:
                vecinos.remove(punto)

        # Eliminar el nodo
        del self.grafo[punto]

    def obtener_vecinos(self, nodo: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene los vecinos de un nodo en el grafo
        """
        return self.grafo.get(nodo, [])

    def esta_en_grafo(self, punto: Tuple[int, int]) -> bool:
        """
        Verifica si un punto está en el grafo
        """
        return punto in self.grafo