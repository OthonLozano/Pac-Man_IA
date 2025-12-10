"""
Clase para los puntos que Pac-Man debe recolectar
"""
import numpy as np
from typing import List

class Punto:
    def __init__(self, x: int, y: int, valor: int = 10):
        self.pos = [x, y]
        self.valor = valor
        self.recolectado = False

    def distancia_a(self, pos: List[int]) -> float:
        """Calcula distancia euclidiana a una posición"""
        return np.sqrt((self.pos[0] - pos[0])**2 +
                      (self.pos[1] - pos[1])**2)

    def get_pos_tuple(self) -> tuple:
        """Retorna la posición como tupla"""
        return tuple(self.pos)