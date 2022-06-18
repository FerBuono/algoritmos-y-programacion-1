class ListaEnlazada:

    def remover_todos(self, elem):
        '''
        Remueve de la lista todas las apariciones del elemento, y devuelve
        la cantidad de eliminados
        '''
        cant = 0
        ant = None
        act = self.prim
        while act:
            if act.dato == elem:
                if ant:
                    ant.prox = act.prox
                    cant += 1
                    self.cant -= 1
                else:
                    self.prim = act.prox
                    cant += 1
                    self.cant -= 1
            else:
                ant = act

            act = act.prox
        return cant
    
    def __str__(self):
        res = '['
        act = self.prim
        while act:
            res += f'{act.dato}'
            if act.prox:
                res += ', '
            act = act.prox
        return res + ']'


    def __init__(self):
        # prim es un _Nodo o None
        self.prim = None
        self.cant = 0

    def append(self, dato):
        nuevo = _Nodo(dato)
        if not self.prim:
            self.prim = nuevo
        else:
            act = self.prim
            while act.prox:
                act = act.prox
            # act es el ultimo nodo
            act.prox = nuevo
        self.cant += 1

    def __len__(self):
        return self.cant

class _Nodo:
    def __init__(self, dato, prox=None):
        self.dato = dato
        self.prox = prox

