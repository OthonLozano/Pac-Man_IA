class Obstaculo:
    """
    Representa un obstáculo en el mapa
    """

    def __init__(self, posx: int, posy: int, tam: int):
        self.pos = [posx, posy]
        self.tam = tam

    def in_collission(self, x: int, y: int) -> bool:
        """
        Verifica si una posición (x, y) colisiona con el obstáculo
        """
        desp = self.tam / 2
        Xa, Ya = self.pos

        return (Xa - desp <= x <= Xa + desp and
                Ya - desp <= y <= Ya + desp)