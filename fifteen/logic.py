import random

VACIO = ""
MOVIMIENTOS = ['a', 'w', 'd', 's']


def formatear_dimensiones(dimensiones):
    '''
        Funcion que recibe las dimensiones del juego en formato numxnum y 
        devuelve ambos números por separado. Si el formato de ingreso no 
        es el indicado entonces pide que se ingresen nuevamente las dimensiones
    '''
    dimensiones_validas = False
    dimensiones_separadas = []

    while dimensiones_validas == False:

        if 'x' not in dimensiones:
            dimensiones = input('Ingrese dimensiones válida (ej: 4x3): ')
            continue

        dimensiones_separadas = (dimensiones.split('x'))

        if not dimensiones_separadas[0].isdigit() or not dimensiones_separadas[1].isdigit():
            dimensiones = input('Ingrese dimensiones válida (ej: 4x3): ')
            continue
    
        dimensiones_validas = True

    return int(dimensiones_separadas[0]), int(dimensiones_separadas[1])
        
def randomizar_matriz(matriz, movimientos_random):
    '''
        Función que altera el órden de los elementos de una matriz.
        Utiliza el módulo random para generar números al azar entre
        0 y la cantidad de movimientos posibles menos 1, y llama a 
        la función mover() mandando como parámetros el movimiento 
        dado por el número random, y la matriz a alterar
    '''
    for i in range(movimientos_random):
        random_num = random.randint(0, len(MOVIMIENTOS) - 1)
        mover(MOVIMIENTOS[random_num], matriz)
    
    return matriz

def crear_matriz(N, M, movimientos_random):
    '''
        Función que recibe dos números enteros y devuelve una matriz 
        de N filas x M columnas rellenada con números del 1 al (N * M - 1)
    '''
    num = 1
    matriz = []

    for fil in range(N):
        matriz.append([])

        for col in range(M):
            matriz[fil].append(num + col)

        num = 1 + matriz[fil][-1]
   
    matriz[-1][-1] = VACIO
   
    return randomizar_matriz(matriz, movimientos_random)


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


def juego(matriz_juego, matriz_backup, movimientos, limite_movimientos):
    '''
        Funcion que verifica que mientras la matriz de juego sea distinta 
        a la de backup y el jugador quiera seguir jugando, se le pida un 
        nuevo movimiento y se matiene el estado del juego como 'Jugando'. 
        El movimiento tiene que ser valido y de no ser así se le solicita 
        una nueva entrada. Se muestra en cada entrada válida el tablero nuevamente. 
        En caso de perder, finalizar el juego o ganar, cambia el estado del juego a:
        'Perdiste', 'Juego finalizado' o 'Ganaste', respectivamente
    '''
    while (matriz_juego != matriz_backup) and (movimientos < limite_movimientos):
        entradas = input('Entrada/s: ')

        for entrada in entradas:
            while entrada not in MOVIMIENTOS + ['o']:
                entrada = input('"' + entrada + '" no es válida, intente nuevamente: ')

            if entrada == 'o':
                mostrar_juego(matriz_juego, movimientos, limite_movimientos)
                return 'Juego finalizado'
            
            mover(entrada, matriz_juego)
            movimientos += 1

            if movimientos >= limite_movimientos:
                mostrar_juego(matriz_juego, movimientos, limite_movimientos)
                return 'Perdiste'

        mostrar_juego(matriz_juego, movimientos, limite_movimientos)
    
    return 'Ganaste'
    