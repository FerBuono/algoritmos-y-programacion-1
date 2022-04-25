from logic import formatear_dimensiones, crear_matriz, mostrar_juego, juego

MOVIMIENTOS_RANDOM = 50

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

    filas, columnas = formatear_dimensiones(dimension_tablero)

    matriz_juego = crear_matriz(filas, columnas, MOVIMIENTOS_RANDOM)
    # Matriz backup con la que comparar si gana o no
    matriz_backup = crear_matriz(filas, columnas, 0)

    # Mostrar juego inicial
    mostrar_juego(matriz_juego, movimientos, limite_movimientos)

    estado_de_juego = 'Jugando'

    # Si el estado es 'Jugando', se sigue jugando
    while estado_de_juego == 'Jugando':
        estado_de_juego = juego(matriz_juego, matriz_backup, movimientos, limite_movimientos)

    if estado_de_juego == 'Ganaste':
        print('\n¡GANASTE!\n')
        return
    elif estado_de_juego == 'Perdiste':
        print('\nPerdiste :(\n')
        return
    else:
        print('\nJuego finalizado :(\n')
        return


main()