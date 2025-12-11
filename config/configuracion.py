"""
Configuración global del juego
"""

# Tamaño del mundo
TAMANIO_MUNDO = 20
LIMITE = TAMANIO_MUNDO // 2

# Modo de juego
MODO_INTERACTIVO = True

# Velocidades (en frames: más alto = más lento)
VELOCIDAD_PACMAN = 5  # Pac-Man se mueve cada 3 frames
VELOCIDAD_FANTASMA_BASE = 1000 # Fantasmas se mueven cada 6 frames (más lento)

# Visualización Pygame
FPS = 60  # Frames por segundo (más alto = más fluido)
ANCHO_VENTANA = 800
ALTO_VENTANA = 800

# Colores (RGB) - Estilo Pac-Man clásico
COLOR_FONDO = (0, 0, 0)  # Negro
COLOR_PACMAN = (255, 255, 0)  # Amarillo
COLOR_FANTASMA_BPA = (255, 0, 0)  # Rojo (Blinky)
COLOR_FANTASMA_GREEDY = (255, 184, 255)  # Rosa (Pinky)
COLOR_FANTASMA_A_STAR = (0, 255, 255)  # Cyan (Inky)
COLOR_FANTASMA_DIJKSTRA = (255, 165, 0)  # Naranja (Clyde)
COLOR_PUNTO = (255, 255, 255)  # Blanco
COLOR_OBSTACULO = (33, 33, 222)  # Azul oscuro

# Generación de puntos
GENERACION_ALEATORIA = True