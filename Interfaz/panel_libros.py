import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

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
        # Pide el código mediante una ventana flotante
        codigo = simpledialog.askstring("Buscar Libro", "Ingrese el código del libro:")

        # Si el usuario presiona "Cancelar" o deja el campo vacío
        if not codigo or not codigo.strip():
            if codigo is not None and not codigo.strip():
                messagebox.showwarning("Buscar", "Debe ingresar un código válido.")
            return

        codigo = codigo.strip()
        libro = self.biblioteca.buscar_libro(codigo)

        if libro is None:
            messagebox.showerror("Error", "Libro no encontrado")
            return

        # Si se encuentra, limpia los campos y carga la información
        self.limpiar_campos()

        self.codigo.insert(0, libro.codigo)
        self.titulo.insert(0, libro.titulo)
        self.autor.insert(0, libro.autor)
        self.categoria.insert(0, libro.categoria)
        self.anio.insert(0, libro.anio)
        self.bloquear_codigo()

        info_libro = (
        f"Libro Encontrado\n\n"
        f"• Código: {libro.codigo}\n"
        f"• Título: {libro.titulo}\n"
        f"• Autor: {libro.autor}\n"
        f"• Categoría: {libro.categoria}\n"
        f"• Año: {libro.anio}"
        )
        messagebox.showinfo("Detalles del Libro", info_libro)


    def eliminar_libro(self):
        # Pide el código mediante ventana flotante
        codigo = simpledialog.askstring("Eliminar Libro", "Ingrese el código del libro a eliminar:")

        # Si cancela o lo deja vacío
        if not codigo or not codigo.strip():
            if codigo is not None and not codigo.strip():
                messagebox.showwarning("Eliminar", "Debe ingresar un código válido.")
            return

        codigo = codigo.strip()

        # Confirmación de eliminación
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el libro con código '{codigo}'?"
        )

        if not respuesta:
            return

        exito, mensaje = self.biblioteca.eliminar_libro(codigo)

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    
    def editar_libro(self):

        codigo = simpledialog.askstring("Editar Libro", "Ingrese el código del libro a editar:")

        if not codigo or not codigo.strip():
            if codigo is not None and not codigo.strip():
                messagebox.showwarning("Editar Libro", "Debe ingresar un código válido.")
            return

        codigo = codigo.strip()

        # 2. Buscar el libro
        libro = self.biblioteca.buscar_libro(codigo)
        if libro is None:
            messagebox.showerror("Error", "Libro no encontrado")
            return

        # 3. Crear la ventana flotante (Toplevel) para el formulario de edición
        ventana_edit = tk.Toplevel(self)
        ventana_edit.title("Editar Libro")
        ventana_edit.geometry("350x300")
        ventana_edit.resizable(False, False)
        ventana_edit.grab_set()  # Bloquea la ventana principal mientras esta está abierta

        # Crear etiquetas y campos de entrada en la ventana flotante
        tk.Label(ventana_edit, text="Código:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        entry_codigo = tk.Entry(ventana_edit)
        entry_codigo.grid(row=0, column=1, padx=10, pady=8)
        entry_codigo.insert(0, libro.codigo)
        entry_codigo.config(state="disabled") # El código no se debe modificar

        tk.Label(ventana_edit, text="Título:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        entry_titulo = tk.Entry(ventana_edit)
        entry_titulo.grid(row=1, column=1, padx=10, pady=8)
        entry_titulo.insert(0, libro.titulo)

        tk.Label(ventana_edit, text="Autor:").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        entry_autor = tk.Entry(ventana_edit)
        entry_autor.grid(row=2, column=1, padx=10, pady=8)
        entry_autor.insert(0, libro.autor)

        tk.Label(ventana_edit, text="Categoría:").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        entry_categoria = tk.Entry(ventana_edit)
        entry_categoria.grid(row=3, column=1, padx=10, pady=8)
        entry_categoria.insert(0, libro.categoria)

        tk.Label(ventana_edit, text="Año:").grid(row=4, column=0, padx=10, pady=8, sticky="e")
        entry_anio = tk.Entry(ventana_edit)
        entry_anio.grid(row=4, column=1, padx=10, pady=8)
        entry_anio.insert(0, libro.anio)

        # Función interna para guardar los cambios desde la ventana flotante
        def guardar_cambios():
            titulo = entry_titulo.get().strip()
            autor = entry_autor.get().strip()
            categoria = entry_categoria.get().strip()
            anio_str = entry_anio.get().strip()

            if not titulo or not autor or not categoria or not anio_str:
                messagebox.showwarning("Editar Libro", "Complete todos los campos", parent=ventana_edit)
                return

            try:
                anio = int(anio_str)
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número entero", parent=ventana_edit)
                return

            exito, mensaje = self.biblioteca.editar_libro(codigo, titulo, autor, categoria, anio)

            if exito:
                messagebox.showinfo("Correcto", mensaje)
                self.actualizar_tabla()
                self.limpiar_campos()
                ventana_edit.destroy() # Cierra la ventana flotante
            else:
                messagebox.showerror("Error", mensaje, parent=ventana_edit)

        # Botón Guardar dentro de la ventana flotante
        btn_guardar = tk.Button(ventana_edit, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=15)
