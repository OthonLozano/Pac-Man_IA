"""
Funciones auxiliares
"""
import numpy as np
from typing import Tuple

def distancia_euclidiana(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Calcula la distancia euclidiana entre dos puntos"""
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def distancia_manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calcula la distancia de Manhattan entre dos puntos"""
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])