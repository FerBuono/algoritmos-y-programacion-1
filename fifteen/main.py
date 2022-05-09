from logic import formatear_dimensiones, crear_matriz, mostrar_juego, mover, MOVIMIENTOS_RANDOM, MOVIMIENTOS


def main():
    '''
        FIFTEEN: Es un sencillo juego donde el objetivo es ordenar todos los números 
        de izquierda a derecha y de arriba a abajo dado un tablero de dimensiones NxM 
        el cual siempre tiene un casillero vacío. Para ello el jugador puede mover las 
        fichas en diferentes direcciones, usando siempre el espacio vacío.

        Finalmente, el juego se considera ganado si todos los elementos están ordenados
         de izquierda a derecha, con el vacío ubicado en el vértice inferior derecho.

        Direcciones válidas: 'a', 'w', 's, 'd'
        Para finalizar el juego: 'o'
    '''
    movimientos = 0
    limite_movimientos = MOVIMIENTOS_RANDOM * 5

    dimension_tablero = input('\nIngrese las dimensiones del tablero (ej: 4x3): ')

    matriz_juego, matriz_backup = crear_matriz(dimension_tablero)

    # Mostrar juego inicial
    mostrar_juego(matriz_juego, movimientos, limite_movimientos)

    # Mientras no esté finalizado, seguir solicitando entradas
    while (matriz_juego != matriz_backup) and (movimientos < limite_movimientos):
        entradas = input('Entrada/s: ')

        for entrada in entradas:
            while entrada not in MOVIMIENTOS + ['o']:
                entrada = input('"' + entrada + '" no es válida, intente nuevamente: ')

            if entrada == 'o':
                mostrar_juego(matriz_juego, movimientos, limite_movimientos)
                print('\nJuego finalizado...\n')
                return
            
            mover(entrada, matriz_juego)
            movimientos += 1

            if movimientos >= limite_movimientos:
                mostrar_juego(matriz_juego, movimientos, limite_movimientos)
                print('\nPerdiste :(\n')
                return

        mostrar_juego(matriz_juego, movimientos, limite_movimientos)
    
    print('\n¡¡Ganaste!!\n')
    return

main()