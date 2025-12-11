"""
Funciones auxiliares y utilidades
"""
import numpy as np
from typing import Tuple, List

def distancia_euclidiana(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Calcula la distancia euclidiana entre dos puntos"""
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def distancia_manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calcula la distancia de Manhattan entre dos puntos"""
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def normalizar_posicion(pos: List[int], limite: int) -> List[int]:
    """
    Normaliza una posición para mantenerla dentro de los límites
    """
    x = max(-limite, min(limite, pos[0]))
    y = max(-limite, min(limite, pos[1]))
    return [x, y]

def punto_en_rectangulo(punto: Tuple[int, int],
                        centro: Tuple[int, int],
                        ancho: float,
                        alto: float) -> bool:
    """
    Verifica si un punto está dentro de un rectángulo
    """
    x, y = punto
    cx, cy = centro

    return (cx - ancho/2 <= x <= cx + ancho/2 and
            cy - alto/2 <= y <= cy + alto/2)

def interpolar_camino(camino: List[List[int]], num_puntos: int = 10) -> List[List[int]]:
    """
    Interpola un camino para suavizar el movimiento
    Útil para animaciones más fluidas
    """
    if len(camino) < 2:
        return camino

    camino_suave = []

    for i in range(len(camino) - 1):
        p1 = np.array(camino[i])
        p2 = np.array(camino[i + 1])

        for t in np.linspace(0, 1, num_puntos):
            punto_interpolado = p1 + t * (p2 - p1)
            camino_suave.append([int(punto_interpolado[0]), int(punto_interpolado[1])])

    camino_suave.append(camino[-1])
    return camino_suave