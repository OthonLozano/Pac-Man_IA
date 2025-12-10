"""
Genera gráficas comparativas de los algoritmos
"""
import matplotlib.pyplot as plt


class GeneradorEstadisticas:
    def __init__(self, entorno):
        self.entorno = entorno

    def mostrar_comparacion_algoritmos(self):
        """Muestra gráficas comparando los algoritmos"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Gráfica 1: Nodos visitados
        # Gráfica 2: Tiempo de cálculo
        # Gráfica 3: Longitud de camino
        # Gráfica 4: Eficiencia

        plt.tight_layout()
        plt.show()