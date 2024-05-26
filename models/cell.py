"""
    Descripcion: Contiene la informacion de una celda en el tablero del totito
    Parametros:
        score - Puntuacion que tiene la celda
        x - Coordenada en el eje x
        y - Coordenada en el eje y
        taken - Tipo de ficha que ocupa la celda ('X' u 'O')
"""
class Cell:
    def __init__(self, score, taken):
        self.score = score
        self.taken = taken