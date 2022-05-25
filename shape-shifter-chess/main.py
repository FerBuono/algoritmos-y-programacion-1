import csv
import gamelib
import os
import random

ANCHO_TABLERO = 400
ALTO_TABLERO = 400
TAMAÑO_CASILLERO = ANCHO_TABLERO // 8
CASILLEROS = 8
SANGRIA_TEXTO = TAMAÑO_CASILLERO * 0.5
RUTA_MOVIMIENTOS = 'movimientos.csv'
RUTA_GUARDADO = 'guardado.csv'

def cargar_juego():
    juego = []
    nivel = 0

    with open(RUTA_GUARDADO) as guardado:
        for fila in csv.reader(guardado):

            for i, elemento in enumerate(fila):
                
                if len(elemento) > 0:
                    pieza, estado = elemento.split(',')
                    fila[i] = (pieza[2 : -1], estado[2 : -2])
                    nivel += 1

            juego.append(fila)

    return juego, nivel - 2

def movimientos_piezas():
    movimientos = {}

    with open(RUTA_MOVIMIENTOS) as movs:
        for linea in csv.reader(movs):
            pieza, extensible = linea[0], linea[2]
            direccion = linea[1].split(';')

            if extensible == 'true':
                for i in range(1, CASILLEROS + 1):
                    movimientos[pieza] = movimientos.get(pieza, []) + [tuple(i * int(x) for x in direccion)]
            else:
                movimientos[pieza] = movimientos.get(pieza, []) + [tuple(int(x) for x in direccion)]
    
    return movimientos


def juego_nuevo(movimientos, nivel):
    '''inicializa el estado del juego para el numero de nivel dado'''
    juego = [['' for j in range(CASILLEROS)] for i in range(CASILLEROS)]
    
    pos_x_original, pos_y_original = random.randint(0, CASILLEROS - 1), random.randint(0, CASILLEROS - 1)
    pieza_original = random.choice(list(movimientos))
    
    juego[pos_y_original][pos_x_original] = (pieza_original, 'activa')
    
    pieza = pieza_original
    pos_x, pos_y = pos_x_original, pos_y_original
    
    for i in range(1, nivel + 2):
        while True:

            dir_x, dir_y = random.choice(movimientos[pieza])

            if (pos_x + dir_x in range(CASILLEROS)) and (pos_y + dir_y in range(CASILLEROS)) and (juego[pos_y + dir_y ][pos_x + dir_x] == ''):
            
                pieza = random.choice(list(movimientos))
                pos_x, pos_y = pos_x + dir_x, pos_y + dir_y 

                juego[pos_y][pos_x] = (pieza, '')

                for direccion in movimientos[pieza_original]:
                    dir_x_original, dir_y_original = direccion

                    if (pos_x == dir_x_original + pos_x_original) and (pos_y == dir_y_original + pos_y_original):
                        juego[pos_y][pos_x] = (pieza, 'posible')
                        
                break

    with open(RUTA_GUARDADO, "w", newline = '') as guardado:
        guardado = csv.writer(guardado)
        guardado.writerows(juego)

    return juego

def juego_actualizar(movimientos, juego, x, y):
    """Actualiza el estado del juego"""
    casillero_x, casillero_y = x // TAMAÑO_CASILLERO, y // TAMAÑO_CASILLERO
    
    if casillero_x < CASILLEROS and casillero_y < CASILLEROS and juego[casillero_y][casillero_x] != '' and juego[casillero_y][casillero_x][1] == 'posible': 
        pieza, estado = juego[casillero_y][casillero_x]

        pos_x_activa, pos_y_activa = '', ''
        
        for fil in range(len(juego)):
            for col in range(len(juego[fil])):
                if juego[fil][col] != '': 
                    if juego[fil][col][1] == 'activa':
                        pos_x_activa, pos_y_activa = col, fil

                    juego[fil][col] = (juego[fil][col][0], '')

        if estado == 'posible': 
            juego[casillero_y][casillero_x] = (pieza, 'activa')
            juego[pos_y_activa][pos_x_activa] = ''

            for direccion in movimientos[pieza]:
                dir_x, dir_y = direccion

                for fil in range(len(juego)):
                    for col in range(len(juego[fil])):
                        if juego[fil][col] != '' and casillero_y + dir_y == fil and casillero_x + dir_x == col:
                            juego[fil][col] = (juego[fil][col][0], 'posible')
                            
    return juego

def juego_mostrar(juego, nivel):
    '''dibuja la interfaz de la aplicación en la ventana'''
    gamelib.draw_begin()

    gamelib.draw_rectangle(0, 0, ANCHO_TABLERO, ALTO_TABLERO + 75, fill="black")

    for casillero_x in range(CASILLEROS):
        for casillero_y in range(CASILLEROS):
            
            if (casillero_x + casillero_y) % 2 == 0:
                gamelib.draw_rectangle(casillero_x * TAMAÑO_CASILLERO + 2, casillero_y * TAMAÑO_CASILLERO + 2, TAMAÑO_CASILLERO * (casillero_x + 1) - 2, TAMAÑO_CASILLERO * (casillero_y + 1) - 2, fill='#2D2D3F')
            else:
                gamelib.draw_rectangle(casillero_x * TAMAÑO_CASILLERO + 2, casillero_y * TAMAÑO_CASILLERO + 2, TAMAÑO_CASILLERO * (casillero_x + 1) - 2, TAMAÑO_CASILLERO * (casillero_y + 1) - 2, fill='#171717')

            if juego[casillero_y][casillero_x] != '':
                pieza, estado = juego[casillero_y][casillero_x]

                if estado == 'activa':
                    gamelib.draw_image(f"img/{pieza}_rojo.gif", (casillero_x * TAMAÑO_CASILLERO) + 3, (casillero_y * TAMAÑO_CASILLERO) + 3)
                elif estado == 'posible':
                    gamelib.draw_rectangle(casillero_x * TAMAÑO_CASILLERO + 3, casillero_y * TAMAÑO_CASILLERO + 3, TAMAÑO_CASILLERO * (casillero_x + 1) - 2, TAMAÑO_CASILLERO * (casillero_y + 1) - 2, fill = '', outline = 'red', width = '2')
                    gamelib.draw_image(f"img/{pieza}_blanco.gif", (casillero_x * TAMAÑO_CASILLERO) + 3, (casillero_y * TAMAÑO_CASILLERO) + 3)
                elif estado == '':
                    gamelib.draw_image(f"img/{pieza}_blanco.gif", (casillero_x * TAMAÑO_CASILLERO) + 3, (casillero_y * TAMAÑO_CASILLERO) + 3)

    gamelib.draw_text('SHAPE SHIFTER CHESS', SANGRIA_TEXTO, ALTO_TABLERO + 15, size = 10, bold = True, anchor = 'nw')
    gamelib.draw_text(f'Nivel: {nivel}', SANGRIA_TEXTO, ALTO_TABLERO + 40, size = 10, bold = True, anchor = 'nw')
    gamelib.draw_text('Salir: Esc', SANGRIA_TEXTO + ANCHO_TABLERO // 2, ALTO_TABLERO + 15, size = 10, bold = True, anchor = 'nw')
    gamelib.draw_text('Reintentar: Z', SANGRIA_TEXTO + ANCHO_TABLERO // 2, ALTO_TABLERO + 40, size = 10, bold = True, anchor = 'nw')

    gamelib.draw_end()

def main():
    movimientos = movimientos_piezas()
    juego = []
    nivel = 0 
    cargar = ''
    
    if os.path.exists(RUTA_GUARDADO):
        while True:
            cargar = gamelib.input('¿Quiere continuar el juego guardado? (Si/No)')
            if cargar == 'Si' or cargar == 'No' or cargar == None:
                break
    else:
        cargar = 'No'

    if cargar == 'Si':
        juego, nivel = cargar_juego()
    elif cargar == 'No':
        nivel = 1
        juego = juego_nuevo(movimientos, nivel)
    else:
        return
    
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(ANCHO_TABLERO, ALTO_TABLERO + 75)

    while gamelib.is_alive():
        juego_mostrar(juego, nivel)

        ev = gamelib.wait()
        if not ev:
            break

        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            x, y = ev.x, ev.y
            juego = juego_actualizar(movimientos, juego, x, y)
                
            piezas_tablero = [juego[fil][col] for fil in range(len(juego)) for col in range(len(juego[fil])) if juego[fil][col] != '' ]
            
            if len(piezas_tablero) == 1:
                nivel += 1
                juego = juego_nuevo(movimientos, nivel)
            
        elif ev.type == gamelib.EventType.KeyPress:

            if ev.key == 'Escape':
                # Finalizar juego
                break

            if ev.key == 'z' or ev.key == 'Z':
                # Reiniciar juego
                juego, nivel = cargar_juego()

gamelib.init(main)