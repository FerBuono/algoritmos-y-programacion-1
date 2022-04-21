import random

def formatear_dimensiones(dimensiones):
    '''
        Funcion que recibe las dimensiones del juego en formato numxnum y devuelve ambos números por separado. Si el formato de ingreso no es el indicado entonces pide que se ingresen nuevamente las dimensiones
    '''
    if 'x' not in dimensiones:
        return formatear_dimensiones(input('Ingrese dimensiones válida (ej: 4x3): '))

    dimensiones_separadas = (dimensiones.split('x'))

    for dimension in dimensiones_separadas:
        if dimension.isdigit() == False:
            return formatear_dimensiones(input('Ingrese dimensiones válida (ej: 4x3): '))

    return int(dimensiones_separadas[0]), int(dimensiones_separadas[1])
        

def crear_matriz(N, M):
    '''
        Función que recibe dos números enteros y devuelve una matriz de N filas x M columnas rellenada con números del 1 al (N * M - 1)
    '''
    num = 1
    matriz = []

    for fil in range(N):
        matriz.append([])

        for col in range(M):
            matriz[fil].append(num + col)

        num = 1 + matriz[fil][-1]
   
    matriz[-1][-1] = ""
   
    return matriz


def mostrar_juego(matriz):
    '''
        Función que recibe una matriz y la imprime con el formato indicado, junto con las instrucciones de juego
    '''
    print("\n====", "Fiften", "====")
    # for fil in matriz:
    #     for col in fil:
    #         if(col == fil[0]):
    #             print(str(col).rjust(3), ' |', end='')
    #         elif(col == fil[-1]):
    #             print('  | ', str(col).ljust(3), '\n')
    #         else:
    #             print(str(col).rjust(3).ljust(3), end='')
    print('\n'.join(['  |'.join(['{:3}'.format(num) for num in fil]) for fil in matriz]))
    print("\nControles: w, a, s, d")
    print("Salir del juego: o")


def mover(direccion, matriz):
    '''
        Función que recibe una direccion (ya verificada que es válida) y la matriz a alterar, y devuelve la misma pero con las posiciones cambiadas según el movimiento a realizar. Direcciones válidas: 'a', 'w', 's, 'd'
    '''
    for fil in range(len(matriz)):
        for col in range(len(matriz[fil])):
            if matriz[fil][col] == "":
                if direccion == 'w' and fil != (len(matriz) - 1):
                    matriz[fil][col] = matriz[fil + 1][col]
                    matriz[fil + 1][col] = ""
                    return
                if direccion == 's' and fil != 0:
                    matriz[fil][col] = matriz[fil - 1][col]
                    matriz[fil - 1][col] = ""
                    return
                if direccion == 'a' and col != (len(matriz[fil]) - 1):
                    matriz[fil][col] = matriz[fil][col + 1]
                    matriz[fil][col + 1] = ""
                    return
                if direccion == 'd' and col != 0:
                    matriz[fil][col] = matriz[fil][col - 1]
                    matriz[fil][col - 1] = ""
                    return


def randomizar_matriz(matriz, Z):
    '''
        Función que altera el órden de los elementos de una matriz. Utiliza el módulo random para generar números al azar entre 0 y la cantidad de movimientos posibles menos 1, y llama a la función mover() mandando como parámetros el movimiento dado por el número random, y la matriz a alterar
    '''
    movimientos = ['a', 'w', 'd', 's']
    for i in range(Z):
        random_num = random.randint(0, len(movimientos) - 1)
        mover(movimientos[random_num], matriz)
