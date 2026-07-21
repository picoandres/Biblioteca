import tkinter as tk
from tkinter import ttk, messagebox


class PanelEstadisticas(tk.Frame):

    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        self.crear_componentes()
        self.actualizar_estadisticas()

    def crear_componentes(self):
        titulo = tk.Label(
            self,
            text="Estadísticas del Sistema",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        subtitulo = tk.Label(
            self,
            text="Resumen general de la biblioteca y sus estructuras de datos",
            fg="gray"
        )
        subtitulo.pack(pady=(0, 10))

        # =========================
        # BOTONES
        # =========================
        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(
            botones,
            text="Actualizar estadísticas",
            command=self.actualizar_estadisticas
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            botones,
            text="Mostrar detalle",
            command=self.mostrar_detalle
        ).grid(row=0, column=1, padx=5)

        # =========================
        # MARCO PRINCIPAL DE TARJETAS
        # =========================
        self.marco_tarjetas = tk.Frame(self)
        self.marco_tarjetas.pack(padx=10, pady=10, fill="x")

        # Variables de texto para las tarjetas
        self.var_libros = tk.StringVar(value="0")
        self.var_usuarios = tk.StringVar(value="0")
        self.var_prestamos = tk.StringVar(value="0")
        self.var_disponibles = tk.StringVar(value="0")
        self.var_prestados = tk.StringVar(value="0")
        self.var_cola = tk.StringVar(value="0")

        # Crear tarjetas
        self.crear_tarjeta(self.marco_tarjetas, "Total de libros", self.var_libros, 0, 0)
        self.crear_tarjeta(self.marco_tarjetas, "Total de usuarios", self.var_usuarios, 0, 1)
        self.crear_tarjeta(self.marco_tarjetas, "Préstamos activos", self.var_prestamos, 0, 2)

        self.crear_tarjeta(self.marco_tarjetas, "Libros disponibles", self.var_disponibles, 1, 0)
        self.crear_tarjeta(self.marco_tarjetas, "Libros prestados", self.var_prestados, 1, 1)
        self.crear_tarjeta(self.marco_tarjetas, "Usuarios en cola", self.var_cola, 1, 2)

        # =========================
        # TABLA RESUMEN
        # =========================
        marco_tabla = tk.LabelFrame(
            self,
            text="Resumen numérico",
            padx=10,
            pady=10
        )
        marco_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("concepto", "cantidad")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=6
        )

        self.tabla.heading("concepto", text="Concepto")
        self.tabla.heading("cantidad", text="Cantidad")

        self.tabla.column("concepto", width=300, anchor="w")
        self.tabla.column("cantidad", width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True)

        # =========================
        # ÁREA DE DETALLE
        # =========================
        marco_detalle = tk.LabelFrame(
            self,
            text="Detalle de estadísticas",
            padx=10,
            pady=10
        )
        marco_detalle.pack(fill="x", padx=10, pady=(0, 10))

        self.texto_detalle = tk.Text(
            marco_detalle,
            height=8,
            wrap="word"
        )
        self.texto_detalle.pack(fill="x")
        self.texto_detalle.config(state="disabled")

    def crear_tarjeta(self, contenedor, titulo, variable, fila, columna):
        tarjeta = tk.LabelFrame(
            contenedor,
            text=titulo,
            padx=20,
            pady=15
        )
        tarjeta.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")

        lbl_valor = tk.Label(
            tarjeta,
            textvariable=variable,
            font=("Arial", 20, "bold")
        )
        lbl_valor.pack()

        contenedor.grid_columnconfigure(columna, weight=1)

    def actualizar_estadisticas(self):
        datos = self.biblioteca.estadisticas()

        self.var_libros.set(str(datos.get("libros", 0)))
        self.var_usuarios.set(str(datos.get("usuarios", 0)))
        self.var_prestamos.set(str(datos.get("prestamos", 0)))
        self.var_disponibles.set(str(datos.get("libros_disponibles", 0)))
        self.var_prestados.set(str(datos.get("libros_prestados", 0)))
        self.var_cola.set(str(datos.get("usuarios_en_cola", 0)))

        self.actualizar_tabla(datos)
        self.actualizar_texto_detalle(datos)

    def actualizar_tabla(self, datos):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        filas = [
            ("Total de libros", datos.get("libros", 0)),
            ("Total de usuarios", datos.get("usuarios", 0)),
            ("Préstamos activos", datos.get("prestamos", 0)),
            ("Libros disponibles", datos.get("libros_disponibles", 0)),
            ("Libros prestados", datos.get("libros_prestados", 0)),
            ("Usuarios en cola de espera", datos.get("usuarios_en_cola", 0))
        ]

        for concepto, cantidad in filas:
            self.tabla.insert("", "end", values=(concepto, cantidad))

    def actualizar_texto_detalle(self, datos):
        texto = (
            "Resumen del estado actual del sistema de biblioteca:\n\n"
            f"- Total de libros registrados: {datos.get('libros', 0)}\n"
            f"- Total de usuarios registrados: {datos.get('usuarios', 0)}\n"
            f"- Préstamos activos: {datos.get('prestamos', 0)}\n"
            f"- Libros disponibles para préstamo: {datos.get('libros_disponibles', 0)}\n"
            f"- Libros actualmente prestados: {datos.get('libros_prestados', 0)}\n"
            f"- Usuarios en colas de espera: {datos.get('usuarios_en_cola', 0)}\n"
        )

        self.texto_detalle.config(state="normal")
        self.texto_detalle.delete("1.0", tk.END)
        self.texto_detalle.insert("1.0", texto)
        self.texto_detalle.config(state="disabled")

    def mostrar_detalle(self):
        datos = self.biblioteca.estadisticas()

        mensaje = (
            "DETALLE DE ESTADÍSTICAS\n\n"
            f"Total de libros: {datos.get('libros', 0)}\n"
            f"Total de usuarios: {datos.get('usuarios', 0)}\n"
            f"Préstamos activos: {datos.get('prestamos', 0)}\n"
            f"Libros disponibles: {datos.get('libros_disponibles', 0)}\n"
            f"Libros prestados: {datos.get('libros_prestados', 0)}\n"
            f"Usuarios en cola de espera: {datos.get('usuarios_en_cola', 0)}"
        )

        messagebox.showinfo("Estadísticas", mensaje)