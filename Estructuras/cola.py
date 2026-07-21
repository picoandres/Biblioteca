from Estructuras.nodo import Nodo

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None

    def esta_vacia(self):
        return self.frente is None


    def encolar(self, dato):
        nuevo = Nodo(dato)

        if self.esta_vacia():

            self.frente = nuevo
            self.final = nuevo

            return

        self.final.siguiente = nuevo
        self.final = nuevo


    def desencolar(self):
        if self.esta_vacia():
            return None

        dato = self.frente.dato

        self.frente = self.frente.siguiente

        if self.frente is None:
            self.final = None

        return dato


    def ver_frente(self):
        if self.esta_vacia():
            return None

        return self.frente.dato


    def recorrer(self):
        elementos = []

        actual = self.frente

        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos
    

    def contiene(self, condicion):
        actual = self.frente

        while actual:

            if condicion(actual.dato):
                return True

            actual = actual.siguiente

        return False