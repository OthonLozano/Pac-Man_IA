"""
Pac-Man con IA - Modo Pygame
"""
from clases.entorno import Entorno
from visualizacion.juego_pygame import JuegoPygame
from config.niveles import NIVELES

def main():
    print("="*60)
    print("PAC-MAN CON IA COMPETITIVA")
    print("="*60)
    print("\nModo: JUGADOR vs IA")
    print("Tú controlas a Pac-Man con las flechas")
    print("Los fantasmas usan diferentes algoritmos de IA\n")

    # Crear entorno del juego
    mundo = Entorno(nivel=0, modo_interactivo=True)

    print(f"✓ {len(NIVELES)} niveles disponibles")
    print(f"✓ {len(mundo.fantasmas)} fantasmas con IA")
    print(f"✓ {len(mundo.puntos)} puntos en el nivel 1")
    print(f"✓ Grafo de visibilidad: {len(mundo.visibility_graph.grafo)} nodos\n")

    # Crear y ejecutar juego
    juego = JuegoPygame(mundo)
    juego.ejecutar()

if __name__ == "__main__":
    main()