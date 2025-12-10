"""
Clase base para todos los agentes (Pac-Man y Fantasmas)
"""
from typing import List, Tuple, Optional
from clases.nodo import Nodo

class Agente:
    def __init__(self, posx: int, posy: int):
        self.pos = [posx, posy]
        self.trayectoria: List[List[int]] = []
        self.nodos_visitados: List = []
        self.nodos_expandidos: List = []
        self.algoritmo_usado: str = ""
        self.tiempo_calculo: float = 0.0

    def get_pos_tuple(self) -> Tuple[int, int]:
        """Retorna la posición como tupla"""
        return tuple(self.pos)

    def mover_siguiente(self) -> bool:
        """
        Mueve al agente al siguiente punto de su trayectoria
        Returns: True si se movió, False si no hay más trayectoria
        """
        if len(self.trayectoria) > 1:
            self.trayectoria.pop(0)
            self.pos = self.trayectoria[0][:]
            return True
        return False

    def limpiar_trayectoria(self):
        """Limpia la trayectoria y estadísticas"""
        self.trayectoria = []
        self.nodos_visitados = []
        self.nodos_expandidos = []