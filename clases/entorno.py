"""
Clase que representa el mundo del juego
"""
from typing import List, Optional
from clases.pacman import PacMan
from clases.fantasma import Fantasma
from clases.obstaculo import Obstaculo
from clases.punto import Punto
from planificacion.visibility_graph import VisibilityGraph
from config.configuracion import *
import random

class Entorno:
    def __init__(self):
        self.size = TAMANIO_MUNDO
        self.pacman: Optional[PacMan] = None
        self.fantasmas: List[Fantasma] = []
        self.obstaculos: List[Obstaculo] = []
        self.puntos: List[Punto] = []
        self.puntaje = 0
        self.juego_terminado = False
        self.victoria = False
        self.visibility_graph: Optional[VisibilityGraph] = None

        self._inicializar()

    def _inicializar(self):
        """Inicializa el mundo con todos los elementos"""
        # Crear obstáculos
        for x, y, tam in OBSTACULOS:
            self.obstaculos.append(Obstaculo(x, y, tam))

        # Crear Visibility Graph
        self.visibility_graph = VisibilityGraph(
            self.obstaculos,
            (LIMITE, LIMITE)
        )

        # Crear Pac-Man
        self.pacman = PacMan(0, 0)

        # Crear fantasmas con diferentes algoritmos
        self.fantasmas = [
            Fantasma(5, 5, "bpa", COLOR_FANTASMA_BPA),
            Fantasma(-5, 5, "greedy", COLOR_FANTASMA_GREEDY),
            Fantasma(5, -5, "a_star", COLOR_FANTASMA_A_STAR),
        ]

        # Generar puntos
        self._generar_puntos()

    def _generar_puntos(self):
        """Genera puntos en posiciones aleatorias válidas"""
        puntos_generados = 0
        intentos = 0
        max_intentos = 1000

        while puntos_generados < NUMERO_PUNTOS and intentos < max_intentos:
            x = random.randint(-LIMITE + 1, LIMITE - 1)
            y = random.randint(-LIMITE + 1, LIMITE - 1)

            # Verificar que no colisione con obstáculos
            colision = False
            for obs in self.obstaculos:
                if obs.in_collission(x, y):
                    colision = True
                    break

            # Verificar que no esté muy cerca de Pac-Man o fantasmas
            if not colision:
                if abs(x) < 2 and abs(y) < 2:  # Muy cerca del inicio de Pac-Man
                    colision = True

            if not colision:
                self.puntos.append(Punto(x, y))
                puntos_generados += 1

            intentos += 1

    def actualizar(self):
        """Actualiza el estado del juego (un paso de simulación)"""
        if self.juego_terminado:
            return

        # Verificar si Pac-Man sigue vivo
        if not self.pacman.vivo:
            self.juego_terminado = True
            self.victoria = False
            return

        # Verificar si recolectó todos los puntos
        if all(p.recolectado for p in self.puntos):
            self.juego_terminado = True
            self.victoria = True
            return

        # Pac-Man busca el siguiente punto
        if not self.pacman.trayectoria:
            punto_objetivo = self.pacman.buscar_punto_mas_cercano_seguro(
                self.puntos,
                self.visibility_graph,
                self.obstaculos,
                self.fantasmas
            )

            if punto_objetivo:
                # Verificar si llegó al punto
                if self.pacman.pos == punto_objetivo.pos:
                    self.pacman.recolectar_punto(punto_objetivo)
                    self.puntaje = self.pacman.puntaje

        # Mover Pac-Man
        self.pacman.mover_siguiente()

        # Fantasmas persiguen a Pac-Man
        for fantasma in self.fantasmas:
            if not fantasma.trayectoria:
                fantasma.perseguir_pacman(
                    self.pacman.pos,
                    self.visibility_graph,
                    self.obstaculos
                )

            fantasma.mover_siguiente()

        # Verificar colisiones con fantasmas
        self.pacman.verificar_colision_fantasma(self.fantasmas)