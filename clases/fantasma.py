"""
Clase Fantasma - Usa diferentes algoritmos para perseguir a Pac-Man
Soporta dos métodos de planificación: Visibility Graph y Diagrama de Voronoi
"""
import time
from typing import List, Tuple
from clases.agente import Agente
from planificacion.visibility_graph import VisibilityGraph
from planificacion.diagrama_voronoi import DiagramaVoronoi
from planificacion.busqueda_grafo import BusquedaEnGrafo


class Fantasma(Agente):
    def __init__(self, posx: int, posy: int, algoritmo: str,
                 metodo_planificacion: str, color: tuple):
        """
        Inicializa un fantasma

        Args:
            posx, posy: Posición inicial
            algoritmo: Algoritmo de búsqueda ('bpa', 'greedy', 'a_star')
            metodo_planificacion: Método de planificación ('visibility' o 'voronoi')
            color: Color RGB del fantasma
        """
        super().__init__(posx, posy)
        self.algoritmo = algoritmo
        self.metodo_planificacion = metodo_planificacion
        self.color = color

        # Nombre descriptivo para el fantasma
        nombre_algoritmo = {
            'bpa': 'BPA',
            'greedy': 'Greedy',
            'a_star': 'A*'
        }.get(algoritmo, algoritmo.upper())

        nombre_metodo = {
            'visibility': 'Visibility Graph',
            'voronoi': 'Voronoi Diagram'
        }.get(metodo_planificacion, metodo_planificacion)

        self.algoritmo_usado = f"{nombre_metodo} + {nombre_algoritmo}"

    def perseguir_pacman(
        self,
        pacman_pos: List[int],
        visibility_graph: VisibilityGraph,
        voronoi_diagram: DiagramaVoronoi,
        obstaculos: List
    ) -> bool:
        """
        Calcula la ruta para perseguir a Pac-Man usando el método de planificación
        y algoritmo de búsqueda asignados

        Args:
            pacman_pos: Posición actual de Pac-Man
            visibility_graph: Grafo de visibilidad
            voronoi_diagram: Diagrama de Voronoi
            obstaculos: Lista de obstáculos (no usado actualmente)

        Returns:
            True si se encontró ruta, False en caso contrario
        """
        inicio = time.time()

        pos_actual = self.get_pos_tuple()
        pos_objetivo = tuple(pacman_pos)

        # Seleccionar el grafo según el método de planificación
        if self.metodo_planificacion == 'voronoi':
            grafo_planificacion = voronoi_diagram
        else:  # 'visibility'
            grafo_planificacion = visibility_graph

        # Agregar puntos temporales al grafo seleccionado
        grafo_planificacion.agregar_punto_temporal(pos_actual)
        grafo_planificacion.agregar_punto_temporal(pos_objetivo)

        # Seleccionar algoritmo de búsqueda
        camino = None

        if self.algoritmo == "bpa":
            camino = BusquedaEnGrafo.bpa_grafo(
                grafo_planificacion.grafo,
                pos_actual,
                pos_objetivo
            )
        elif self.algoritmo == "greedy":
            camino = BusquedaEnGrafo.greedy_grafo(
                grafo_planificacion.grafo,
                pos_actual,
                pos_objetivo
            )
        elif self.algoritmo == "a_star":
            camino = BusquedaEnGrafo.a_estrella_grafo(
                grafo_planificacion.grafo,
                pos_actual,
                pos_objetivo
            )

        # Limpiar puntos temporales
        grafo_planificacion.eliminar_punto_temporal(pos_actual)
        grafo_planificacion.eliminar_punto_temporal(pos_objetivo)

        self.tiempo_calculo = time.time() - inicio

        if camino:
            self.trayectoria = [list(pos) for pos in camino]
            return True

        return False