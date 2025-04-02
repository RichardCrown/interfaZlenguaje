import tkinter as tk
from tkinter import ttk, messagebox


class VentanaInput(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Nombrar Nuevo Archivo")
        self.geometry("500x150")
        self.config(bg="#3c3c3c")
        self.entrada = tk.Entry(self, width=30)
        self.entrada.pack(pady=25)
        btn_ok = tk.Button(self, text="Aceptar", command=self.obtener_texto)
        btn_ok.pack(pady=15)
        self.texto = "" 

    def obtener_texto(self):
        self.texto = self.entrada.get()
        if self.texto:  
            self.destroy()  
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre para el archivo.")


class VisualizadorArchivos(ttk.Notebook):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.pack(side="right", fill="both", expand=True)


class Archivo(ttk.Frame):
    def __init__(self, visualizador_archivo, nombre):
        super().__init__(visualizador_archivo)
        self.nombre_archivo = f"{nombre}.utlitary"
        visualizador_archivo.add(self, text=self.nombre_archivo)
        self.crear_editor()

    def crear_editor(self):
        editor = tk.Text(self, wrap="none", bg="#1e1e1e", fg="white", insertbackground="white")
        editor.pack(fill="both", expand=True)


class Boton(tk.Button):
    def __init__(self, nav_bar, nombre, color, tamano, command=None):
        super().__init__(nav_bar, text=nombre, fg=color, bg="#3c3c3c", relief="flat", command=command)
        self.pack(fill="x", padx=10, pady=5)


def nuevo_archivo(root, visualizador_archivos):
    ventana_input = VentanaInput(root)
    root.wait_window(ventana_input)  
    if ventana_input.texto: 
        archivo = Archivo(visualizador_archivos, ventana_input.texto)
        messagebox.showinfo("Nuevo Archivo", f"Se ha creado un archivo: {ventana_input.texto}")
    else:
        messagebox.showwarning("Nuevo Archivo", "No se creó el archivo. El nombre estaba vacío.")


def abrir_archivo():
    messagebox.showinfo("Abrir Archivo", "Abrir un archivo existente")


def guardar_archivo():
    messagebox.showinfo("Guardar Archivo", "Guardar el archivo actual")


def salir(root):
    root.quit()


def mostrar_config():
    messagebox.showinfo("Configuración", "Abrir configuración")


def cambiar_fuente():
    messagebox.showinfo("Tema", "Cambiar el tema de la aplicación")


def acerca_de():
    messagebox.showinfo("Acerca de", "MiniIDE - Versión 1.0")


def main():
    root = tk.Tk()
    root.title("MiniIDE")
    root.geometry("1000x600")
    root.config(bg="#3c3c3c") 

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    menubar = tk.Menu(root,bg="black", fg="white",font=("Arial", 10, "bold"))

    style = ttk.Style()

    style.configure("TNotebook", background="black", tabbackground="black", foreground="white")
    style.configure("TNotebook.Tab", background="black", foreground="white", font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", "#333333")], foreground=[("selected", "white")])

    visualizador_archivos = VisualizadorArchivos(main_frame)

    file_opcion = tk.Menu(menubar, tearoff=0, bg="#3c3c3c", fg="white")  
    file_opcion.add_command(label="Nuevo", command=lambda: nuevo_archivo(root,visualizador_archivos), font=("Arial", 10, "bold"))
    file_opcion.add_command(label="Abrir", command=abrir_archivo, font=("Arial", 10, "bold"))
    file_opcion.add_command(label="Guardar", command=guardar_archivo, font=("Arial", 10, "bold"))
    file_opcion.add_separator()
    file_opcion.add_command(label="Salir", command=lambda: salir(root), font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Archivo", menu=file_opcion)

    opciones_menui = tk.Menu(menubar, tearoff=0,bg="#3c3c3c", fg="white")
    opciones_menui.add_command(label="Configuración", command=mostrar_config,font=("Arial", 10, "bold"))
    opciones_menui.add_command(label="Cambiar Fuente", command=cambiar_fuente,font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Opciones", menu=opciones_menui)

    compilar = tk.Menu(menubar, tearoff=0,bg="#3c3c3c", fg="white")
    compilar.add_command(label="Compilar",font=("Arial", 10, "bold"))
    compilar.add_command(label="...",font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Compilar", menu=compilar)

    help_menu = tk.Menu(menubar, tearoff=0,bg="#3c3c3c", fg="white")
    help_menu.add_command(label="Acerca de", command=acerca_de,font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Ayuda", menu=help_menu)

    root.config(menu=menubar)

    navbar = tk.Frame(main_frame, bg="#2e2e2e", width=150)
    navbar.pack(side="left", fill="y")

    boton_compilar = Boton(navbar, "Compilar", "White", 20)
    boton_guarddar = Boton(navbar, "Guardar", "White", 20)
    boton_ex = Boton(navbar, "...", "White", 20)

    root.mainloop()


if __name__ == "__main__":
    main()
