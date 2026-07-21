class Usuario:

    def __init__(self, cedula, nombre, apellido, correo, telefono=""):

        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono

    def __str__(self):
        return f"{self.cedula} - {self.nombre} {self.apellido}"