import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

class PanelLibros(tk.Frame):

    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        self.crear_componentes()
        self.actualizar_tabla()

    # Todos los elementos que se muestran en el panel
    def crear_componentes(self):
        titulo = tk.Label(
            self,
            text="Gestión de Libros",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        #Formulario
        formulario = tk.Frame(self)
        formulario.pack(pady=10)
        tk.Label(formulario, text="Código").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.codigo = tk.Entry(formulario)
        self.codigo.grid(row=0, column=1, padx=5)

        tk.Label(formulario, text="Título").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.titulo = tk.Entry(formulario)
        self.titulo.grid(row=1, column=1, padx=5)

        tk.Label(formulario, text="Autor").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.autor = tk.Entry(formulario)
        self.autor.grid(row=2, column=1, padx=5)

        tk.Label(formulario, text="Categoría").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.categoria = tk.Entry(formulario)
        self.categoria.grid(row=3, column=1, padx=5)

        tk.Label(formulario, text="Año").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.anio = tk.Entry(formulario)
        self.anio.grid(row=4, column=1, padx=5)

        tk.Label(formulario, text="El código del libro no se puede modificar al editar", fg="gray").grid(row=5, column=0, columnspan=2, pady=5)


        #Botones
        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(botones, text="Registrar", command=self.registrar_libro).grid(row=0, column=0, padx=5)
        tk.Button(botones, text="Buscar", command=self.buscar_libro).grid(row=0, column=1, padx=5)
        tk.Button(botones, text="Eliminar", command=self.eliminar_libro).grid(row=0, column=2, padx=5)
        tk.Button(botones, text="Editar", command=self.editar_libro).grid(row=0, column=3, padx=5)
        tk.Button(botones, text="Actualizar Lista", command=self.actualizar_tabla).grid(row=0, column=4, padx=5)

        #Tabla de libros
        columnas = (
            "codigo",
            "titulo",
            "autor",
            "categoria",
            "año",
            "estado"
        )

        #Títulos de la tabla
        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=12
        )

        # Tablas de contenido
        for columna in columnas:
            self.tabla.heading(columna, text=columna.capitalize())
            self.tabla.column(columna, width=150)

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        """
        Para resaltar todos los datos de un libro
        al hacerle doble click en su respectiva fila de la tabla

        1) También sirve para mostrar todos los datos
        del libro seleccionado en el formulario
        2) Y para escoger cuál editar
        """

        self.tabla.bind("<Double-1>",self.seleccionar_libro)

    # Métodos auxiliares
    def obtener_datos_formulario(self):
        return (
            self.codigo.get().strip(),
            self.titulo.get().strip(),
            self.autor.get().strip(),
            self.categoria.get().strip(),
            self.anio.get().strip()
            )

    def limpiar_campos(self):
        self.desbloquear_codigo()
        self.codigo.delete(0, tk.END)
        self.titulo.delete(0, tk.END)
        self.autor.delete(0, tk.END)
        self.categoria.delete(0, tk.END)
        self.anio.delete(0, tk.END)

    def bloquear_codigo(self):
        self.codigo.config(state="disabled")

    def desbloquear_codigo(self):
        self.codigo.config(state="normal")


    def registrar_libro(self):
        codigo, titulo, autor, categoria, anio = self.obtener_datos_formulario()

        if not re.fullmatch(r"[A-Za-z]\d{1,3}", codigo):
            messagebox.showerror(
                "Error",
                "El código debe tener una letra seguida de 1 a 3 números.\nEjemplos: A1, B25, L999"
            )
            return

        # Validar que no se registren libros con datos incompletos
        if not codigo or not titulo or not autor or not categoria or not anio:
            messagebox.showerror(
                "Error",
                "Complete los campos obligatorios"
            )
            return

        # Convertir año a entero y validarlo
        try:
            anio = int(anio)

        except ValueError:
            messagebox.showerror(
            "Error",
            "El año debe ser un número entero"
            )
            return

        # Llamar a la lógica de la biblioteca
        exito, mensaje = self.biblioteca.registrar_libro(
            codigo,
            titulo,
            autor,
            categoria,
            anio
        )

        # Mostrar el resultado
        if exito:
            messagebox.showinfo("Correcto", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

        # Si se registró correctamente, limpiar los campos
        if exito:
            self.limpiar_campos()

            # Actualizar la tabla
            self.actualizar_tabla()



    def actualizar_tabla(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for libro in self.biblioteca.listar_libros():
            estado = (
                "Disponible"
                if libro.disponible
                else "Prestado"
            )

            self.tabla.insert(
                "",
                "end",
                values=(
                    libro.codigo,
                    libro.titulo,
                    libro.autor,
                    libro.categoria,
                    libro.anio,
                    estado
                )
            )


    def seleccionar_libro(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado, "values")

        self.limpiar_campos()

        self.codigo.insert(0, datos[0])
        self.titulo.insert(0, datos[1])
        self.autor.insert(0, datos[2])
        self.categoria.insert(0, datos[3])
        self.anio.insert(0, datos[4])
        self.bloquear_codigo()


    def buscar_libro(self):

        codigo = self.codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Buscar",
                "Ingrese un código"
            )
            return

        libro = self.biblioteca.buscar_libro(codigo)

        if libro is None:
            messagebox.showerror(
                "Error",
                "Libro no encontrado"
            )
            return

        self.limpiar_campos()

        self.codigo.insert(0, libro.codigo)
        self.titulo.insert(0, libro.titulo)
        self.autor.insert(0, libro.autor)
        self.categoria.insert(0, libro.categoria)
        self.anio.insert(0, libro.anio)
        self.bloquear_codigo()


    def eliminar_libro(self):

        codigo = self.codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Eliminar",
                "Ingrese el código del libro"
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar este libro?"
        )

        if not respuesta:
            return

        exito, mensaje = self.biblioteca.eliminar_libro(codigo)

        if exito:
            messagebox.showinfo(
                "Correcto",
                mensaje
            )

            self.limpiar_campos()
            self.actualizar_tabla()

        else:
            messagebox.showerror(
                "Error",
                mensaje
            )

    
    def editar_libro(self):

        codigo, titulo, autor, categoria, anio = self.obtener_datos_formulario()

        # Para editar solo un libro
        if not codigo:
            messagebox.showwarning(
            "Editar libro",
            "Ingrese el código del libro que desea editar"
            )
            return

        # Evitar que se deje algún campo sin editar
        if not titulo or not autor or not categoria or not anio:
            messagebox.showwarning(
                "Editar libro",
                "Complete los campos obligatorios"
            )
            return

        # Convertir año a entero
        try:
            anio = int(anio)

        except ValueError:
            messagebox.showerror(
            "Error",
            "El año debe ser un número entero"
            )
            return

        exito, mensaje = self.biblioteca.editar_libro(
            codigo,
            titulo,
            autor,
            categoria,
            anio
        )

        # Validar si se editaron correctamente o no los datos del libro
        if exito:
            messagebox.showinfo(
                "Correcto",
                mensaje
            )
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror(
                "Error",
                mensaje
            )