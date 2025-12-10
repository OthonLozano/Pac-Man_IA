"""
Clase PacMan - Usa Visibility Graph + A* para navegar
"""
import time
from typing import List, Tuple, Optional
from clases.agente import Agente
from clases.punto import Punto
from clases.fantasma import Fantasma
from planificacion.visibility_graph import VisibilityGraph
from planificacion.busqueda_grafo import BusquedaEnGrafo


class PacMan(Agente):
    def __init__(self, posx: int, posy: int):
        super().__init__(posx, posy)
        self.puntos_recolectados = 0
        self.puntaje = 0
        self.vivo = True
        self.algoritmo_usado = "Visibility Graph + A*"
        self.distancia_seguridad = 3  # Distancia mínima a fantasmas

    def calcular_ruta_hacia_punto(
            self,
            punto: Punto,
            visibility_graph: VisibilityGraph,
            obstaculos: List,
            fantasmas: List[Fantasma]
    ) -> bool:
        """
        Calcula la ruta hacia un punto usando Visibility Graph + A*
        Evita fantasmas cercanos
        Returns: True si se encontró ruta, False en caso contrario
        """
        inicio = time.time()

        # Verificar si el punto es seguro (lejos de fantasmas)
        if not self._es_punto_seguro(punto.pos, fantasmas):
            return False

        # Agregar posición actual y objetivo al grafo temporal
        pos_actual = self.get_pos_tuple()
        pos_objetivo = punto.get_pos_tuple()

        visibility_graph.agregar_punto_temporal(pos_actual)
        visibility_graph.agregar_punto_temporal(pos_objetivo)

        # Buscar ruta con A*
        camino = BusquedaEnGrafo.a_estrella_grafo(
            visibility_graph.grafo,
            pos_actual,
            pos_objetivo
        )

        # Limpiar puntos temporales
        visibility_graph.eliminar_punto_temporal(pos_actual)
        visibility_graph.eliminar_punto_temporal(pos_objetivo)

        self.tiempo_calculo = time.time() - inicio

        if camino:
            # Convertir tuplas a listas para compatibilidad
            self.trayectoria = [list(pos) for pos in camino]
            return True

        return False

    def _es_punto_seguro(self, punto_pos: List[int], fantasmas: List[Fantasma]) -> bool:
        """
        Verifica si un punto está lo suficientemente lejos de los fantasmas
        """
        for fantasma in fantasmas:
            distancia = ((punto_pos[0] - fantasma.pos[0]) ** 2 +
                         (punto_pos[1] - fantasma.pos[1]) ** 2) ** 0.5

            if distancia < self.distancia_seguridad:
                return False

        return True

    def buscar_punto_mas_cercano_seguro(
            self,
            puntos: List[Punto],
            visibility_graph: VisibilityGraph,
            obstaculos: List,
            fantasmas: List[Fantasma]
    ) -> Optional[Punto]:
        """
        Busca el punto más cercano que sea seguro (lejos de fantasmas)
        """
        puntos_disponibles = [p for p in puntos if not p.recolectado]

        if not puntos_disponibles:
            return None

        # Ordenar puntos por distancia
        puntos_disponibles.sort(key=lambda p: p.distancia_a(self.pos))

        # Intentar calcular ruta al punto más cercano seguro
        for punto in puntos_disponibles:
            if self.calcular_ruta_hacia_punto(punto, visibility_graph, obstaculos, fantasmas):
                return punto

        return None

    def recolectar_punto(self, punto: Punto):
        """Recolecta un punto y suma el puntaje"""
        punto.recolectado = True
        self.puntos_recolectados += 1
        self.puntaje += punto.valor

    def verificar_colision_fantasma(self, fantasmas: List[Fantasma]) -> bool:
        """Verifica si colisionó con algún fantasma"""
        for fantasma in fantasmas:
            if self.pos == fantasma.pos:
                self.vivo = False
                return True
        return False