from logic import formatear_dimensiones, crear_matriz, mostrar_juego, mover, randomizar_matriz

def main():
    '''
        FIFTEEN: Es un sencillo juego donde el objetivo es ordenar todos los números de izquierda a derecha y de arriba a abajo dado un tablero de dimensiones NxM el cual siempre tiene un casillero vacío. Para ello el jugador puede mover las fichas en diferentes direcciones, usando siempre el espacio vacío.

        Finalmente, el juego se considera ganado si todos los elementos están ordenados de izquierda a derecha, con el vacío ubicado en el vértice inferior derecho.

        Direcciones válidas: 'a', 'w', 's, 'd'
        Para finalizar el juego: 'o'
    '''

    # Ingreso las dimensiones del juego
    dimension_tablero = input('\nIngrese las dimensiones del tablero (ej: 4x3): ')

    # Dimensiones separadas en filas y columnas
    filas, columnas = formatear_dimensiones(dimension_tablero)

    # Creación de 2 matrices, con una se juega y la otra se guarda para el chequeo final
    matriz_juego = crear_matriz(filas, columnas)
    matriz_backup = crear_matriz(filas, columnas)

    # 'Randomizado' de la matriz de juego 
    randomizar_matriz(matriz_juego)
    
    # Mostrar tablero inicial
    mostrar_juego(matriz_juego)
    
    # Variable en donde se guardan los movimientos realizados en la partida
    movimientos = 0

    # Verifico que mientras la matriz de juego sea distinta a la de backup y el jugador quiera seguir jugando, se le pida un nuevo movimiento. Este tiene que ser valido y de no ser así se le solicita una nueva entrada. Se muestra en cada entrada válida el tablero nuevamente
    while matriz_juego != matriz_backup:
        entradas = input('Entrada/s: ')
        entradas_separadas = list(entradas)
        for entrada in entradas_separadas:
            if entrada not in ['a', 'w', 'd', 's', 'o']:
                entradas = input('Por favor, ingrese entradas válidas: ')
            if entrada == 'o':
                print('\nJuego finalizado :(\n')
                return
            
            mover(entrada, matriz_juego)
            movimientos += 1

        mostrar_juego(matriz_juego)
        print('Movimientos realizados: ', movimientos)
        
    print('\n¡GANASTE!\n')

main()