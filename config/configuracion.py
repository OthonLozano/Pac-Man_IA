"""
Configuración global del juego
"""

# Tamaño del mundo
TAMANIO_MUNDO = 20
LIMITE = TAMANIO_MUNDO // 2

# Modo de juego
MODO_INTERACTIVO = True

# Velocidades (en frames: más alto = más lento)
VELOCIDAD_PACMAN = 5  # Pac-Man se mueve cada 5 frames
VELOCIDAD_FANTASMA_BASE = 1000  # Fantasmas se mueven cada 1000 frames (muy lento)

# Visualización Pygame
FPS = 60  # Frames por segundo
ANCHO_VENTANA = 800
ALTO_VENTANA = 800

# Colores (RGB) - Estilo Pac-Man clásico
COLOR_FONDO = (0, 0, 0)  # Negro
COLOR_PACMAN = (255, 255, 0)  # Amarillo

# Colores de fantasmas según algoritmo/método
COLOR_FANTASMA_BPA = (255, 0, 0)  # Rojo (Blinky) - BPA + Visibility
COLOR_FANTASMA_GREEDY = (255, 184, 255)  # Rosa (Pinky) - Greedy + Visibility
COLOR_FANTASMA_A_STAR = (0, 255, 255)  # Cyan (Inky) - A* + Visibility
COLOR_FANTASMA_DIJKSTRA = (255, 165, 0)  # Naranja (Clyde) - A* + Voronoi
COLOR_FANTASMA_VORONOI_GREEDY = (0, 255, 100)  # Verde - Greedy + Voronoi

COLOR_PUNTO = (255, 255, 255)  # Blanco
COLOR_OBSTACULO = (33, 33, 222)  # Azul oscuro

# ============================================
# VISUALIZACIÓN DE GRAFOS DE PLANIFICACIÓN
# ============================================

# Visibility Graph (caminos óptimos)
MOSTRAR_VISIBILITY_GRAPH = False  # Cambiar a True para visualizar
COLOR_VG_NODO = (0, 200, 100)  # Verde claro
COLOR_VG_LINEA = (0, 100, 50)  # Verde oscuro

# Diagrama de Voronoi (caminos seguros)
MOSTRAR_VORONOI = False  # Cambiar a True para visualizar
COLOR_VORONOI_NODO = (100, 100, 150)  # Gris azulado
COLOR_VORONOI_LINEA = (60, 60, 90)  # Gris oscuro

# Generación de puntos
GENERACION_ALEATORIA = True