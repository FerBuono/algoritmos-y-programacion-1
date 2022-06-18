import random

COLORES = {
    0: '#FF0000',
    1: '#33DD33',
    2: '#334DFF',
    3: '#8000B3',
    4: '#FF8000',
    5: '#DA2071',
    6: '#EEEE00',
    7: '#C0C0C0',
    8: '#808080',
    9: '#0C0C0C'
}
BLOQUE_PPAL = 'bloque'

class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla.
        """
        self.filas = alto
        self.columnas = ancho
        self.color_ini = random.randint(0, 9)
        self.colores = []
        self.tablero = [[self.color_ini for j in range(ancho)] for i in range(alto)]


    def mezclar_tablero(self, n_colores):
        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Argumentos:
            n_colores (int): Cantidad maxima de colores a incluir en la grilla.
        """
        self.colores = [self.color_ini] + random.sample(list(filter(lambda x: x != self.color_ini, COLORES)), n_colores - 1)
        self.tablero = [[random.choice(self.colores) for col in range(len(self.tablero[0]))] for fil in range(len(self.tablero))]


    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.

        Devuelve:
            Color asignado.
        """
        return self.tablero[fil][col]


    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.
        La secuencia tendrá todos los colores posibles que fueron utilizados
        para generar el tablero, sin importar cuántos de estos colores queden
        actualmente en el tablero.

        Devuelve:
            iterable: secuencia ordenada de colores.
        """
        return sorted(self.colores)


    def dimensiones(self):
        """
        Dimensiones de la grilla (filas y columnas)

        Devuelve:
            (int, int): alto y ancho de la grilla en ese orden.
        """
        return (self.filas, self.columnas)


    def _cambiar_color(self, color_nuevo, color_viejo, f = 0, c = 0):
        """
        Chequea recursivamente si los vecinos de la casilla en tablero[f][c]
        (arrancando desde f = 0 y c = 0) son del color del bloque principal
        y las cambia al color nuevo
        """
        if f < 0 or f >= self.filas or c < 0 or c >= self.columnas:
            return
        if self.tablero[f][c] != color_viejo:
            return
        
        self.tablero[f][c] = color_nuevo

        self._cambiar_color(color_nuevo, color_viejo, f, c + 1)
        self._cambiar_color(color_nuevo, color_viejo, f, c - 1)
        self._cambiar_color(color_nuevo, color_viejo, f + 1, c)
        self._cambiar_color(color_nuevo, color_viejo, f - 1, c)


    def cambiar_color(self, color_nuevo):
        """
        Asigna el nuevo color al Flood de la grilla. Es decir, a todas las
        coordenadas que formen un camino continuo del mismo color comenzando
        desde la coordenada origen en (0, 0) se les asignará `color_nuevo`

        Argumentos:
            color_nuevo: Valor del nuevo color a asignar al Flood.
        """
        color_viejo = self.tablero[0][0]

        if self.esta_completado() or color_viejo == color_nuevo:
            return
            
        self._cambiar_color(color_nuevo, color_viejo)


    def clonar(self):
        """
        Devuelve:
            Flood: Copia del Flood actual
        """
        nuevo = Flood(self.filas, self.columnas)
        nuevo.color_ini = self.color_ini
        nuevo.colores = self.colores
        nuevo.tablero = [[num for num in fil] for fil in self.tablero]
        return nuevo


    def _casilleros_bloque(self, color, clon, f = 0, c = 0):
        """
        Chequea recursivamente si el casillero tablero[f][c] pertenece
        al bloque principal y le cambia el valor a 'bloque' para poder
        identificarlo
        """
        cant = 0

        if f < 0 or f >= clon.filas or c < 0 or c >= clon.columnas:
            return 0
        if clon.tablero[f][c] != color:
            return 0

        clon.tablero[f][c] = BLOQUE_PPAL
        cant += 1

        cant += clon._casilleros_bloque(color, clon, f, c + 1)
        cant += clon._casilleros_bloque(color, clon, f, c - 1)
        cant += clon._casilleros_bloque(color, clon, f + 1, c)
        cant += clon._casilleros_bloque(color, clon, f - 1, c)

        return cant


    def casilleros_bloque(self):
        """
        La cantidad de casilleros que ocupa el bloque principal

        Devuelve:
            int: tamaño del bloque principal
        """
        clon = self.clonar()
        color = clon.tablero[0][0]
        return self._casilleros_bloque(color, clon)
        

    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color

        Devuelve:
            bool: True si toda la grilla tiene el mismo color
        """
        color_actual = self.tablero[0][0]
        for fil in self.tablero:
            for num in fil:
                if num != color_actual:
                    return False
        return True
        
