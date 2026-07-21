from datetime import date, timedelta

class Prestamo:

    def __init__(self, usuario, libro):
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = date.today()

        self.fecha_devolucion = (
            self.fecha_prestamo + timedelta(days=7)
        )

    def __str__(self):

        return (
            f"{self.usuario.nombre} "
            f"-> "
            f"{self.libro.titulo} "
        )
