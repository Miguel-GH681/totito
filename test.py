import math

board = [] #Nuestro tablero inicialmente seran nuevas casillas vacias
# inicializar el tablero
for i in range(9):
    board.append(' ')
TABLERO_FILAS = 3
TABLERO_COLUMNAS = 3

def getBoard():
    pos = 0
    for row in range(3):
        for column in range(3):
            print(board[pos], end=' ')
            pos += 1
        print()

def getCoordinate(literal, lower, upper):
    while True:
        value = input(literal)
        while(not value.isnumeric()):
            print('Solo se adminten valores entre {0} y {1}'.format(lower, upper))
            value = input(literal)
        coordinate = int(value)
        if(coordinate >= lower and coordinate <= upper):
            return coordinate
        else:
            print('Valor fuera del rango')

# Coloca una ficha en el tablero
def setChip(chip):
    print("Ingresa las coordenadas de tu ficha")
    while True:
        row = getCoordinate("Fila: ", 1, 3)-1
        column = getCoordinate("Columna: ", 1, 3)-1
        # Como mi tablero es de 3x3
        cell = row*3+column
        if(board[cell]!=' '):
            #Esa casilla ya esta cubierta
            print('La casilla esta ocupada')
        else:
            board[cell]=chip
            return cell


def noSiblings(cell, chip, h, v):
    f = math.floor(cell/TABLERO_COLUMNAS)
    c= cell % TABLERO_COLUMNAS
    new_row = f + v #1
    if(new_row < 0 or new_row >= TABLERO_FILAS):
        return 0

    new_column = c + h
    if(new_column < 0 or new_column >= TABLERO_COLUMNAS):
        return 0

    pos = (new_row*TABLERO_COLUMNAS + new_column)
    if (board[pos] != chip):
        return 0
    else:
        return 1 + noSiblings(pos, chip, v, h)
    
def numeroHermanos(cell, chip):
    position = cell
    if( (cell%2) == 0 ):
        position = 0
        


def checkWinner(cell, chip):
    siblings = noSiblings(cell, chip, -1, -1)+1+noSiblings(cell, chip, 1,1)
    if(siblings == 2):
        return True
    siblings = noSiblings(cell, chip, 1, -1)+noSiblings(cell, chip, -1, 1)
    if(siblings == 2):
        return True
    siblings = noSiblings(cell, chip, -1, 0)+noSiblings(cell, chip, 1, 0)
    if(siblings == 2):
        return True
    siblings = noSiblings(cell, chip, 0, -1)+noSiblings(cell, chip, 0, 1)
    if(siblings == 2):
        return True
    

# Iniciamos el juego
continue_playing = True
chips_in_play = 0

players = []
players.append(input("Nombre del jugador 1: "))
players.append(input("Nombre del jugador 2: "))

while continue_playing:
    # Pedimos fichas
    getBoard()
    player = (chips_in_play & 1)
    chip = 'X' if player==1 else 'O'
    cell = setChip(chip)
    if(checkWinner(cell, chip)):
        continue_playing = False
        print(players[player], 'Has ganado!!!')
    chips_in_play += 1
    if(chips_in_play == 9):
        continue_playing = False

getBoard()