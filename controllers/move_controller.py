import os
import sys
import graphviz

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from node import Node
from cell import Cell

class MoveController:
    def __init__(self):
        self.root = None

    def insert(self, value: Cell):
        self.root = self._insert(self.root, value)

    def _insert(self, root: Node, value: Cell):
        if root is None:
            return Node(value)
        elif value.score < root.value.score:
            root.left = self._insert(root.left, value)
        elif value.score > root.value.score:
            root.right = self._insert(root.right, value)
        return root
    
    def find(self, value: Cell):
        self._find(self.root, value)
    
    def _find(self, root: Node, value: Cell):
        if root is None:
            print('valor no encontrado')
            return Node(None)
        elif value.score == root.value.score:
            print('El valor encontrado es: {0}'.format(root.value.score))
            return root.value
        elif value.score < root.value.score:
            return self._find(root.left, value)
        else:
            return self._find(root.right, value)
        
    def listMoves(self):
        self._listMoves(self.root)

    def _listMoves(self, root):
        if root != None:
            self._listMoves(root.left)
            print("{0} - {1}".format(root.value.score, root.value.taken))
            self._listMoves(root.right)

    def getMoves(self):
        return self.root
    
    def clearMoves(self):
        self.root = None

    def getGraph(self, name):
        dot = graphviz.Digraph()
        self._getGraph(self.root, dot)

        out_file = name
        dot.render(out_file, format='png', cleanup=True)
        
    def _getGraph(self, root: Node, dot: graphviz.Digraph):
        if root is not None:
            dot.node(str(root.value.score), "{0} - {1}".format(root.value.score, root.value.taken))
            if root.left is not None:
                dot.edge(str(root.value.score), str(root.left.value.score))
                self._getGraph(root.left, dot)
            elif root.right is not None:
                dot.edge(str(root.value.score), str(root.right.value.score))
                self._getGraph(root.right.value, dot)
        