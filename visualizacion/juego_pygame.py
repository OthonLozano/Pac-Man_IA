"""
Visualización del juego con Pygame (modo interactivo)
"""
import pygame
import sys
from typing import List, Tuple
from clases.entorno import Entorno
from config.configuracion import *


class JuegoPygame:
    def __init__(self, entorno: Entorno):
        pygame.init()

        self.entorno = entorno
        self.ancho = ANCHO_VENTANA
        self.alto = ALTO_VENTANA
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption(f"Pac-Man IA - Nivel {entorno.nivel_actual + 1}")

        self.clock = pygame.time.Clock()
        self.fps = FPS

        # Calcular tamaño de celda
        self.cell_size = self.ancho // (TAMANIO_MUNDO + 2)
        self.offset_x = self.ancho // 2
        self.offset_y = self.alto // 2

        # Fuentes
        self.font_grande = pygame.font.Font(None, 48)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_pequeña = pygame.font.Font(None, 24)

        # Contador de frames para controlar velocidad
        self.frame_count = 0
        self.velocidad_pacman = VELOCIDAD_PACMAN
        self.velocidad_fantasma = 2  # Más lento que antes

        # Estado del juego
        self.pausa = False
        self.mostrar_ayuda = True

        #Tiempo de gracia al inicio
        self.tiempo_gracia = 180  # 3 segundos a 60 FPS
        self.en_gracia = True

    def mundo_a_pantalla(self, x: int, y: int) -> Tuple[int, int]:
        """Convierte coordenadas del mundo a coordenadas de pantalla"""
        screen_x = self.offset_x + (x * self.cell_size)
        screen_y = self.offset_y - (y * self.cell_size)
        return (screen_x, screen_y)

    def dibujar_grid(self):
        """Dibuja la cuadrícula de fondo"""
        for x in range(-LIMITE, LIMITE + 1):
            for y in range(-LIMITE, LIMITE + 1):
                pos_x, pos_y = self.mundo_a_pantalla(x, y)
                pygame.draw.rect(
                    self.screen,
                    (20, 20, 20),
                    (pos_x - self.cell_size // 2, pos_y - self.cell_size // 2,
                     self.cell_size, self.cell_size),
                    1
                )

    def dibujar_obstaculos(self):
        """Dibuja los obstáculos (paredes del laberinto)"""
        for obs in self.entorno.obstaculos:
            x, y = obs.pos
            tam = obs.tam

            pos_x, pos_y = self.mundo_a_pantalla(x, y)

            # Dibujar cuadrado con borde brillante (estilo Pac-Man)
            rect = pygame.Rect(
                pos_x - (tam * self.cell_size) // 2,
                pos_y - (tam * self.cell_size) // 2,
                tam * self.cell_size,
                tam * self.cell_size
            )

            # Relleno
            pygame.draw.rect(self.screen, COLOR_OBSTACULO, rect)
            # Borde brillante
            pygame.draw.rect(self.screen, (100, 100, 255), rect, 3)

    def dibujar_puntos(self):
        """Dibuja los puntos a recolectar"""
        for punto in self.entorno.puntos:
            if not punto.recolectado:
                x, y = punto.pos
                pos_x, pos_y = self.mundo_a_pantalla(x, y)

                # Punto pequeño blanco
                pygame.draw.circle(
                    self.screen,
                    COLOR_PUNTO,
                    (pos_x, pos_y),
                    self.cell_size // 4
                )

    def dibujar_pacman(self):
        """Dibuja a Pac-Man"""
        if not self.entorno.pacman.vivo:
            return

        x, y = self.entorno.pacman.pos
        pos_x, pos_y = self.mundo_a_pantalla(x, y)

        # Círculo amarillo más grande
        radio = int(self.cell_size * 0.4)
        pygame.draw.circle(
            self.screen,
            COLOR_PACMAN,
            (pos_x, pos_y),
            radio
        )

        # "Boca" de Pac-Man (triángulo negro)
        direccion = self.entorno.pacman.direccion_actual
        if direccion != [0, 0]:
            # Calcular ángulo de la boca
            import math
            angulo = math.atan2(direccion[1], direccion[0])

            # Dibujar sector circular (boca abierta)
            puntos = [
                (pos_x, pos_y),
                (pos_x + radio * math.cos(angulo + 0.5),
                 pos_y - radio * math.sin(angulo + 0.5)),
                (pos_x + radio * math.cos(angulo - 0.5),
                 pos_y - radio * math.sin(angulo - 0.5))
            ]
            pygame.draw.polygon(self.screen, COLOR_FONDO, puntos)

    def dibujar_fantasmas(self):
        """Dibuja los fantasmas"""
        for fantasma in self.entorno.fantasmas:
            x, y = fantasma.pos
            pos_x, pos_y = self.mundo_a_pantalla(x, y)

            # Cuerpo del fantasma (cuadrado redondeado)
            radio = int(self.cell_size * 0.35)

            # Cuerpo principal
            pygame.draw.circle(
                self.screen,
                fantasma.color,
                (pos_x, pos_y),
                radio
            )

            # Ojos blancos
            ojo_radio = radio // 4
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (pos_x - radio // 3, pos_y - radio // 4),
                ojo_radio
            )
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (pos_x + radio // 3, pos_y - radio // 4),
                ojo_radio
            )

            # Pupilas negras
            pupila_radio = ojo_radio // 2
            pygame.draw.circle(
                self.screen,
                (0, 0, 0),
                (pos_x - radio // 3, pos_y - radio // 4),
                pupila_radio
            )
            pygame.draw.circle(
                self.screen,
                (0, 0, 0),
                (pos_x + radio // 3, pos_y - radio // 4),
                pupila_radio
            )

    def dibujar_hud(self):
        """Dibuja la información en pantalla"""
        # Nivel
        texto_nivel = self.font_normal.render(
            f"NIVEL {self.entorno.nivel_actual + 1}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(texto_nivel, (20, 20))

        # Puntaje
        texto_puntaje = self.font_normal.render(
            f"PUNTOS: {self.entorno.pacman.puntaje}",
            True,
            (255, 255, 0)
        )
        self.screen.blit(texto_puntaje, (20, 60))

        # Puntos restantes
        puntos_restantes = sum(1 for p in self.entorno.puntos if not p.recolectado)
        texto_restantes = self.font_pequeña.render(
            f"Restantes: {puntos_restantes}/{len(self.entorno.puntos)}",
            True,
            (200, 200, 200)
        )
        self.screen.blit(texto_restantes, (20, 100))

        # Ayuda (solo al inicio)
        if self.mostrar_ayuda and self.frame_count < 300:  # 5 segundos
            ayuda_textos = [
                "Usa las FLECHAS para mover",
                "ESPACIO para pausar",
                "ESC para salir"
            ]

            for i, texto in enumerate(ayuda_textos):
                superficie = self.font_pequeña.render(texto, True, (100, 255, 100))
                self.screen.blit(
                    superficie,
                    (self.ancho - 300, 20 + i * 30)
                )

    def dibujar_pausa(self):
        """Dibuja la pantalla de pausa"""
        # Fondo semi-transparente
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Texto "PAUSA"
        texto = self.font_grande.render("PAUSA", True, (255, 255, 0))
        rect = texto.get_rect(center=(self.ancho // 2, self.alto // 2))
        self.screen.blit(texto, rect)

        # Instrucción
        texto_continuar = self.font_pequeña.render(
            "Presiona ESPACIO para continuar",
            True,
            (255, 255, 255)
        )
        rect_continuar = texto_continuar.get_rect(
            center=(self.ancho // 2, self.alto // 2 + 60)
        )
        self.screen.blit(texto_continuar, rect_continuar)

    def dibujar_game_over(self):
        """Dibuja la pantalla de game over"""
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        if self.entorno.victoria:
            texto = self.font_grande.render("¡VICTORIA!", True, (0, 255, 0))
            mensaje = "¡Completaste todos los niveles!"
        else:
            texto = self.font_grande.render("GAME OVER", True, (255, 0, 0))
            mensaje = "Pac-Man fue atrapado"

        rect = texto.get_rect(center=(self.ancho // 2, self.alto // 2 - 40))
        self.screen.blit(texto, rect)

        texto_mensaje = self.font_normal.render(mensaje, True, (255, 255, 255))
        rect_mensaje = texto_mensaje.get_rect(center=(self.ancho // 2, self.alto // 2 + 20))
        self.screen.blit(texto_mensaje, rect_mensaje)

        texto_puntaje = self.font_normal.render(
            f"Puntaje Final: {self.entorno.pacman.puntaje}",
            True,
            (255, 255, 0)
        )
        rect_puntaje = texto_puntaje.get_rect(center=(self.ancho // 2, self.alto // 2 + 70))
        self.screen.blit(texto_puntaje, rect_puntaje)

        texto_salir = self.font_pequeña.render(
            "Presiona ESC para salir",
            True,
            (200, 200, 200)
        )
        rect_salir = texto_salir.get_rect(center=(self.ancho // 2, self.alto // 2 + 120))
        self.screen.blit(texto_salir, rect_salir)

    def manejar_eventos(self):
        """Maneja los eventos del teclado"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_SPACE:
                    self.pausa = not self.pausa

                if not self.pausa and not self.entorno.juego_terminado:
                    if event.key == pygame.K_UP:
                        self.entorno.pacman.set_direccion('up')
                    elif event.key == pygame.K_DOWN:
                        self.entorno.pacman.set_direccion('down')
                    elif event.key == pygame.K_LEFT:
                        self.entorno.pacman.set_direccion('left')
                    elif event.key == pygame.K_RIGHT:
                        self.entorno.pacman.set_direccion('right')

        return True

    def actualizar(self):
        """Actualiza la lógica del juego"""
        if self.pausa or self.entorno.juego_terminado:
            return

        self.frame_count += 1

        # Verificar tiempo de gracia
        if self.en_gracia:
            if self.frame_count >= self.tiempo_gracia:
                self.en_gracia = False
                print("⚠️  ¡Los fantasmas se activan!")

        # Actualizar Pac-Man cada X frames
        if self.frame_count % self.velocidad_pacman == 0:
            self.entorno.pacman.actualizar_movimiento_interactivo(self.entorno.obstaculos)

            # Verificar recolección de puntos
            for punto in self.entorno.puntos:
                if not punto.recolectado and self.entorno.pacman.pos == punto.pos:
                    self.entorno.pacman.recolectar_punto(punto)
                    self.entorno.puntaje = self.entorno.pacman.puntaje
                    print(f"🟡 Punto! Puntaje: {self.entorno.puntaje}")

        # ========================================
        # FANTASMAS SOLO SE ACTIVAN DESPUÉS DEL TIEMPO DE GRACIA
        # ========================================
        if not self.en_gracia:
            # Actualizar fantasmas cada X frames (más lento)
            if self.frame_count % self.velocidad_fantasma == 0:
                for fantasma in self.entorno.fantasmas:
                    if not fantasma.trayectoria or len(fantasma.trayectoria) <= 1:
                        fantasma.perseguir_pacman(
                            self.entorno.pacman.pos,
                            self.entorno.visibility_graph,
                            self.entorno.obstaculos
                        )

                    if fantasma.trayectoria and len(fantasma.trayectoria) > 1:
                        fantasma.mover_siguiente()

        # Verificar colisiones (solo después del tiempo de gracia)
        if not self.en_gracia:
            if self.entorno.pacman.verificar_colision_fantasma(self.entorno.fantasmas):
                self.entorno.juego_terminado = True
                self.entorno.victoria = False
                print("\n💀 GAME OVER")

        # Verificar victoria
        puntos_restantes = [p for p in self.entorno.puntos if not p.recolectado]
        if not puntos_restantes:
            print(f"\n🎉 ¡Nivel {self.entorno.nivel_actual + 1} completado!")
            self.entorno.nivel_actual += 1

            if self.entorno.nivel_actual >= len(self.entorno.visibility_graph.obstaculos):
                self.entorno.juego_terminado = True
                self.entorno.victoria = True
                print("\n🏆 ¡GANASTE TODO!")
            else:
                self.entorno._reiniciar_nivel()
                self.en_gracia = True  # Reiniciar tiempo de gracia
                self.frame_count = 0
                pygame.display.set_caption(f"Pac-Man IA - Nivel {self.entorno.nivel_actual + 1}")

    def dibujar(self):
        """Dibuja todos los elementos"""
        self.screen.fill(COLOR_FONDO)

        # self.dibujar_grid()  # Descomentar si quieres ver la cuadrícula
        self.dibujar_obstaculos()
        self.dibujar_puntos()
        self.dibujar_fantasmas()
        self.dibujar_pacman()
        self.dibujar_hud()

        if self.pausa:
            self.dibujar_pausa()

        if self.entorno.juego_terminado:
            self.dibujar_game_over()

        pygame.display.flip()

    def ejecutar(self):
        """Loop principal del juego"""
        print("\n" + "=" * 60)
        print("🎮 CONTROLES:")
        print("  ⬆️⬇️⬅️➡️  - Mover Pac-Man")
        print("  ESPACIO - Pausar")
        print("  ESC - Salir")
        print("=" * 60 + "\n")

        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(self.fps)

        pygame.quit()

        # Mostrar resultado final
        print("\n" + "=" * 60)
        print("RESULTADO FINAL")
        print("=" * 60)
        print(f"Estado: {'VICTORIA ✓' if self.entorno.victoria else 'DERROTA ✗'}")
        print(f"Nivel alcanzado: {self.entorno.nivel_actual + 1}")
        print(f"Puntaje final: {self.entorno.pacman.puntaje}")
        print(f"Puntos recolectados: {self.entorno.pacman.puntos_recolectados}")
        print("=" * 60 + "\n")