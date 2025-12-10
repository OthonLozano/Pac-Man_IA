"""
Configuración global del juego
"""

# Tamaño del mundo
TAMANIO_MUNDO = 20
LIMITE = TAMANIO_MUNDO // 2

# Velocidades (frames entre movimientos)
VELOCIDAD_PACMAN = 2
VELOCIDAD_FANTASMA = 3

# Visualización
FPS = 30
ANCHO_VENTANA = 800
ALTO_VENTANA = 800

# Colores (RGB)
COLOR_FONDO = (0, 0, 0)
COLOR_PACMAN = (255, 255, 0)
COLOR_FANTASMA_BPA = (255, 0, 0)
COLOR_FANTASMA_GREEDY = (255, 100, 150)
COLOR_FANTASMA_A_STAR = (0, 255, 255)
COLOR_PUNTO = (255, 255, 255)
COLOR_OBSTACULO = (100, 100, 100)
COLOR_CAMINO = (0, 255, 0)

# Obstáculos (posiciones predefinidas)
OBSTACULOS = [
    (7, 5, 2),   # (x, y, tamaño)
    (0, 2, 2),
    (5, 0, 2),
    (-5, -5, 3),
]

# Puntos (generación)
NUMERO_PUNTOS = 15
GENERACION_ALEATORIA = True