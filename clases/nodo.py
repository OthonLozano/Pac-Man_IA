import numpy as np
from typing import List, Tuple, Optional


class Nodo:
    """
    Representa un nodo en el espacio de búsqueda
    """

    def __init__(self, pos: List[int], padre: Optional['Nodo'] = None):
        self.pos = pos
        self.papa = padre
        self.hijos: List['Nodo'] = []
        self.h: Optional[float] = None

        if padre is not None:
            self.g = padre.g + 1
        else:
            self.g = 0

    def expande(self, obstaculos, env_size, goal=None):
        """
        Expande el nodo generando sus hijos (vecinos válidos)
        """
        limite = env_size / 2

        direcciones = [
            [self.pos[0], self.pos[1] + 1],  # arriba
            [self.pos[0] + 1, self.pos[1]],  # derecha
            [self.pos[0], self.pos[1] - 1],  # abajo
            [self.pos[0] - 1, self.pos[1]]  # izquierda
        ]

        for nueva_pos in direcciones:
            x, y = nueva_pos

            if -limite <= x <= limite and -limite <= y <= limite:
                hay_colision = False
                for obs in obstaculos:
                    if obs.in_collission(x, y):
                        hay_colision = True
                        break

                if not hay_colision:
                    nuevo = Nodo([x, y], self)
                    if goal is not None:
                        nuevo.heuristica(goal)
                    self.hijos.append(nuevo)

    def heuristica(self, goal: List[int]) -> float:
        """
        Calcula la distancia euclidiana al objetivo
        """
        self.h = np.sqrt((goal[0] - self.pos[0]) ** 2 +
                         (goal[1] - self.pos[1]) ** 2)
        return self.h

    def f_n(self, goal: List[int]) -> float:
        """
        Función de evaluación para A*: f(n) = g(n) + h(n)
        """
        if self.h is not None:
            return self.g + self.h
        return self.g + self.heuristica(goal)

    def bpa(self, goal: List[int], obstaculos, entorno) -> Tuple[Optional[List['Nodo']], List['Nodo'], List['Nodo']]:
        """
        Búsqueda Primero en Anchura (BPA/BFS)
        """
        visitados = []
        expandidos = []

        if self.pos == goal:
            return [self], visitados, expandidos

        if self in visitados:
            return None, visitados, expandidos

        self.expande(obstaculos, entorno)
        visitados.append(self)

        if len(self.hijos) > 0:
            expandidos.append(self)

        por_visitar = self.hijos[:]

        while por_visitar:
            h = por_visitar.pop(0)

            if h.pos == goal:
                camino = [h]
                papa = h.papa
                while papa:
                    camino.append(papa)
                    papa = papa.papa
                return camino, visitados, expandidos

            if h in visitados:
                continue

            h.expande(obstaculos, entorno)
            visitados.append(h)

            if len(h.hijos) > 0:
                expandidos.append(h)

            por_visitar += h.hijos

        return None, visitados, expandidos

    def greedy(self, goal: List[int], obstaculos, env_size) -> Tuple[
        Optional[List['Nodo']], List['Nodo'], List['Nodo']]:
        """
        Búsqueda Greedy (voraz)
        """
        visitados = []
        expandidos = []

        if self.pos == goal:
            return [self], visitados, expandidos

        if self in visitados:
            return None, visitados, expandidos

        self.expande(obstaculos, env_size, goal)
        visitados.append(self)

        if len(self.hijos) > 0:
            expandidos.append(self)

        franja = self.hijos[:]
        franja.sort()

        while franja:
            h = franja.pop(0)

            if h.pos == goal:
                camino = [h]
                papa = h.papa
                while papa:
                    camino.append(papa)
                    papa = papa.papa
                return camino, visitados, expandidos

            if h in visitados:
                continue

            visitados.append(h)
            h.expande(obstaculos, env_size, goal)

            if len(h.hijos) > 0:
                expandidos.append(h)

            franja += h.hijos[:]
            franja.sort()

        return None, visitados, expandidos

    def a_estrella(self, goal: List[int], obstaculos, env_size) -> Tuple[
        Optional[List['Nodo']], List['Nodo'], List['Nodo']]:
        """
        Algoritmo A*
        """
        visitados = []
        expandidos = []

        if self.pos == goal:
            return [self], visitados, expandidos

        if self in visitados:
            return None, visitados, expandidos

        self.expande(obstaculos, env_size, goal)
        visitados.append(self)

        if len(self.hijos) > 0:
            expandidos.append(self)

        franja = self.hijos[:]
        franja.sort(key=lambda nodo: nodo.f_n(goal))

        while franja:
            h = franja.pop(0)

            if h.pos == goal:
                camino = [h]
                papa = h.papa
                while papa:
                    camino.append(papa)
                    papa = papa.papa
                return camino, visitados, expandidos

            if h in visitados:
                continue

            visitados.append(h)
            h.expande(obstaculos, env_size, goal)

            if len(h.hijos) > 0:
                expandidos.append(h)

            franja += h.hijos[:]
            franja.sort(key=lambda nodo: nodo.f_n(goal))

        return None, visitados, expandidos

    def __eq__(self, nodo2: 'Nodo') -> bool:
        return self.pos == nodo2.pos

    def __repr__(self) -> str:
        return str(self.pos)

    def __lt__(self, nodo2: 'Nodo') -> bool:
        return self.h < nodo2.h