import gamelib

ANCHO_VENTANA = 300
ALTO_VENTANA = 300
TAMAÑO_CASILLERO = ANCHO_VENTANA // 10
CASILLEROS = 10


def juego_crear():
    """Inicializar el estado del juego"""
    grilla_juego = [['' for j in range(CASILLEROS)] for i in range(CASILLEROS)]
    return grilla_juego


def juego_actualizar(juego, x, y, turno):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    casillero_x, casillero_y = x // TAMAÑO_CASILLERO, y // TAMAÑO_CASILLERO

    if casillero_x < CASILLEROS and casillero_y < CASILLEROS and juego[casillero_y][casillero_x] == '':
        if turno % 2 == 0:
            juego[casillero_y][casillero_x] = 'O'
        else:
            juego[casillero_y][casillero_x] = 'X'
        turno += 1
    return juego, turno


def juego_mostrar(juego, turno):
    """Actualizar la ventana"""
    for casillero_x in range(CASILLEROS):
        gamelib.draw_line(casillero_x * TAMAÑO_CASILLERO, 0, casillero_x * TAMAÑO_CASILLERO, ALTO_VENTANA)
        for casillero_y in range(CASILLEROS):
            gamelib.draw_line(0, casillero_y * TAMAÑO_CASILLERO, ANCHO_VENTANA, casillero_y * TAMAÑO_CASILLERO)
            gamelib.draw_text(juego[casillero_x][casillero_y], TAMAÑO_CASILLERO * (casillero_y + 0.5), TAMAÑO_CASILLERO * (casillero_x + 0.5))
    gamelib.draw_line(0, ALTO_VENTANA, ANCHO_VENTANA, ALTO_VENTANA)
    
    if turno % 2 == 0:
        gamelib.draw_text('Turno: O', ANCHO_VENTANA // 2, ALTO_VENTANA + 25)
    else:
        gamelib.draw_text('Turno: X', ANCHO_VENTANA // 2, ALTO_VENTANA + 25)


def main():
    juego = juego_crear()
    turno = 0
    # Ajustar el tamaño de la ventana
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA + 50)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego, turno)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego, turno = juego_actualizar(juego, x, y, turno)

gamelib.init(main)