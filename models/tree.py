"""
    Descripcion: Contiene un conjunto de celdas que forman una combinacion ganadora
    Parametros:
        tree - Arbol binario de celdas
        score - Puntuacion que recibe este conjunto de celdas
"""
class Tree:
    def __init__(self, tree, score):
        self.tree = tree
        self.score = score