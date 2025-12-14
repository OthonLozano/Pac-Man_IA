"""
Clase que representa el mundo del juego
"""
from typing import List, Optional
from clases.pacman import PacMan
from clases.fantasma import Fantasma
from clases.obstaculo import Obstaculo
from clases.punto import Punto
from planificacion.visibility_graph import VisibilityGraph
from planificacion.diagrama_voronoi import DiagramaVoronoi
from config.configuracion import *
from config.niveles import NIVELES
import random

class Entorno:
    def __init__(self, nivel: int = 0, modo_interactivo: bool = True):
        self.size = TAMANIO_MUNDO
        self.nivel_actual = nivel
        self.modo_interactivo = modo_interactivo

        self.pacman: Optional[PacMan] = None
        self.fantasmas: List[Fantasma] = []
        self.obstaculos: List[Obstaculo] = []
        self.puntos: List[Punto] = []
        self.puntaje = 0
        self.juego_terminado = False
        self.victoria = False

        # AMBOS métodos de planificación
        self.visibility_graph: Optional[VisibilityGraph] = None
        self.voronoi_diagram: Optional[DiagramaVoronoi] = None

        self._inicializar_nivel()

    def _inicializar_nivel(self):
        """Inicializa el nivel actual"""
        if self.nivel_actual >= len(NIVELES):
            print("¡Completaste todos los niveles!")
            self.juego_terminado = True
            self.victoria = True
            return

        nivel_config = NIVELES[self.nivel_actual]
        print(f"\n{'=' * 60}")
        print(f"NIVEL {self.nivel_actual + 1}: {nivel_config['nombre']}")
        print(f"{'=' * 60}\n")

        # Crear obstáculos del nivel
        for x, y, tam in nivel_config['obstaculos']:
            self.obstaculos.append(Obstaculo(x, y, tam))

        # Visibility Graph (caminos óptimos)
        self.visibility_graph = VisibilityGraph(
            self.obstaculos,
            (LIMITE, LIMITE)
        )

        # Diagrama de Voronoi (caminos seguros)
        self.voronoi_diagram = DiagramaVoronoi(
            self.obstaculos,
            (LIMITE, LIMITE)
        )

        self.pacman = PacMan(0, 0, self.modo_interactivo) # Pac-Man en el centro



        # Configuraciones FIJAS: (algoritmo, método_planificación, color)
        configuraciones = [
            ('a_star', 'visibility', COLOR_FANTASMA_VG_ASTAR),      # Fantasma 1
            ('bpa', 'visibility', COLOR_FANTASMA_VG_BPA),           # Fantasma 2
            ('a_star', 'voronoi', COLOR_FANTASMA_VORONOI_ASTAR),    # Fantasma 3
            ('bpa', 'voronoi', COLOR_FANTASMA_VORONOI_BPA)          # Fantasma 4
        ]

        # Posiciones iniciales de los fantasmas en las 4 esquinas
        posiciones_iniciales = [
            (-8, 8),   # Esquina superior izquierda
            (8, 8),    # Esquina superior derecha
            (-8, -8),  # Esquina inferior izquierda
            (8, -8)    # Esquina inferior derecha
        ]

        for i in range(4):
            x, y = posiciones_iniciales[i]
            algoritmo, metodo, color = configuraciones[i]

            fantasma = Fantasma(x, y, algoritmo, metodo, color)
            self.fantasmas.append(fantasma)



        # Generar puntos a recolectar de manera random
        self._generar_puntos(nivel_config['puntos'])

    def _generar_puntos(self, cantidad: int):
        """Genera puntos válidos en el mapa"""
        puntos_generados = 0
        intentos = 0
        max_intentos = cantidad * 50

        while puntos_generados < cantidad and intentos < max_intentos:
            x = random.randint(-LIMITE + 2, LIMITE - 2)
            y = random.randint(-LIMITE + 2, LIMITE - 2)

            # Verificar colisiones
            colision = False

            # Con obstáculos
            for obs in self.obstaculos:
                if obs.in_collission(x, y):
                    colision = True
                    break

            # Con spawn de Pac-Man (más espacio)
            if abs(x) <= 2 and abs(y) <= 2:
                colision = True

            # Con spawn de fantasmas (más espacio)
            for fantasma in self.fantasmas:
                if abs(x - fantasma.pos[0]) <= 3 and abs(y - fantasma.pos[1]) <= 3:
                    colision = True
                    break

            if not colision:
                self.puntos.append(Punto(x, y))
                puntos_generados += 1

            intentos += 1

        if puntos_generados < cantidad:
            print(f"Solo se pudieron generar {puntos_generados}/{cantidad} puntos")

    def actualizar(self):
        """Actualiza el juego cada frame"""
        if self.juego_terminado:
            return

        if not self.pacman.vivo:
            self.juego_terminado = True
            self.victoria = False
            print("\nGAME OVER - Pac-Man fue atrapado")
            return

        # Verificar victoria
        puntos_restantes = [p for p in self.puntos if not p.recolectado]
        if not puntos_restantes:
            print(f"\n¡Nivel {self.nivel_actual + 1} completado!")
            self.nivel_actual += 1

            if self.nivel_actual >= len(NIVELES):
                self.juego_terminado = True
                self.victoria = True
                print("\n¡GANASTE EL JUEGO COMPLETO!")
            else:
                self._reiniciar_nivel()
            return

        # MOVER PAC-MAN
        if self.modo_interactivo:
            self.pacman.actualizar_movimiento_interactivo(self.obstaculos)
        else:
            if not self.pacman.trayectoria or len(self.pacman.trayectoria) <= 1:
                punto_objetivo = self._buscar_mejor_punto()
                if punto_objetivo:
                    self.pacman.calcular_ruta_hacia_punto(
                        punto_objetivo,
                        self.visibility_graph,
                        self.obstaculos,
                        self.fantasmas
                    )

            if self.pacman.trayectoria and len(self.pacman.trayectoria) > 1:
                self.pacman.mover_siguiente()

        # Verificar recolección de puntos
        for punto in self.puntos:
            if not punto.recolectado and self.pacman.pos == punto.pos:
                self.pacman.recolectar_punto(punto)
                self.puntaje = self.pacman.puntaje

        # MOVER FANTASMAS
        for fantasma in self.fantasmas:
            if not fantasma.trayectoria or len(fantasma.trayectoria) <= 1:
                fantasma.perseguir_pacman(
                    self.pacman.pos,
                    self.visibility_graph,
                    self.voronoi_diagram,
                    self.obstaculos
                )

            if fantasma.trayectoria and len(fantasma.trayectoria) > 1:
                fantasma.mover_siguiente()

        # VERIFICAR COLISIONES
        self.pacman.verificar_colision_fantasma(self.fantasmas)

    def _buscar_mejor_punto(self) -> Optional[Punto]:
        """Busca el mejor punto para recolectar (modo automático)"""
        puntos_disponibles = [p for p in self.puntos if not p.recolectado]
        if not puntos_disponibles:
            return None
        return min(puntos_disponibles, key=lambda p: p.distancia_a(self.pacman.pos))

    def _reiniciar_nivel(self):
        """Reinicia variables para el siguiente nivel"""
        self.pacman = None
        self.fantasmas = []
        self.obstaculos = []
        self.puntos = []
        self.puntaje = 0
        self.juego_terminado = False
        self.victoria = False
        self.visibility_graph = None
        self.voronoi_diagram = None
        self._inicializar_nivel()