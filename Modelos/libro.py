from Estructuras.cola import Cola

class Libro:

    def __init__(self, codigo, titulo, autor, categoria="", anio=0):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.anio = anio

        self.disponible = True

        # Cola exclusiva para este libro
        self.cola_espera = Cola()

    def prestar(self):
        self.disponible = False

    def devolver(self):
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"

        return (
            f"[{self.codigo}] "
            f"{self.titulo} - "
            f"{self.autor} ({estado})"
        )