"""
    Descripcion: Contiene un conjunto de celdas que forman una combinacion ganadora
    Parametros:
        tree - Arbol binario de celdas
        score - Puntuacion que recibe este conjunto de celdas
"""
class Tree:
    def __init__(self, tree, score, name):
        self.tree = tree
        self.score = score
        self.pieces = 0
        self.taken = False
        self.name = name