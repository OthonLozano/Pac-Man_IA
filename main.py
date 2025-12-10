"""
Punto de entrada principal del juego Pac-Man IA
Ejecuta la simulación y muestra resultados
"""
from clases.entorno import Entorno
from visualizacion.dibujado_matplotlib import VisualizadorMatplotlib
from visualizacion.estadisticas import GeneradorEstadisticas


def main():
    # Crear el entorno
    mundo = Entorno()

    # Crear visualizador
    visualizador = VisualizadorMatplotlib(mundo)

    # Ejecutar simulación
    visualizador.iniciar_simulacion()

    # Mostrar estadísticas
    stats = GeneradorEstadisticas(mundo)
    stats.mostrar_comparacion_algoritmos()


if __name__ == "__main__":
    main()