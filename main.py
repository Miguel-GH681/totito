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
movement_controller = MoveController()

def main():

    option = 0
    while option != 6:
        os.system('clear')
        print('---------------------')
        print('|    Menú principal  |')
        print('| 1. Carga inicial   |')
        print('| 2. Recorrido mov.  |')
        print('| 4. Jugar           |')
        print('| 5. Eliminar        |')
        print('| 6. Salir           |')
        print('---------------------')
        option = int(input('Ingrese una opción: '))
        
        if option == 1:
            try:
                dbPath = os.path.join(os.getcwd(), 'db', 'data.csv')
                with open(dbPath, 'r', newline='') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):
                        movement_controller.insert(Cell(int(row['score']), row['taken']))
                        if( ((i+1)%3) == 0):
                            moves = movement_controller.getMoves()
                            movement_score = (i * 100)
                            treeController.insert(Tree(moves, movement_score, movement_score))
                            movement_controller.getGraph("{0}".format(movement_score))
                            movement_controller.clearMoves()
                treeController.getGraph("tree.dot")
                input('Presione enter para continuar')
            except:
                print('Ha ocurrido un error, inténtelo nuevamente')
                input('Presione enter para continuar')
        elif option == 2:
            treeController.list_movements()
            input('Presione enter para continuar')
        elif option == 4:
            jugada = int(input("Ingrese su casilla: "))
            treeController.configure_cells(jugada, False)
            is_winner = treeController.builder()
            if is_winner:
                print("felicidades ha ganado 'X'")
                treeController.clear_data()

            else:
                pc_election = treeController.getFirstValue()
                print('Eleccion de la pc: ', pc_election[0])
                if pc_election[1] == 3:
                    print("Felicidades ha ganado 'O'")
                    treeController.clear_data()
            
            treeController.getGraph("tree.dot")
            input('Presione enter para continuar')
        elif option == 5:
            treeController.eliminar(1400)
            treeController.getGraph("tree.dot")
            input('Presione enter para continuar')
        elif option == 6:
            print('Cerrando programa...')
        else:
            print('Ingrese una opción válida')
            input('Presione enter para continuar')

if __name__ == "__main__":
    main()
