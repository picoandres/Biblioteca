import tkinter as tk
from Interfaz.panel_inicio import PanelInicio
from Interfaz.panel_libros import PanelLibros
from Interfaz.panel_usuarios import PanelUsuarios
from Interfaz.panel_prestamos import PanelPrestamos
from Interfaz.panel_historial import PanelHistorial
from Interfaz.panel_estadisticas import PanelEstadisticas
from Interfaz.panel_arbol import PanelArbolLibros
from Gestores.biblioteca import Biblioteca


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.biblioteca = Biblioteca()
        self.title("Sistema de Biblioteca")
        self.geometry("1200x700")
        self.resizable(False, False)

        self.crear_estructura()
        self.crear_menu()
        self.mostrar_panel(PanelInicio)

    def crear_estructura(self):
        # Barra lateral
        self.menu = tk.Frame(
            self,
            width=220,
            bg="#2C3E50"
        )
        self.menu.pack(side="left", fill="y")

        # Área principal
        self.contenido = tk.Frame(
            self,
            bg="white"
        )
        self.contenido.pack(side="right", expand=True, fill="both")

    def crear_menu(self):
        # Título del menú
        tk.Label(
            self.menu,
            text="BIBLIOTECA",
            bg="#2C3E50",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Botón Inicio
        tk.Button(
            self.menu,
            text="Inicio",
            width=20,
            command=lambda: self.mostrar_panel(PanelInicio)
        ).pack(pady=5)

        # Botón Libros
        tk.Button(
            self.menu,
            text="Libros",
            width=20,
            command=lambda: self.mostrar_panel(PanelLibros)
        ).pack(pady=5)

        # Botón Usuarios
        tk.Button(
            self.menu,
            text="Usuarios",
            width=20,
            command=lambda: self.mostrar_panel(PanelUsuarios)
        ).pack(pady=5)

        # Botón Préstamos
        tk.Button(
            self.menu,
            text="Préstamos",
            width=20,
            command=lambda: self.mostrar_panel(PanelPrestamos)
        ).pack(pady=5)

        # Botón Historial
        tk.Button(
            self.menu,
            text="Historial",
            width=20,
            command=lambda: self.mostrar_panel(PanelHistorial)
        ).pack(pady=5)

        # Botón Estadísticas
        tk.Button(
            self.menu,
            text="Estadísticas",
            width=20,
            command=lambda: self.mostrar_panel(PanelEstadisticas)
        ).pack(pady=5)

        # Botón Árbol de Libros
        tk.Button(
            self.menu,
            text="Árbol de Libros",
            width=20,
            command=lambda: self.mostrar_panel(PanelArbolLibros)
        ).pack(pady=5)

    def mostrar_panel(self, panel):
        for widget in self.contenido.winfo_children():
            widget.destroy()

        panel(self.contenido, self.biblioteca).pack(
            expand=True,
            fill="both"
        )