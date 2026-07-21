import tkinter as tk
from tkinter import ttk, messagebox

class PanelPrestamos(tk.Frame):

    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        self.crear_componentes()
        self.actualizar_tabla()

    #Todos los elementos que se muestran en el panel
    def crear_componentes(self):
        titulo = tk.Label(
            self,
            text="Gestión de Préstamos",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Formularios
        formulario = tk.Frame(self)
        formulario.pack(pady=10)

        tk.Label(formulario, text="Cédula del usuario").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cedula = tk.Entry(formulario)
        self.cedula.grid(row=0, column=1, padx=5)

        tk.Label(formulario, text="Código del libro").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.codigo = tk.Entry(formulario)
        self.codigo.grid(row=1, column=1, padx=5)

        tk.Label(
            formulario,
            text="Para devolver o buscar un préstamo basta con el código del libro",
            fg="gray").grid(row=2, column=0, columnspan=2, pady=5)

        #Botones
        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(botones, text="Prestar", command=self.prestar_libro).grid(row=0, column=0, padx=5)
        tk.Button(botones, text="Buscar préstamo", command=self.buscar_prestamo).grid(row=0, column=1, padx=5)
        tk.Button(botones, text="Devolver libro", command=self.devolver_libro).grid(row=0, column=2, padx=5)
        tk.Button(botones,text="Actualizar Lista",command=self.actualizar_tabla).grid(row=0, column=3, padx=5)
        tk.Button(botones, text="Ver cola de espera", command=self.ver_cola_espera).grid(row=0, column=4, padx=5)

        # Tabla de préstamos
        columnas = ("cedula", "usuario", "codigo", "libro")

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tabla.heading("cedula", text="Cédula")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.heading("codigo", text="Código del libro")
        self.tabla.heading("libro", text="Título del libro")

        self.tabla.column("cedula", width=150)
        self.tabla.column("usuario", width=220)
        self.tabla.column("codigo", width=120)
        self.tabla.column("libro", width=250)

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla.bind("<Double-1>", self.seleccionar_prestamo)

    # Métodos auxiliares
    def obtener_datos_formulario(self):
        return (
            self.cedula.get().strip(),
            self.codigo.get().strip()
        )

    def limpiar_campos(self):
        self.cedula.delete(0, tk.END)
        self.codigo.delete(0, tk.END)

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        prestamos = self.biblioteca.listar_prestamos()

        for prestamo in prestamos:
            self.tabla.insert(
                "",
                "end",
                values=(
                    prestamo.usuario.cedula,
                    prestamo.usuario.nombre,
                    prestamo.libro.codigo,
                    prestamo.libro.titulo
                )
            )

    def seleccionar_prestamo(self, event):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado, "values")

        self.limpiar_campos()

        self.cedula.insert(0, datos[0])
        self.codigo.insert(0, datos[2])


    # Primera opción del panel
    def prestar_libro(self):
        cedula, codigo = self.obtener_datos_formulario()

        if not cedula or not codigo:
            messagebox.showwarning(
                "Préstamo",
                "Ingrese la cédula del usuario y el código del libro"
            )
            return

        exito, mensaje = self.biblioteca.prestar_libro(cedula, codigo)

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)


    def buscar_prestamo(self):
        codigo = self.codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Buscar préstamo",
                "Ingrese el código del libro"
            )
            return

        prestamo = self.biblioteca.buscar_prestamo(codigo)

        if prestamo is None:
            messagebox.showerror(
                "Error",
                "No existe un préstamo activo para ese libro"
            )
            return

        self.limpiar_campos()

        self.cedula.insert(0, prestamo.usuario.cedula)
        self.codigo.insert(0, prestamo.libro.codigo)

        messagebox.showinfo(
            "Préstamo encontrado",
            f"Usuario: {prestamo.usuario.nombre}\n"
            f"Libro: {prestamo.libro.titulo}"
        )


    def devolver_libro(self):
        codigo = self.codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Devolver libro",
                "Ingrese el código del libro"
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar devolución",
            "¿Está seguro de devolver este libro?"
        )

        if not respuesta:
            return

        exito, mensaje = self.biblioteca.devolver_libro(codigo)

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)


    def ver_cola_espera(self):
        codigo = self.codigo.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Cola de espera",
                "Ingrese el código del libro"
            )
            return

        libro = self.biblioteca.buscar_libro(codigo)

        if libro is None:
            messagebox.showerror(
                "Error",
                "El libro no existe"
            )
            return

        cola = self.biblioteca.mostrar_cola_espera(codigo)

        if not cola:
            messagebox.showinfo(
                "Cola de espera",
                "Este libro no tiene usuarios en cola de espera"
            )
            return

        texto = f"Cola de espera del libro: {libro.titulo}\n\n"

        for i, usuario in enumerate(cola, 1):
            texto += f"{i}. {usuario.nombre} - {usuario.cedula}\n"

        messagebox.showinfo("Cola de espera", texto)