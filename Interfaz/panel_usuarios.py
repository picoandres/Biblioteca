import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class PanelUsuarios(tk.Frame):

    def __init__(self, master, biblioteca):
        super().__init__(master)
        self.biblioteca = biblioteca
        self.crear_componentes()
        self.actualizar_tabla()

    def crear_componentes(self):
        titulo = tk.Label(
            self,
            text="Gestión de Usuarios",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Formulario
        formulario = tk.Frame(self)
        formulario.pack(pady=10)

        tk.Label(formulario, text="Cédula").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cedula = tk.Entry(formulario)
        self.cedula.grid(row=0, column=1, padx=5)

        tk.Label(formulario, text="Nombre").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.nombre = tk.Entry(formulario)
        self.nombre.grid(row=1, column=1, padx=5)

        tk.Label(formulario, text="Apellido").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.apellido = tk.Entry(formulario)
        self.apellido.grid(row=2, column=1, padx=5)

        tk.Label(formulario, text="Correo").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.correo = tk.Entry(formulario)
        self.correo.grid(row=3, column=1, padx=5)

        tk.Label(formulario, text="Teléfono").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.telefono = tk.Entry(formulario)
        self.telefono.grid(row=4, column=1, padx=5)

        tk.Label(formulario, text="La cédula del usuario no se puede modificar al editar", fg="gray").grid(row=5, column=0, columnspan=2, pady=5)


        # Botones
        botones = tk.Frame(self)
        botones.pack(pady=10)

        tk.Button(botones, text="Registrar", command=self.registrar_usuario).grid(row=0, column=0, padx=5)
        tk.Button(botones, text="Buscar", command=self.buscar_usuario).grid(row=0, column=1, padx=5)
        tk.Button(botones, text="Eliminar", command=self.eliminar_usuario).grid(row=0, column=2, padx=5)
        tk.Button(botones, text="Editar", command=self.editar_usuario).grid(row=0, column=3, padx=5)
        tk.Button(botones, text="Actualizar Lista", command=self.actualizar_tabla).grid(row=0, column=4, padx=5)

        # Tabla de usuarios
        columnas = ("cedula", "nombre", "apellido", "correo", "telefono")

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=12
        )

        for columna in columnas:
            self.tabla.heading(columna, text=columna.capitalize())
            self.tabla.column(columna, width=180, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabla.bind("<Double-1>", self.seleccionar_usuario)

    def obtener_datos_formulario(self):
        return (
            self.cedula.get().strip(),
            self.nombre.get().strip(),
            self.apellido.get().strip(),
            self.correo.get().strip(),
            self.telefono.get().strip()
        )

    def limpiar_campos(self):
        self.desbloquear_cedula()
        self.cedula.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.apellido.delete(0, tk.END)
        self.correo.delete(0, tk.END)
        self.telefono.delete(0, tk.END)

    def bloquear_cedula(self):
        self.cedula.config(state="disabled")

    def desbloquear_cedula(self):
        self.cedula.config(state="normal")

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for usuario in self.biblioteca.listar_usuarios():
            self.tabla.insert(
                "",
                "end",
                values=(
                    usuario.cedula,
                    usuario.nombre,
                    usuario.apellido,
                    usuario.correo,
                    usuario.telefono
                )
            )

    def seleccionar_usuario(self, event):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado, "values")

        if not datos:
            return

        self.limpiar_campos()

        self.cedula.insert(0, datos[0])
        self.nombre.insert(0, datos[1])
        self.apellido.insert(0, datos[2])
        self.correo.insert(0, datos[3])
        self.telefono.insert(0, datos[4])
        self.bloquear_cedula()

    def registrar_usuario(self):
        cedula, nombre, apellido, correo, telefono = self.obtener_datos_formulario()

        if not cedula or not nombre or not apellido:
            messagebox.showerror(
                "Error",
                "Complete los campos obligatorios"
            )
            return

        exito, mensaje = self.biblioteca.registrar_usuario(
            cedula,
            nombre,
            apellido,
            correo,
            telefono
        )

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", mensaje)


    def buscar_usuario(self):
        cedula = simpledialog.askstring("Buscar Usuario", "Ingrese la cédula del usuario:")

        if not cedula or not cedula.strip():
            if cedula is not None and not cedula.strip():
                messagebox.showwarning("Buscar", "Debe ingresar una cédula válida.")
            return

        cedula = cedula.strip()
        usuario = self.biblioteca.buscar_usuario(cedula)

        if usuario is None:
            messagebox.showerror("Error", "Usuario no encontrado")
            return

        # Cargar datos en la interfaz
        self.limpiar_campos()
        self.cedula.insert(0, usuario.cedula)
        self.nombre.insert(0, usuario.nombre)
        self.apellido.insert(0, usuario.apellido)
        self.correo.insert(0, usuario.correo)
        self.telefono.insert(0, usuario.telefono)
        self.bloquear_cedula()

        # Ventana flotante con los datos del usuario
        info_usuario = (
            f" Usuario Encontrado \n\n"
            f"• Cédula: {usuario.cedula}\n"
            f"• Nombre: {usuario.nombre} {usuario.apellido}\n"
            f"• Correo: {usuario.correo}\n"
            f"• Teléfono: {usuario.telefono}"
        )
        messagebox.showinfo("Detalles del Usuario", info_usuario)

    def eliminar_usuario(self):
        cedula = self.cedula.get().strip()

        if not cedula:
            messagebox.showwarning(
                "Eliminar",
                "Ingrese la cédula del usuario"
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar este usuario?"
        )

        if not respuesta:
            return

        exito, mensaje = self.biblioteca.eliminar_usuario(cedula)

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    def editar_usuario(self):
        # Si la cédula no está cargada en el formulario, la pide mediante la ventana flotante
        cedula_actual = self.cedula.get().strip()

        if not cedula_actual:
            cedula_actual = simpledialog.askstring("Editar Usuario", "Ingrese la cédula del usuario a editar:")
            
            # Si presiona "Cancelar" o deja la casilla vacía
            if not cedula_actual or not cedula_actual.strip():
                if cedula_actual is not None and not cedula_actual.strip():
                    messagebox.showwarning("Editar Usuario", "Debe ingresar una cédula válida.")
                return

            cedula_actual = cedula_actual.strip()
            
            # Buscar el usuario en la base de datos/sistema
            usuario = self.biblioteca.buscar_usuario(cedula_actual)
            if usuario is None:
                messagebox.showerror("Error", "Usuario no encontrado")
                return
            
            # Limpia los campos y carga la información encontrada
            self.limpiar_campos()
            self.cedula.insert(0, usuario.cedula)
            self.nombre.insert(0, usuario.nombre)
            self.apellido.insert(0, usuario.apellido)
            self.correo.insert(0, usuario.correo)
            self.telefono.insert(0, usuario.telefono)
            self.bloquear_cedula()

        # Si la cédula ya está cargada en la interfaz, lee los datos modificados del formulario
        cedula, nombre, apellido, correo, telefono = self.obtener_datos_formulario()

        if not nombre:
            messagebox.showwarning(
                "Editar usuario",
                "El nombre es obligatorio"
            )
            return

        # Guardar los cambios actualizados
        exito, mensaje = self.biblioteca.editar_usuario(
            cedula,
            nombre,
            apellido,
            correo,
            telefono
        )

        if exito:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)
        


    
