from factor import Factor
from node import Node

class FactorController:
    def __init__(self):
        self.root = None

    def insert(self, value: Factor):
        self.root = self._insert(self.root, value)

    def _insert(self, root: Node, value: Factor):
        if root is None:
            return Node(value)
        elif value.score < root.value.score:
            root.left = self._insert(root.left, value)
        elif value.score > root.value.score:
            root.right = self._insert(root.right, value)
        return root
    
    def getFirst(self):
        return self._get_first(self.root)
    
    def _get_first(self, root: Node):
        if root:
            actual:Node = root
            while actual.right is not None:
                actual = actual.right
            return actual.value
        else:
            return None

    def getLast(self):
        return self._getLast(self.root)

    def _getLast(self, root: Node):
        if root:
            actual:Node = root
            while actual.left is not None:
                actual = actual.left
            return actual.value
        else:
            return None
    
    def eliminar(self, valor):
        self.root = self._eliminar(self.root, valor)

    def _eliminar(self, root, valor: int):
        if root is None:
            return root

        if valor < root.value.score:
            root.left = self._eliminar(root.left, valor)
        elif valor > root.value.score:
            root.right = self._eliminar(root.right, valor)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            
            temp = self._valor_minimo(root.right)
            root.value.score = temp.value.score
            root.right = self._eliminar(root.right, temp.value.score)
        return root
