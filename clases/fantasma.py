"""
Clase Fantasma - Usa diferentes algoritmos para perseguir a Pac-Man
"""
import time
from typing import List, Tuple
from clases.agente import Agente
from planificacion.visibility_graph import VisibilityGraph
from planificacion.busqueda_grafo import BusquedaEnGrafo


class Fantasma(Agente):
    def __init__(self, posx: int, posy: int, algoritmo: str, color: tuple):
        super().__init__(posx, posy)
        self.algoritmo = algoritmo  # "bpa", "greedy", "a_star"
        self.color = color
        self.algoritmo_usado = f"Visibility Graph + {algoritmo.upper()}"

    def perseguir_pacman(
            self,
            pacman_pos: List[int],
            visibility_graph: VisibilityGraph,
            obstaculos: List
    ) -> bool:
        """
        Calcula la ruta para perseguir a Pac-Man
        Returns: True si se encontró ruta, False en caso contrario
        """
        inicio = time.time()

        pos_actual = self.get_pos_tuple()
        pos_objetivo = tuple(pacman_pos)

        # Agregar puntos temporales al grafo
        visibility_graph.agregar_punto_temporal(pos_actual)
        visibility_graph.agregar_punto_temporal(pos_objetivo)

        # Seleccionar algoritmo de búsqueda
        camino = None

        if self.algoritmo == "bpa":
            camino = BusquedaEnGrafo.bpa_grafo(
                visibility_graph.grafo,
                pos_actual,
                pos_objetivo
            )
        elif self.algoritmo == "greedy":
            camino = BusquedaEnGrafo.greedy_grafo(
                visibility_graph.grafo,
                pos_actual,
                pos_objetivo
            )
        elif self.algoritmo == "a_star":
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
            self.trayectoria = [list(pos) for pos in camino]
            return True

        return False