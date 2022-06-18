from flood import Flood
from pila import Pila
from cola import Cola


class JuegoFlood:
    """
    Clase para administrar un Flood, junto con sus estados y acciones
    """

    def __init__(self, alto, ancho, n_colores):
        """
        Genera un nuevo JuegoFlood, el cual tiene un Flood y otros
        atributos para realizar las distintas acciones del juego.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla del Flood.
            n_colores: Cantidad maxima de colores a incluir en la grilla.
        """
        self.flood = Flood(alto, ancho)
        self.flood.mezclar_tablero(n_colores)
        self.mejor_n_movimientos, _ = self._calcular_movimientos()
        self.n_movimientos = 0
        self.pasos_solucion = Cola()
        self.estados_deshacer = Pila()
        self.estados_rehacer = Pila()


    def cambiar_color(self, color):
        """
        Realiza la acción para seleccionar un color en el Flood, sumando a la
        cantidad de movimientos realizados y manejando las estructuras para
        deshacer y rehacer

        Argumentos:
            color (int): Nuevo color a seleccionar
        """
        clon = self.flood.clonar()
        self.estados_deshacer.apilar(clon.tablero)

        self.n_movimientos += 1
        self.flood.cambiar_color(color)

        if not self.estados_rehacer.esta_vacia():
            self.estados_rehacer = Pila()

        if not self.pasos_solucion.esta_vacia() and self.pasos_solucion.ver_frente() == color:
            self.pasos_solucion.desencolar()
        else:
            self.pasos_solucion = Cola()


    def deshacer(self):
        """
        Deshace el ultimo movimiento realizado si existen pasos previos,
        manejando las estructuras para deshacer y rehacer.
        """
        if self.estados_deshacer.esta_vacia():
            return
        
        clon = self.flood.clonar()
        self.estados_rehacer.apilar(clon.tablero)

        self.flood.tablero = self.estados_deshacer.desapilar()

        self.n_movimientos -= 1
        self.pasos_solucion = Cola()


    def rehacer(self):
        """
        Rehace el movimiento que fue deshecho si existe, manejando las
        estructuras para deshacer y rehacer.
        """
        if self.estados_rehacer.esta_vacia():
            return

        clon = self.flood.clonar()
        self.estados_deshacer.apilar(clon.tablero)
        
        self.flood.tablero = self.estados_rehacer.desapilar()

        self.n_movimientos += 1
        self.pasos_solucion = Cola()


    def _calcular_movimientos(self):
        """
        Realiza una solución de pasos contra el Flood actual (en una Cola)
        y devuelve la cantidad de movimientos que llevó a esa solución.
        
        Heurística: en cada paso seleccionar el color que más casilleros
        agrgaría al Flood actual.

        Para encontrar esta secuencia de pasos primero se crea una copia 
        del Flood actual sobre la cual se van a realizar las pruebas. Luego
        se realiza una copia "test" para contar la cantidad de casilleros
        que tendría el nuevo Flood si seleccionáramos los otros colores
        disponibles (sin incluir al actual). Finalmente, se selecciona el 
        color que más casilleros agregaría al bloque principal.

        Devuelve:
            int: Cantidad de movimientos que llevó a la solución encontrada.
            Cola: Pasos utilizados para llegar a dicha solución
        """
        pasos = Cola()
        movimientos = 0
        clon = self.flood.clonar()
        while not clon.esta_completado():
            colores_posibles = {}
            otros_colores = list(filter(lambda x: x != clon.tablero[0][0], clon.obtener_posibles_colores()))

            for color in otros_colores:
                clon_test = clon.clonar()
                clon_test.cambiar_color(color)
                colores_posibles[color] = clon_test.casilleros_bloque()

            prox_color = max(colores_posibles, key = colores_posibles.get)
            pasos.encolar(prox_color)
            movimientos += 1
            clon.cambiar_color(prox_color)

        return movimientos, pasos


    def hay_proximo_paso(self):
        """
        Devuelve un booleano indicando si hay una solución calculada
        """
        return not self.pasos_solucion.esta_vacia()


    def proximo_paso(self):
        """
        Si hay una solución calculada, devuelve el próximo paso.
        Caso contrario devuelve ValueError

        Devuelve:
            Color del próximo paso de la solución
        """
        return self.pasos_solucion.ver_frente()


    def calcular_nueva_solucion(self):
        """
        Calcula una secuencia de pasos que solucionan el estado actual
        del flood, de tal forma que se pueda llamar al método `proximo_paso()`
        """
        _, self.pasos_solucion = self._calcular_movimientos()


    def dimensiones(self):
        return self.flood.dimensiones()


    def obtener_color(self, fil, col):
        return self.flood.obtener_color(fil, col)


    def obtener_posibles_colores(self):
        return self.flood.obtener_posibles_colores()


    def esta_completado(self):
        return self.flood.esta_completado()
