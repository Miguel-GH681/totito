import os
import sys
import graphviz

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from tree import Tree
from node import Node

class TreeController:

    def __init__(self):
        self.root = None

    def insert(self, value : Tree):
        self.root = self._insert(self.root, value)

    def _insert(self, root : Node, value : Tree):
        if root is None:
            return Node(value)
        elif value.score < root.value.score:
            root.left = self._insert(root.left, value)
        elif value.score > root.value.score:
            root.right = self._insert(root.right, value)
        return root
    
    def find(self, value: int):
        self._find(self.root, value)
    
    def _find(self, root: Node, value: int):
        if root is None:
            print('valor no encontrado')
            return Node(None)
        elif value == root.value.score:
            print('El valor encontrado es: {0}'.format(root.value.tree))
            return root.value.score
        elif value < root.value.score:
            return self._find(root.left, value)
        else:
            return self._find(root.right, value)
        
    def list(self):
        self._list(self.root)

    def _list(self, root: Node):
        if root != None:
            self._list(root.left)
            print(root.value.tree.value.score)
            self._list2(root.value.tree)
            self._list(root.right)

    def _list2(self, root):
        if root != None:
            self._list2(root.left)
            print(root.value.score)
            self._list2(root.right)
    

    def getGraph(self):
        dot = graphviz.Digraph()
        self._getGraph(self.root, dot)

        out_file = "tree.dot"
        dot.render(out_file, format='png', cleanup=True)
        
    def _getGraph(self, root: Node, dot: graphviz.Digraph):
        if root is not None:
            dot.node(str(root.value.score))
            if root.left is not None:
                dot.edge(str(root.value.score), str(root.left.value.score))
                self._getGraph(root.left, dot)
            if root.right is not None:
                dot.edge(str(root.value.score), str(root.right.value.score))
                self._getGraph(root.right, dot)