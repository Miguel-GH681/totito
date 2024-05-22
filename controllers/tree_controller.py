import os
import sys
import graphviz

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from tree import Tree
from node import Node
from factor import Factor
from factor_controller import FactorController

fc = FactorController()

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
    
    def find_cell(self, root, value: int):
        return self._find_cell(root, value)
    
    def _find_cell(self, root: Node, value: int):
        if root is None:
            return None
        elif value == root.value.score:
            print(root.value)
            return root
        elif value < root.value.score:
            return self._find_cell(root.left, value)
        else:
            return self._find_cell(root.right, value)
                
        
    def list_movements(self):
        self._list_movements_header(self.root)
 
    def _list_movements_header(self, root: Node):
        if root != None:
            self._list_movements_header(root.left)
            print('----------')
            self._list_movements_body(root.value.tree)
            self._list_movements_header(root.right)

    def _list_movements_body(self, root):
        if root != None:
            self._list_movements_body(root.left)
            print(root.value.score)
            self._list_movements_body(root.right) 

    def configure_cells(self, score: int, cpu: bool):
        self._configure_cells(self.root, score, cpu)
 
    def _configure_cells(self, root: Node, score: int, cpu: bool):
        if root != None:
            self._configure_cells(root.left, score, cpu)
            finded = self.find_cell(root.value.tree ,score)
            restructuring_factor = -400 if (finded != None and cpu) else (400 if (finded != None and cpu is False) else 0)
            if restructuring_factor != 0:
                fc.insert(Factor(root.value.score, restructuring_factor, finded))
            self._configure_cells(root.right, score, cpu)

    def get_nodes_found(self):
        fc.list()

    def builder(self):
        factor: Factor = 0
        while factor != None:
            factor = fc.getLast()
            if factor is not None:
                self.eliminar(factor.score)
                self.insert(Tree(factor.movements, (factor.score+(factor.factor))))
                fc.eliminar(factor.score)

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

    def _valor_minimo(self, root):
        actual = root
        while actual.left is not None:
            actual = actual.left
        return actual

    def getGraph(self):
        dot = graphviz.Digraph()
        self._getGraph(self.root, dot)

        out_file = "tree.dot"
        dot.render(out_file, format='png', cleanup=True)
        
    def _getGraph(self, root: Node, dot: graphviz.Digraph):
        if root is not None:
            dot.node(str(root.value.score), "{0}".format(root.value.score))
            if root.left is not None:
                dot.edge(str(root.value.score), str(root.left.value.score))
                self._getGraph(root.left, dot)
            if root.right is not None:
                dot.edge(str(root.value.score), str(root.right.value.score))
                self._getGraph(root.right, dot)