"""
Diagrama de Voronoi - Planificación de caminos seguros
Maximiza la distancia a los obstáculos
"""
import numpy as np
from typing import List, Tuple, Dict, Set
from clases.obstaculo import Obstaculo


class DiagramaVoronoi:
    """
    Construye un diagrama de Voronoi para planificación segura.
    Los caminos en el diagrama de Voronoi maximizan la distancia a los obstáculos,
    proporcionando rutas más seguras (aunque potencialmente más largas).
    """

    def __init__(self, obstaculos: List[Obstaculo], limites: Tuple[int, int]):
        """
        Inicializa el diagrama de Voronoi

        Args:
            obstaculos: Lista de obstáculos en el entorno
            limites: Tupla (limite_x, limite_y) del mundo
        """
        self.obstaculos = obstaculos
        self.limites = limites
        self.grafo: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        self.mapa_distancias: Dict[Tuple[int, int], float] = {}
        self.puntos_voronoi: Set[Tuple[int, int]] = set()

        print(f"Construyendo Diagrama de Voronoi...")
        self.construir_voronoi()
        print(f"   ✓ {len(self.grafo)} nodos en el diagrama")
        print(f"   ✓ {sum(len(vecinos) for vecinos in self.grafo.values()) // 2} conexiones")

    def distancia_punto_a_obstaculo(self, punto: Tuple[int, int],
                                    obstaculo: Obstaculo) -> float:
        """
        Calcula la distancia mínima de un punto al borde de un obstáculo

        Args:
            punto: Coordenadas (x, y) del punto
            obstaculo: Obstáculo al que calcular la distancia

        Returns:
            Distancia mínima al borde del obstáculo
        """
        x, y = punto
        ox, oy = obstaculo.pos
        tam = obstaculo.tam / 2

        # Encontrar el punto más cercano en el obstáculo
        closest_x = max(ox - tam, min(x, ox + tam))
        closest_y = max(oy - tam, min(y, oy + tam))

        # Calcular distancia
        dx = x - closest_x
        dy = y - closest_y

        return np.sqrt(dx ** 2 + dy ** 2)

    def distancia_a_obstaculo_mas_cercano(self, punto: Tuple[int, int]) -> float:
        """
        Calcula la distancia al obstáculo más cercano

        Args:
            punto: Coordenadas (x, y) del punto

        Returns:
            Distancia al obstáculo más cercano
        """
        if not self.obstaculos:
            return float('inf')

        distancias = [
            self.distancia_punto_a_obstaculo(punto, obs)
            for obs in self.obstaculos
        ]
        return min(distancias)

    def es_punto_voronoi(self, punto: Tuple[int, int],
                         threshold: float = 0.7) -> bool:
        """
        Verifica si un punto pertenece al diagrama de Voronoi.
        Un punto está en el diagrama si es equidistante a 2 o más obstáculos.

        Args:
            punto: Coordenadas (x, y) del punto
            threshold: Tolerancia para considerar distancias iguales

        Returns:
            True si el punto está en el diagrama de Voronoi
        """
        if not self.obstaculos or len(self.obstaculos) < 2:
            # Con menos de 2 obstáculos, usar puntos con alta clearance
            dist = self.distancia_a_obstaculo_mas_cercano(punto)
            return dist > 2.0

        # Calcular distancias a todos los obstáculos
        distancias = [
            self.distancia_punto_a_obstaculo(punto, obs)
            for obs in self.obstaculos
        ]
        distancias.sort()

        # Verificar si las dos distancias mínimas son similares
        if len(distancias) >= 2:
            diferencia = abs(distancias[0] - distancias[1])
            return diferencia < threshold

        return False

    def punto_en_espacio_libre(self, punto: Tuple[int, int]) -> bool:
        """
        Verifica si un punto está en espacio libre (no dentro de un obstáculo)

        Args:
            punto: Coordenadas (x, y) del punto

        Returns:
            True si el punto está libre
        """
        x, y = punto
        lim_x, lim_y = self.limites

        # Verificar límites del mundo
        if not (-lim_x <= x <= lim_x and -lim_y <= y <= lim_y):
            return False

        # Verificar colisión con obstáculos
        for obs in self.obstaculos:
            if obs.in_collission(x, y):
                return False

        return True

    def camino_seguro(self, p1: Tuple[int, int], p2: Tuple[int, int],
                      min_clearance: float = 1.0) -> bool:
        """
        Verifica si el camino entre dos puntos mantiene distancia segura a obstáculos

        Args:
            p1: Punto inicial
            p2: Punto final
            min_clearance: Distancia mínima requerida a obstáculos

        Returns:
            True si el camino es seguro
        """
        # Calcular número de muestras basado en distancia
        distancia = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        num_samples = max(int(distancia), 3)

        for i in range(num_samples + 1):
            t = i / num_samples
            x = int(p1[0] + t * (p2[0] - p1[0]))
            y = int(p1[1] + t * (p2[1] - p1[1]))

            # Verificar que esté en espacio libre
            if not self.punto_en_espacio_libre((x, y)):
                return False

            # Verificar clearance mínima
            dist = self.distancia_a_obstaculo_mas_cercano((x, y))
            if dist < min_clearance:
                return False

        return True

    def construir_voronoi(self):
        """
        Construye el diagrama de Voronoi mediante discretización del espacio.
        Identifica puntos equidistantes a múltiples obstáculos y los conecta.
        """
        lim_x, lim_y = self.limites
        candidatos = []

        # Fase 1: Identificar puntos del diagrama de Voronoi
        for x in range(-lim_x, lim_x + 1):
            for y in range(-lim_y, lim_y + 1):
                punto = (x, y)

                # Verificar que esté en espacio libre
                if not self.punto_en_espacio_libre(punto):
                    continue

                # Calcular distancia al obstáculo más cercano
                dist = self.distancia_a_obstaculo_mas_cercano(punto)
                self.mapa_distancias[punto] = dist

                # Agregar si es punto de Voronoi o tiene alta clearance
                if self.es_punto_voronoi(punto) or dist > 2.5:
                    candidatos.append(punto)
                    self.puntos_voronoi.add(punto)

        # Inicializar grafo
        for punto in candidatos:
            self.grafo[punto] = []

        # Fase 2: Conectar puntos cercanos manteniendo seguridad
        radio_conexion = 2.0  # Radio para buscar vecinos

        for punto in candidatos:
            px, py = punto

            # Buscar vecinos en un radio
            for vecino in candidatos:
                if punto == vecino:
                    continue

                vx, vy = vecino
                distancia = np.sqrt((vx - px) ** 2 + (vy - py) ** 2)

                # Conectar si están cerca y el camino es seguro
                if distancia <= radio_conexion:
                    if self.camino_seguro(punto, vecino, min_clearance=0.8):
                        # Evitar duplicados
                        if vecino not in self.grafo[punto]:
                            self.grafo[punto].append(vecino)
                        if punto not in self.grafo[vecino]:
                            self.grafo[vecino].append(punto)

    def agregar_punto_temporal(self, punto: Tuple[int, int]):
        """
        Agrega un punto temporal al grafo (posición de agentes).
        Conecta el punto con nodos cercanos del diagrama.

        Args:
            punto: Coordenadas del punto temporal
        """
        if punto in self.grafo:
            return  # Ya existe

        self.grafo[punto] = []
        radio_conexion = 5.0  # Radio más amplio para puntos temporales

        # Conectar con nodos cercanos del diagrama
        for nodo in list(self.grafo.keys()):
            if nodo == punto:
                continue

            distancia = np.sqrt(
                (nodo[0] - punto[0]) ** 2 +
                (nodo[1] - punto[1]) ** 2
            )

            if distancia <= radio_conexion:
                # Verificar que el camino sea seguro (clearance menor para conexión temporal)
                if self.camino_seguro(punto, nodo, min_clearance=0.5):
                    self.grafo[punto].append(nodo)
                    self.grafo[nodo].append(punto)

    def eliminar_punto_temporal(self, punto: Tuple[int, int]):
        """
        Elimina un punto temporal del grafo

        Args:
            punto: Coordenadas del punto a eliminar
        """
        if punto not in self.grafo:
            return

        # Eliminar conexiones de otros nodos hacia este punto
        for vecinos in self.grafo.values():
            if punto in vecinos:
                vecinos.remove(punto)

        # Eliminar el nodo
        del self.grafo[punto]

    def obtener_vecinos(self, nodo: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene los vecinos de un nodo en el grafo

        Args:
            nodo: Coordenadas del nodo

        Returns:
            Lista de vecinos
        """
        return self.grafo.get(nodo, [])

    def esta_en_grafo(self, punto: Tuple[int, int]) -> bool:
        """
        Verifica si un punto está en el grafo

        Args:
            punto: Coordenadas del punto

        Returns:
            True si el punto está en el grafo
        """
        return punto in self.grafo

    def obtener_clearance(self, punto: Tuple[int, int]) -> float:
        """
        Obtiene la distancia de clearance (margen de seguridad) de un punto

        Args:
            punto: Coordenadas del punto

        Returns:
            Distancia al obstáculo más cercano
        """
        if punto in self.mapa_distancias:
            return self.mapa_distancias[punto]
        return self.distancia_a_obstaculo_mas_cercano(punto)