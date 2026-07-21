from Estructuras.nodo import Nodo

class Pila:

    def __init__(self):
        self.tope = None


    def esta_vacia(self):
        return self.tope is None


    def push(self, dato):

        nuevo = Nodo(dato)

        nuevo.siguiente = self.tope

        self.tope = nuevo


    def pop(self):

        if self.esta_vacia():
            return None

        dato = self.tope.dato

        self.tope = self.tope.siguiente

        return dato


    def peek(self):

        if self.esta_vacia():
            return None

        return self.tope.dato


    def recorrer(self):

        elementos = []

        actual = self.tope

        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos