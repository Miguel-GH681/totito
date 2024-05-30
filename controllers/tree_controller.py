import os
import sys
import csv
import graphviz
import cloudinary
import cloudinary.uploader

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from dotenv import load_dotenv
load_dotenv()

from cell import Cell
from tree import Tree
from node import Node
from simple_node import SimpleNode
from factor import Factor
from factor_controller import FactorController
from move_controller import MoveController

fc = FactorController()
movement_controller = MoveController()

cloudinary.config(
    cloudname = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

class TreeController:

    def __init__(self):
        self.root = None
        self.last_movement = None
        self.lost_movement = None

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
            return root
        elif value < root.value.score:
            return self._find_cell(root.left, value)
        else:
            return self._find_cell(root.right, value)

    def configure_cells(self, score: int, cpu: bool):
        self._configure_cells(self.root, score, cpu)
 
    def _configure_cells(self, root: Node, score: int, cpu: bool):
        if root != None:
            self._configure_cells(root.left, score, cpu)
            finded = self.find_cell(root.value.tree ,score)
            restructuring_factor = -self.getMaxValue() if (finded != None and cpu) else (self.getMaxValue() if (finded != None and cpu is False) else 0)
            if restructuring_factor != 0:
                pieces_played = 1 if root.value.taken == False else (root.value.pieces + 1)
                fc.insert(Factor(root.value.score, restructuring_factor, root.value.tree, pieces_played, True, root.value.name))
            if root.value.taken == False and root.value.pieces == 2:
                self.lost_movement = (root.value.score + (restructuring_factor))
            self._configure_cells(root.right, score, cpu)

    def builder(self):
        factor: Factor = 0
        is_winner = False
        while factor != None:
            factor = fc.getLast()
            if factor is not None:
                self.eliminar(factor.score)
                new_tree: Tree = Tree(factor.movements, (factor.score+(factor.factor)), factor.name) 
                new_tree.pieces = factor.pieces
                new_tree.taken = factor.taken
                self.insert(new_tree)
                fc.eliminar(factor.score)

            if factor is not None and factor.pieces == 3:
                is_winner = True
                break

        return is_winner

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
    
    def getMaxValue(self):
        return self._getMaxValue(self.root.right)
    
    def _getMaxValue(self, root):
        current = root
        while current.right is not None:
            current = current.right
        return current.value.score
    
    def get_first_cell(self, root, pos):
        current = root
        current_pos = pos
        while current.left is not None and current_pos != 0:
            current = current.left
            current_pos -= 1
        return current.value.score
    
    def get_cpu_election(self):
        if(self.root.value.taken is True):
            return None
        else:
            max_value = self.get_first_cell(self.root.value.tree, self.root.value.pieces)
            if self.compare_cells_played(max_value)[1]:
                self.root.value.pieces = 0
                self.get_last_movements(self.root.value.tree)
                tmp = fc.getFirst()
                max_value = tmp.score

            fc.root = None
            self.root.value.pieces += 1
            new_last_movement = SimpleNode(max_value)
            new_last_movement.next = self.last_movement
            self.last_movement = new_last_movement

            return [max_value, self.root.value.pieces]

    def getGraph(self, name):
        dot = graphviz.Digraph()
        self._getGraph(self.root, dot)

        out_file = name
        dot.render(out_file, format='png', cleanup=True)
        
    def _getGraph(self, root: Node, dot: graphviz.Digraph):
        if root is not None:
            dot.node(str(root.value.score), "{0} - {1}".format(root.value.name, root.value.score))
            if root.left is not None:
                dot.edge(str(root.value.score), str(root.left.value.score))
                self._getGraph(root.left, dot)
            if root.right is not None:
                dot.edge(str(root.value.score), str(root.right.value.score))
                self._getGraph(root.right, dot)

    def init_game(self):
        if self.root is None:
            dbPath = os.path.join(os.getcwd(), 'db', 'data.csv')
            with open(dbPath, 'r', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for i, row in enumerate(csv_reader):
                    movement_controller.insert(Cell(int(row['score']), row['taken']))
                    if( ((i+1)%3) == 0):
                        moves = movement_controller.getMoves()
                        movement_score = (i * 1)
                        self.insert(Tree(moves, movement_score, movement_score))
                        movement_controller.getGraph("{0}".format(movement_score))
                        movement_controller.clearMoves()

    def get_cpu_movement(self, cell: int, first_player: bool):
        self.configure_cells(cell, first_player)
        is_winner = self.builder()
        if is_winner:
            print("felicidades ha ganado 'X'")
            return [True, -1]
        else:
            pc_election = self.get_cpu_election()
            if pc_election != None:
                print('Eleccion de la pc: ', pc_election[0])
                if pc_election[1] == 3:
                    print("Felicidades ha ganado 'O'")
                    return [True, pc_election[0]]            
                return [False, pc_election[0]]
            else:
                return [False, -1]
        
    def clear_data(self):
        self.last_movement = None
        self._clear_data(self.root)
        self._builder()
        self.clear_lost_movement(self.lost_movement)
        self.lost_movement = None

    def _clear_data(self, root):
        if root != None:
            self._clear_data(root.left)
            fc.insert(Factor(root.value.score, 0, root.value.tree, 0, False, root.value.name))
            self._clear_data(root.right)

    def _builder(self):
        factor: Factor = 0
        while factor != None:
            factor = fc.getLast()
            if factor is not None:
                self.eliminar(factor.score)
                new_tree: Tree = Tree(factor.movements, (factor.score+(factor.factor)), factor.name) 
                new_tree.pieces = factor.pieces
                new_tree.taken = factor.taken
                self.insert(new_tree)
                fc.eliminar(factor.score)

    def clear_lost_movement(self, score):
        self._clear_data_2(self.root, score)
        factor: Factor = 0
        while factor != None:
            factor = fc.getLast()
            print("Mi factor: {0}".format(factor))
            if factor is not None:
                self.eliminar(factor.score)
                new_tree: Tree = Tree(factor.movements, (factor.score+(factor.factor)), factor.name)
                new_tree.pieces = factor.pieces
                new_tree.taken = factor.taken
                self.insert(new_tree)
                fc.eliminar(factor.score)


    def _clear_data_2(self, root, score):
        if root != None:
            self._clear_data_2(root.left, score)
            if root.value.score == score:
                fc.insert(Factor(root.value.score, self.getMaxValue(), root.value.tree, 0, False, root.value.name))
            self._clear_data_2(root.right, score)

    def compare_cells_played(self, value):
        current = self.last_movement
        exists = False

        while current:
            if value == current.value:
                self.root.value.pieces += 1
                exists = True
                break
            else:
                current = current.next
            
        return [value, exists]

    def get_last_movements(self, root):
        if root != None:
            self.get_last_movements(root.left)
            value = self.compare_cells_played(root.value.score)
            if value[1] is False:
                print(value[0])
                fc.insert(Factor(value[0], None, None, None, None, None))
            self.get_last_movements(root.right)

    def get_last_movement(self, value):
        current = self.last_movement
        exists = False

        while current:
            if value == current.value:
                self.root.value.pieces += 1
                print(self.root.value.pieces)
            current = current.next

        return exists
    
    def upload_images(self, name):
        response = cloudinary.uploader.upload(name)
        return response["secure_url"]