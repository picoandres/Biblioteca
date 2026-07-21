import tkinter as tk
from tkinter import ttk, messagebox

class PanelHistorial(tk.Frame):

    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        self.crear_componentes()
        self.actualizar_tabla()

    def crear_componentes(self):
        titulo = tk.Label(
            self,
            text="Historial de Operaciones",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        subtitulo = tk.Label(
            self,
            text="Aquí se muestran las acciones registradas en la pila del sistema",
            fg="gray"
        )
        subtitulo.pack(pady=(0, 10))

        # Botones
        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(botones, text="Actualizar historial", command=self.actualizar_tabla).grid(row=0, column=0, padx=5)
        tk.Button(botones, text="Limpiar vista", command=self.limpiar_tabla).grid(row=0, column=1, padx=5)

        # Tabla de historial
        columnas = ("numero", "accion", "detalle")

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=14
        )

        self.tabla.heading("numero", text="N°")
        self.tabla.heading("accion", text="Acción")
        self.tabla.heading("detalle", text="Detalle")

        self.tabla.column("numero", width=60, anchor="center")
        self.tabla.column("accion", width=220, anchor="center")
        self.tabla.column("detalle", width=500, anchor="w")

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalle)


        # Detalle seleccionado
        marco_detalle = tk.LabelFrame(
            self,
            text="Detalle de la operación seleccionada",
            padx=10,
            pady=10
        )
        marco_detalle.pack(fill="x", padx=10, pady=(0, 10))

        self.lbl_accion = tk.Label(
            marco_detalle,
            text="Acción: ",
            anchor="w",
            justify="left",
            font=("Arial", 10, "bold")
        )
        self.lbl_accion.pack(fill="x", pady=2)

        self.lbl_detalle = tk.Label(
            marco_detalle,
            text="Detalle: ",
            anchor="w",
            justify="left",
            wraplength=900
        )
        self.lbl_detalle.pack(fill="x", pady=2)


    # MÉTODOS AUXILIARES
    def limpiar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.lbl_accion.config(text="Acción: ")
        self.lbl_detalle.config(text="Detalle: ")

    def actualizar_tabla(self):
        self.limpiar_tabla()

        historial = self.biblioteca.mostrar_historial()

        if not historial:
            return

        for i, registro in enumerate(historial, start=1):
            accion = registro.get("accion", "")
            detalle = registro.get("detalle", "")

            self.tabla.insert(
                "",
                "end",
                values=(i, accion, detalle)
            )

    def mostrar_detalle(self, event):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado, "values")

        if not datos:
            return

        numero = datos[0]
        accion = datos[1]
        detalle = datos[2]

        self.lbl_accion.config(text=f"Acción: {accion}")
        self.lbl_detalle.config(
            text=f"Detalle: {detalle}"
        )