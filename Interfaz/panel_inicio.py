import tkinter as tk

class PanelInicio(tk.Frame):

    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        tk.Label(self, text="Sistema de Gestión de Biblioteca", font=("Arial",24,"bold")).pack(pady=40)
        tk.Label(self, text="Seleccione una opción del menú").pack()