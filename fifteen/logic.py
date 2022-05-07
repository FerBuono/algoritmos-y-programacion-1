import random

VACIO = ""
MOVIMIENTOS = ['a', 'w', 'd', 's']
MOVIMIENTOS_RANDOM = 50

def formatear_dimensiones(dimensiones):
    '''
        Funcion que recibe las dimensiones del juego en formato numxnum y 
        devuelve ambos números por separado. Si el formato de ingreso no 
        es el indicado entonces pide que se ingresen nuevamente las dimensiones
    '''
    dimensiones_separadas = []

    while True:

        if 'x' in dimensiones:
            dimension_1, dimension_2 = dimensiones.split('x')

            if dimension_1.isdigit() and dimension_2.isdigit():
                break
        
        dimensiones = input('Ingrese dimensiones válidas (ej: 4x3): ')
        continue

    return int(dimension_1), int(dimension_2)


def crear_matriz(dimension_tablero):
    '''
        Función que recibe dos números enteros y devuelve una matriz 
        desordenada de N filas x M columnas rellenada con números del 
        1 al (N * M - 1). Para desordenarla se utiliza random.choice y
        llama a la función mover(), mandando como parámetro un movimiento
        al azar y la matriz
    '''
    N, M = formatear_dimensiones(dimension_tablero)

    num = 1
    matriz = []
    matriz_backup = []

    for fil in range(N):
        matriz.append([])
        matriz_backup.append([])

        for col in range(M):
            matriz[fil].append(num + col)
            matriz_backup[fil].append(num + col)

        num = 1 + matriz[fil][-1]
        num = 1 + matriz_backup[fil][-1]
   
    matriz[-1][-1] = VACIO
    matriz_backup[-1][-1] = VACIO
   
    for i in range(MOVIMIENTOS_RANDOM):
        mover(random.choice(MOVIMIENTOS), matriz)

    return matriz, matriz_backup


def mostrar_juego(matriz, movimientos, limite_movimientos):
    '''
        Función que recibe una matriz y la imprime con el formato indicado,
        junto con las instrucciones de juego y los movimientos
    '''
    print("\n====", "Fiften", "====")
    print('\n'.join(['  |'.join(['{:3}'.format(num) for num in fil]) for fil in matriz]))
    print("\nControles: w, a, s, d")
    print("Salir del juego: o")
    print('Movimientos realizados: ', movimientos)
    print('Movimientos restantes: ', limite_movimientos - movimientos)


def mover(direccion, matriz):
    '''
        Función que recibe una direccion (ya verificada que es válida) 
        y la matriz a alterar, y devuelve la misma pero con las posiciones
        cambiadas según el movimiento a realizar. 
        Direcciones válidas: 'a', 'w', 's, 'd'
    '''
    fil_vacio, col_vacio = ubicar_vacio(matriz)
    fil_nuevo, col_nuevo = fil_vacio, col_vacio

    if direccion == 'w':
        fil_nuevo = fil_vacio + 1
    if direccion == 's':
        fil_nuevo = fil_vacio - 1
    if direccion == 'a':
        col_nuevo = col_vacio + 1
    if direccion == 'd':
        col_nuevo = col_vacio - 1

    if (0 <= fil_nuevo <= len(matriz) - 1) and (0 <= col_nuevo <= len(matriz[fil_nuevo]) - 1):
        matriz[fil_vacio][col_vacio] = matriz[fil_nuevo][col_nuevo]
        matriz[fil_nuevo][col_nuevo] = VACIO


def ubicar_vacio(matriz):
    '''
        Función que ubica el casillero vacío en una matriz
    '''
    for fil in range(len(matriz)):
        for col in range(len(matriz[fil])):
            if matriz[fil][col] == VACIO:
                return fil, col

