"""
Clase PacMan - Modo interactivo y automático
"""
import time
from typing import List, Tuple, Optional
from clases.agente import Agente
from clases.punto import Punto
from clases.fantasma import Fantasma
from planificacion.visibility_graph import VisibilityGraph
from planificacion.busqueda_grafo import BusquedaEnGrafo

class PacMan(Agente):
    def __init__(self, posx: int, posy: int, modo_interactivo: bool = True):
        super().__init__(posx, posy)
        self.puntos_recolectados = 0
        self.puntaje = 0
        self.vivo = True
        self.modo_interactivo = modo_interactivo
        self.algoritmo_usado = "Control Manual" if modo_interactivo else "Visibility Graph + A*"
        self.distancia_seguridad = 3

        # Para modo interactivo
        self.direccion_actual = [0, 0]  # [dx, dy]
        self.proxima_direccion = [0, 0]

    def mover_en_direccion(self, direccion: List[int], obstaculos: List) -> bool:
        """
        Intenta mover en una dirección específica
        Returns: True si el movimiento fue válido
        """
        nueva_pos = [self.pos[0] + direccion[0], self.pos[1] + direccion[1]]

        # Verificar límites
        from config.configuracion import LIMITE
        if not (-LIMITE <= nueva_pos[0] <= LIMITE and -LIMITE <= nueva_pos[1] <= LIMITE):
            return False

        # Verificar colisión con obstáculos
        for obs in obstaculos:
            if obs.in_collission(nueva_pos[0], nueva_pos[1]):
                return False

        # Movimiento válido
        self.pos = nueva_pos
        return True

    def set_direccion(self, direccion: str):
        """
        Establece la dirección de movimiento basada en tecla presionada
        """
        direcciones = {
            'up': [0, 1],
            'down': [0, -1],
            'left': [-1, 0],
            'right': [1, 0]
        }

        if direccion in direcciones:
            self.proxima_direccion = direcciones[direccion]

    def actualizar_movimiento_interactivo(self, obstaculos: List) -> bool:
        """
        Actualiza la posición en modo interactivo
        """
        # Intentar cambiar a la próxima dirección
        if self.proxima_direccion != [0, 0]:
            if self.mover_en_direccion(self.proxima_direccion, obstaculos):
                self.direccion_actual = self.proxima_direccion
                return True

        # Si no se pudo cambiar, continuar en dirección actual
        if self.direccion_actual != [0, 0]:
            return self.mover_en_direccion(self.direccion_actual, obstaculos)

        return False

    def calcular_ruta_hacia_punto(
        self,
        punto: Punto,
        visibility_graph: VisibilityGraph,
        obstaculos: List,
        fantasmas: List[Fantasma]
    ) -> bool:
        """
        Modo automático: Calcula ruta con A*
        """
        if self.modo_interactivo:
            return False

        inicio = time.time()

        if not self._es_punto_seguro(punto.pos, fantasmas):
            return False

        pos_actual = self.get_pos_tuple()
        pos_objetivo = punto.get_pos_tuple()

        visibility_graph.agregar_punto_temporal(pos_actual)
        visibility_graph.agregar_punto_temporal(pos_objetivo)

        camino = BusquedaEnGrafo.a_estrella_grafo(
            visibility_graph.grafo,
            pos_actual,
            pos_objetivo
        )

        visibility_graph.eliminar_punto_temporal(pos_actual)
        visibility_graph.eliminar_punto_temporal(pos_objetivo)

        self.tiempo_calculo = time.time() - inicio

        if camino:
            self.trayectoria = [list(pos) for pos in camino]
            return True

        return False

    def _es_punto_seguro(self, punto_pos: List[int], fantasmas: List[Fantasma]) -> bool:
        """Verifica si un punto está lejos de fantasmas"""
        for fantasma in fantasmas:
            distancia = ((punto_pos[0] - fantasma.pos[0])**2 +
                        (punto_pos[1] - fantasma.pos[1])**2)**0.5
            if distancia < self.distancia_seguridad:
                return False
        return True

    def recolectar_punto(self, punto: Punto):
        """Recolecta un punto y suma puntaje"""
        punto.recolectado = True
        self.puntos_recolectados += 1
        self.puntaje += punto.valor

    def verificar_colision_fantasma(self, fantasmas: List[Fantasma]) -> bool:
        """Verifica colisión con fantasmas"""
        for fantasma in fantasmas:
            if self.pos == fantasma.pos:
                self.vivo = False
                return True
        return False