import tkinter as tk
from tkinter import ttk

class PanelArbolLibros(tk.Frame):
    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        self.recorrido_actual = "inorden"
        self.crear_componentes()
        self.mostrar_inorden()


    def crear_componentes(self):
        titulo = tk.Label(
            self,
            text="Recorridos del Árbol de Libros",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        subtitulo = tk.Label(
            self,
            text="Visualización de los recorridos y la estructura del árbol binario de búsqueda (BST) de libros.",
            fg="gray"
        )
        subtitulo.pack(pady=(0, 10))


        # Botones
        marco_botones = tk.Frame(self)
        marco_botones.pack(pady=10)

        tk.Button(marco_botones, text="Inorden", width=15, command=self.mostrar_inorden).grid(row=0, column=0, padx=5)
        tk.Button(marco_botones, text="Preorden", width=15, command=self.mostrar_preorden).grid(row=0, column=1, padx=5)
        tk.Button(marco_botones, text="Postorden", width=15, command=self.mostrar_postorden).grid(row=0, column=2, padx=5)
        tk.Button(marco_botones, text="Actualizar", width=15, command=self.actualizar_recorrido_actual).grid(row=0, column=3, padx=5)

        # Información del recorrido
        self.lbl_recorrido = tk.Label(
            self,
            text="Recorrido actual: Inorden",
            font=("Arial", 11, "bold")
        )
        self.lbl_recorrido.pack(pady=(10, 5))

        self.lbl_descripcion = tk.Label(
            self,
            text="Inorden: izquierda → raíz → derecha. Muestra los libros ordenados por código.",
            wraplength=1000,
            justify="left"
        )
        self.lbl_descripcion.pack(pady=(0, 10))


        # Tabla de libros de recorridos
        columnas = (
            "posicion",
            "codigo",
            "titulo",
            "autor",
            "categoria",
            "anio",
            "estado"
        )

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tabla.heading("posicion", text="Pos.")
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("titulo", text="Título")
        self.tabla.heading("autor", text="Autor")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("anio", text="Año")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("posicion", width=60, anchor="center")
        self.tabla.column("codigo", width=100, anchor="center")
        self.tabla.column("titulo", width=220, anchor="w")
        self.tabla.column("autor", width=180, anchor="w")
        self.tabla.column("categoria", width=150, anchor="center")
        self.tabla.column("anio", width=80, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Resumen del recorrido
        marco_resumen = tk.LabelFrame(
            self,
            text="Resumen del recorrido",
            padx=10,
            pady=10
        )
        marco_resumen.pack(fill="x", padx=10, pady=(0, 10))

        self.lbl_total = tk.Label(
            marco_resumen,
            text="Total de libros en el recorrido: 0",
            anchor="w",
            justify="left"
        )
        self.lbl_total.pack(fill="x")

        # Estructura del árbol
        marco_arbol = tk.LabelFrame(
            self,
            text="Estructura del árbol BST de libros",
            padx=10,
            pady=10
        )
        marco_arbol.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.texto_arbol = tk.Text(
            marco_arbol,
            height=12,
            wrap="none",
            font=("Consolas", 10)
        )
        self.texto_arbol.pack(fill="both", expand=True)


    # Métodos auxiliares
    def limpiar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)


    def cargar_tabla(self, libros):
        self.limpiar_tabla()

        for i, libro in enumerate(libros, start=1):
            estado = "Disponible" if libro.disponible else "Prestado"

            self.tabla.insert(
                "",
                "end",
                values=(
                    i,
                    libro.codigo,
                    libro.titulo,
                    libro.autor,
                    libro.categoria,
                    libro.anio,
                    estado
                )
            )

        self.lbl_total.config(
            text=f"Total de libros en el recorrido: {len(libros)}"
        )


    def actualizar_texto_arbol(self):
        estructura = self.biblioteca.representar_arbol_libros()

        self.texto_arbol.config(state="normal")
        self.texto_arbol.delete("1.0", tk.END)
        self.texto_arbol.insert("1.0", estructura)
        self.texto_arbol.config(state="disabled")

    # Recorridos inorden, preorden y postorden
    def mostrar_inorden(self):
        self.recorrido_actual = "inorden"
        libros = self.biblioteca.listar_libros_inorden()

        self.lbl_recorrido.config(
            text="Recorrido actual: Inorden"
        )
        self.lbl_descripcion.config(
            text="Inorden: izquierda → raíz → derecha. "
                 "Muestra los libros ordenados por código."
        )

        self.cargar_tabla(libros)
        self.actualizar_texto_arbol()


    def mostrar_preorden(self):
        self.recorrido_actual = "preorden"
        libros = self.biblioteca.listar_libros_preorden()

        self.lbl_recorrido.config(
            text="Recorrido actual: Preorden"
        )
        self.lbl_descripcion.config(
            text="Preorden: raíz → izquierda → derecha. "
                 "Muestra primero la raíz del árbol y luego sus subárboles."
        )

        self.cargar_tabla(libros)
        self.actualizar_texto_arbol()


    def mostrar_postorden(self):
        self.recorrido_actual = "postorden"
        libros = self.biblioteca.listar_libros_postorden()

        self.lbl_recorrido.config(
            text="Recorrido actual: Postorden"
        )
        self.lbl_descripcion.config(
            text="Postorden: izquierda → derecha → raíz. "
                 "Muestra primero los subárboles y al final la raíz."
        )

        self.cargar_tabla(libros)
        self.actualizar_texto_arbol()


    def actualizar_recorrido_actual(self):
        if self.recorrido_actual == "inorden":
            self.mostrar_inorden()

        elif self.recorrido_actual == "preorden":
            self.mostrar_preorden()

        elif self.recorrido_actual == "postorden":
            self.mostrar_postorden()