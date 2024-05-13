import os
import sys
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from cell import Cell
from tree import Tree
from move_controller import MoveController
from tree_controller import TreeController

treeController = TreeController()
moveController = MoveController()

def main():

    option = 0
    while option != 2:
        os.system('clear')
        print('---------------------')
        print('|    Menú principal  |')
        print('| 1. Carga inicial   |')
        print('| 2. Salir           |')
        print('---------------------')
        option = int(input('Ingrese una opción: '))
        
        if option == 1:
            try:
                myPath = os.path.join(os.getcwd(), 'db', 'data.csv')
                with open(myPath, 'r', newline='') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for i, row in enumerate(csv_reader):
                        moveController.insert(Cell(int(row['score']), row['taken'], int(row['x']), int(row['y'])))
                        if( ((i+1)%3) == 0):
                            moves = moveController.getMoves()
                            score = (i * 10)
                            treeController.insert(Tree(moves, score))
                            moveController.clear()
                treeController.getGraph()
                input('Presione enter para continuar')
            except:
                print('Ha ocurrido un error, inténtelo nuevamente')
                input('Presione enter para continuar')
        elif option == 2:
            print('Cerrando programa...')
        else:
            print('Ingrese una opción válida')
            input('Presione enter para continuar')

if __name__ == "__main__":
    main()
