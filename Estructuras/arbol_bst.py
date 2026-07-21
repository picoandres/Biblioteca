class NodoArbol:

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

class Arbol_BST:

    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
            return

        self._insertar(self.raiz, dato)


    def _insertar(self, nodo, dato):

        if dato.codigo < nodo.dato.codigo:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(dato)
            else:
                self._insertar(nodo.izquierdo, dato)

        elif dato.codigo > nodo.dato.codigo:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(dato)
            else:
                self._insertar(nodo.derecho, dato)


    def buscar(self, codigo):
        return self._buscar(self.raiz, codigo)


    def _buscar(self, nodo, codigo):
        if nodo is None:
            return None

        if codigo == nodo.dato.codigo:
            return nodo.dato

        if codigo < nodo.dato.codigo:
            return self._buscar(nodo.izquierdo, codigo)

        return self._buscar(nodo.derecho, codigo)


    def eliminar(self, codigo):
        self.raiz = self._eliminar(self.raiz, codigo)


    def _eliminar(self, nodo, codigo):
        if nodo is None:
            return nodo

        if codigo < nodo.dato.codigo:
            nodo.izquierdo = self._eliminar(
                nodo.izquierdo,
                codigo
            )

        elif codigo > nodo.dato.codigo:
            nodo.derecho = self._eliminar(
                nodo.derecho,
                codigo
            )

        else:

            if nodo.izquierdo is None:
                return nodo.derecho

            if nodo.derecho is None:
                return nodo.izquierdo

            sucesor = self._minimo(nodo.derecho)

            nodo.dato = sucesor.dato

            nodo.derecho = self._eliminar(
                nodo.derecho,
                sucesor.dato.codigo
            )

        return nodo
    

    def inorden(self):
        resultado = []

        self._inorden(self.raiz, resultado)

        return resultado


    def _inorden(self, nodo, resultado):
        if nodo:

            self._inorden(nodo.izquierdo, resultado)

            resultado.append(nodo.dato)

            self._inorden(nodo.derecho, resultado)


    def preorden(self):
        resultado = []

        self._preorden(self.raiz, resultado)

        return resultado


    def _preorden(self, nodo, resultado):
        if nodo:

            resultado.append(nodo.dato)

            self._preorden(nodo.izquierdo, resultado)

            self._preorden(nodo.derecho, resultado)


    def postorden(self):
        resultado = []

        self._postorden(self.raiz, resultado)

        return resultado


    def _postorden(self, nodo, resultado):
        if nodo:

            self._postorden(nodo.izquierdo, resultado)

            self._postorden(nodo.derecho, resultado)

            resultado.append(nodo.dato)


    def _minimo(self, nodo):
        while nodo.izquierdo:

            nodo = nodo.izquierdo

        return nodo
    

    def cantidad(self):
        return self._cantidad(self.raiz)


    def _cantidad(self, nodo):
        if nodo is None:
            return 0

        return (
            1 +
            self._cantidad(nodo.izquierdo) +
            self._cantidad(nodo.derecho)
        )
    
    def representar_arbol(self):
        if self.raiz is None:
            return "Árbol vacío"

        lineas = []
        self._representar_arbol(self.raiz, "", True, lineas)
        return "\n".join(lineas)


    def _representar_arbol(self, nodo, prefijo, es_ultimo, lineas):
        if nodo is None:
            return

        conector = "└── " if es_ultimo else "├── "
        lineas.append(f"{prefijo}{conector}{nodo.dato.codigo} - {nodo.dato.titulo}")

        hijos = []
        if nodo.izquierdo is not None:
            hijos.append(nodo.izquierdo)
        if nodo.derecho is not None:
            hijos.append(nodo.derecho)

        for i, hijo in enumerate(hijos):
            ultimo = i == len(hijos) - 1

            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            self._representar_arbol(hijo, nuevo_prefijo, ultimo, lineas)