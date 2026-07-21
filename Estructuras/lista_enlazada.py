from Estructuras.nodo import Nodo

class ListaEnlazada:

    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None


    def insertar(self, dato):
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self.cabeza = nuevo
            return

        actual = self.cabeza

        while actual.siguiente:
            actual = actual.siguiente

        actual.siguiente = nuevo


    def buscar(self, condicion):
        actual = self.cabeza

        while actual:

            if condicion(actual.dato):
                return actual.dato

            actual = actual.siguiente

        return None


    def eliminar(self, condicion):
        actual = self.cabeza
        anterior = None

        while actual:

            if condicion(actual.dato):

                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                return True

            anterior = actual
            actual = actual.siguiente

        return False


    def recorrer(self):
        elementos = []

        actual = self.cabeza

        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos


    def cantidad(self):
        contador = 0

        actual = self.cabeza

        while actual:

            contador += 1

            actual = actual.siguiente

        return contador
    
    
    def cantidad_prestamos(self):
        return self.prestamos.cantidad()