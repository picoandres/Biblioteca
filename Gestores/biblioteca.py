from Estructuras.arbol_bst import Arbol_BST
from Estructuras.lista_enlazada import ListaEnlazada
from Estructuras.pila import Pila
from Estructuras.cola import Cola
from Modelos.libro import Libro
from Modelos.usuario import Usuario
from Modelos.prestamo import Prestamo
from datetime import datetime
import re

class Biblioteca:
    def __init__(self):
        self.libros = Arbol_BST()
        self.usuarios = ListaEnlazada()
        self.prestamos = ListaEnlazada()
        self.historial = Pila()
        self.espera = Cola()
    
# MÉTODOS DE PANEL DE LIBROS
    def registrar_libro(self, codigo, titulo, autor, categoria="", anio=0):
        codigo = codigo.strip()
        titulo = titulo.strip()
        autor = autor.strip()
        categoria = categoria.strip()
        
        if self.libros.buscar(codigo):
            return False, "Ya existe un libro con ese código"

        if not self._anio_libro_valido(anio):
            return False, "El año debe estar entre 0 y el año actual"

        libro = Libro(
            codigo,
            titulo,
            autor,
            categoria,
            anio
        )

        self.libros.insertar(libro)
        self._registrar_historial("Libro registrado", f"{codigo} - {titulo}")
        return True, "Libro registrado correctamente"


    def buscar_libro(self, codigo):
        return self.libros.buscar(codigo)
        

    def eliminar_libro(self, codigo):
        libro = self.libros.buscar(codigo)

        if libro is None:
            return False, "El libro no existe"
        
        # Validar si el libro está prestado
        prestamo = self.buscar_prestamo(codigo)

        if prestamo is not None:
            return False, "No se puede eliminar un libro mientras está prestado"

        # Validar si tiene usuarios en cola de espera
        if not libro.cola_espera.esta_vacia():
            return False, "No se puede eliminar el libro porque tiene usuarios en cola de espera"

        self.libros.eliminar(codigo)

        self._registrar_historial("Libro eliminado", f"{libro.titulo} - {codigo}")
        return True, "Libro eliminado correctamente"
    

    def editar_libro(self, codigo, titulo, autor, categoria, anio):
        codigo = codigo.strip()
        titulo = titulo.strip()
        autor = autor.strip()
        categoria = categoria.strip()

        libro = self.buscar_libro(codigo)

        if libro is None:
            return False, "El libro no existe"

        if not self._anio_libro_valido(anio):
            return False, "El año debe estar entre 0 y el año actual"

        libro.titulo = titulo
        libro.autor = autor
        libro.categoria = categoria
        libro.anio = anio

        self._registrar_historial("Libro editado: ", f"{codigo} - {titulo}")
        return True, "Libro actualizado correctamente"


# MÉTODOS DE PANEL DE USUARIO
    def listar_usuarios(self):
        return self.usuarios.recorrer()

    def registrar_usuario(self, cedula, nombre, apellido, correo, telefono=""):
        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido = apellido.strip()
        correo = correo.strip()
        telefono = telefono.strip()

        if not self._cedula_valida(cedula):
            return False, "La cédula debe contener exactamente 10 dígitos numéricos"

        if not self._telefono_valido(telefono):
            return False, "El teléfono debe contener exactamente 10 dígitos numéricos"

        if self.buscar_usuario(cedula):
            return False, "Ya existe un usuario con esa cédula"

        if self.buscar_usuario_por_correo(correo):
            return False, "Ya existe un usuario con ese correo"

        if not self._correo_valido(correo):
            return False, "El correo ingresado no tiene un formato válido"

        if self._correo_duplicado(correo):
            return False, "Ya existe un usuario con ese correo"

        if self._telefono_duplicado(telefono):
            return False, "Ya existe un usuario con ese número de teléfono"

        usuario = Usuario(cedula, nombre, apellido, correo, telefono)
        self.usuarios.insertar(usuario)

        self._registrar_historial("Usuario registrado", f"{cedula} - {nombre}")
        return True, "Usuario registrado correctamente"


    def buscar_usuario(self, cedula):
        return self.usuarios.buscar(lambda u: u.cedula == cedula)
        

    def eliminar_usuario(self, cedula):
        usuario = self.buscar_usuario(cedula)

        if usuario is None:
            return False, "El usuario no existe"

         # Validar si el usuario tiene préstamos activos
        if self.usuario_tiene_prestamos(cedula):
            return False, "No se puede eliminar el usuario porque tiene préstamos activos"

    # Validar si el usuario está en alguna cola de espera
        if self.usuario_en_cola_espera(cedula):
            return False, "No se puede eliminar el usuario porque está en una cola de espera"

        # Eliminar usuario si pasa las validaciones
        eliminado = self.usuarios.eliminar(lambda u: u.cedula == cedula)

        if eliminado:
            self._registrar_historial("Usuario eliminado", f"{cedula} - {usuario.nombre}")
            return True, "Usuario eliminado correctamente"

        return False, "No se pudo eliminar el usuario"


    def editar_usuario(self, cedula, nombre, apellido, correo, telefono):
        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido = apellido.strip()
        correo = correo.strip()
        telefono = telefono.strip()

        if not self._cedula_valida(cedula):
            return False, "La cédula debe contener exactamente 10 dígitos numéricos"

        if not self._telefono_valido(telefono):
            return False, "El teléfono debe contener exactamente 10 dígitos numéricos"

        usuario = self.buscar_usuario(cedula)
        if usuario is None:
            return False, "El usuario no existe"

        usuario_correo = self.buscar_usuario_por_correo(correo)
        if usuario_correo and usuario_correo.cedula != cedula:
            return False, "Ese correo ya está registrado por otro usuario"

        if not self._correo_valido(correo):
            return False, "El correo ingresado no tiene un formato válido"
        
        if self._correo_duplicado(correo):
            return False, "Ya existe un usuario con ese correo"

        if self._telefono_duplicado(telefono):
            return False, "Ya existe un usuario con ese número de teléfono"

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.telefono = telefono

        self._registrar_historial("Usuario editado", f"{cedula} - {nombre}")
        return True, "Usuario actualizado correctamente"


# MÉTODOS PARA VALIDACIONES DE USUARIO
    def usuario_tiene_prestamos(self, cedula):
        return self.prestamos.buscar(lambda p: p.usuario.cedula == cedula) is not None


    def usuario_en_cola_espera(self, cedula):
        for libro in self.listar_libros():
            if libro.cola_espera.contiene(lambda u: u.cedula == cedula):
                return True
        return False


    def usuario_ya_tiene_libro(self, cedula, codigo):
        return self.prestamos.buscar(lambda p: p.usuario.cedula == cedula and p.libro.codigo == codigo) is not None


    def buscar_usuario_por_correo(self, correo):
        return self.usuarios.buscar(lambda u: u.correo.lower() == correo.lower())


    def _correo_valido(self, correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, correo) is not None


    def _telefono_duplicado(self, telefono, cedula_actual=None):
        if not telefono.strip():
            return False

        for usuario in self.usuarios.recorrer():
            if usuario.telefono == telefono:
                if cedula_actual is None or usuario.cedula != cedula_actual:
                    return True
        return False
    

    def _correo_duplicado(self, correo, cedula_actual=None):
        for usuario in self.usuarios.recorrer():
            if usuario.correo.lower() == correo.lower():
                if cedula_actual is None or usuario.cedula != cedula_actual:
                    return True
        return False


    def _cedula_valida(self, cedula):
        cedula = cedula.strip()
        return cedula.isdigit() and len(cedula) == 10


    def _telefono_valido(self, telefono):
        telefono = telefono.strip()

    # El teléfono es opcional, por lo que vacío sí se permite
        if telefono == "":
            return True

        return telefono.isdigit() and len(telefono) == 10


    def _anio_libro_valido(self, anio):
        anio_actual = datetime.now().year
        return isinstance(anio, int) and 0 <= anio <= anio_actual


# MÉTODOS DE PANEL DE PRÉSTAMOS
    def prestar_libro(self, cedula, codigo):
        usuario = self.buscar_usuario(cedula)

        if usuario is None:
            return False, "El usuario no existe"

        libro = self.buscar_libro(codigo)

        if libro is None:
            return False, "El libro no existe"

        prestamo_actual = self.buscar_prestamo(codigo)

        if libro.disponible:
            libro.prestar()

            prestamo = Prestamo(usuario, libro)
            self.prestamos.insertar(prestamo)

            self._registrar_historial(f"Préstamo realizado", f"{usuario.nombre} prestó {libro.titulo}")
            return True, "Préstamo realizado"
        
        # Para que no se agregue a la cola al usuario que ya está prestando
        if prestamo_actual is not None and prestamo_actual.usuario.cedula == cedula:
            return False, "El usuario ya tiene prestado ese libro"

        # Si el libro no está disponible, revisar si ya está en la cola
        if libro.cola_espera.contiene(lambda u: u.cedula == usuario.cedula):
            return False, "El usuario ya se encuentra en la lista de espera"        
        
        # Agregar a la cola de espera
        libro.cola_espera.encolar(usuario)

        self._registrar_historial("Usuario agregado a la cola de espera", f"{usuario.nombre} para {libro.titulo}")
        return True, "Libro actualmente prestado. Usuario agregado a la lista de espera"


    def buscar_prestamo(self, codigo):
        return self.prestamos.buscar(lambda p: p.libro.codigo == codigo)


    def devolver_libro(self, codigo):
        prestamo = self.buscar_prestamo(codigo)

        if prestamo is None:
            return False, "Ese libro no está prestado"

        libro = prestamo.libro

        self.prestamos.eliminar(lambda p: p.libro.codigo == codigo)

        # Si no hay cola de espera, el libro vuelve a estar disponible
        if libro.cola_espera.esta_vacia():
            libro.devolver()

            self._registrar_historial("Devolución de libro", f"{libro.codigo} - {libro.titulo}")
            return True, "Libro devuelto correctamente"

        # Si hay cola, se presta automáticamente al siguiente usuario
        siguiente_usuario = libro.cola_espera.desencolar()

        nuevo = Prestamo(siguiente_usuario, libro)
        self.prestamos.insertar(nuevo)

        self._registrar_historial("Préstamo automático por cola de espera", f"{siguiente_usuario.nombre} recibió {libro.titulo}")
        return True, f"Libro entregado automáticamente a: {siguiente_usuario.nombre}"
    

    def listar_prestamos(self):
        return self.prestamos.recorrer()
    

    def mostrar_cola_espera(self, codigo):
        libro = self.buscar_libro(codigo)

        if libro is None:
            return []

        return libro.cola_espera.recorrer()
    
# MÉTODOS DE PANEL DE HISTORIAL
    def _registrar_historial(self, accion, detalle):
        self.historial.push({
        "accion": accion,
        "detalle": detalle
    })

    def mostrar_historial(self):
        return self.historial.recorrer()

# MÉTODOS DE PANEL DE ESTADÍSTICAS
    def estadisticas(self):
        libros = self.listar_libros()

        total_libros = len(libros)
        libros_disponibles = 0
        libros_prestados = 0
        usuarios_en_cola = 0

        for libro in libros:
            if libro.disponible:
                libros_disponibles += 1
            else:
                libros_prestados += 1

            usuarios_en_cola += len(libro.cola_espera.recorrer())

        return {
            "libros": total_libros,
            "usuarios": self.usuarios.cantidad(),
            "prestamos": self.prestamos.cantidad(),
            "libros_disponibles": libros_disponibles,
            "libros_prestados": libros_prestados,
            "usuarios_en_cola": usuarios_en_cola
        }

    
    # MÉTODOS DE RECORRIDOS DEL ÁRBOL DE LIBROS
    def listar_libros_inorden(self):
        return self.libros.inorden()

    def listar_libros_preorden(self):
        return self.libros.preorden()

    def listar_libros_postorden(self):
        return self.libros.postorden()
    
    def representar_arbol_libros(self):
        return self.libros.representar_arbol()

    # Alias (inorden es el método predeterminado de recorrido)
    def listar_libros(self):
        return self.listar_libros_inorden()