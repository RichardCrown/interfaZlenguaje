import tkinter as tk
from tkinter import ttk, messagebox


class VentanaInput(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Nombrar Nuevo Archivo")
        self.geometry("500x150")
        self.config(bg="#3c3c3c")
        label = tk.Label(self,text="Nombre del Archivo:",font=("Arial",12,"bold"),fg="white",bg="#3c3c3c")
        label.pack(pady=20)
        self.entrada = tk.Entry(self, width=30)
        self.entrada.pack(pady=5)
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
    def __init__(self, visualizador_archivo, nombre,label_counter_tokens,label_counter_err):
        super().__init__(visualizador_archivo)
        self.nombre_archivo = f"{nombre}.orange"
        visualizador_archivo.add(self, text=self.nombre_archivo)
        self.crear_editor(label_counter_tokens,label_counter_err)
        self.is_seleccionada=False

    def crear_editor(self,label_counter_tokens,label_counter_err):
        self.editor = tk.Text(self, wrap="none", bg="#1e1e1e", fg="white", insertbackground="white",font=("Arial", 15, "bold"))
        self.editor.pack(fill="both", expand=True)
        #self.editor.tag_configure("highlight",background="#66CDAA" ,foreground="black",font=("Arial", 15, "bold"))
        self.editor.tag_configure("highlight",background="green" ,foreground="white",font=("Arial", 15, "bold"))
        self.editor.tag_configure("id_highlight", background="blue", foreground="white",font=("Arial", 15, "bold"))
        self.editor.tag_configure("num_highlight", background="yellow", foreground="black",font=("Arial", 15, "bold"))
        self.editor.tag_configure("err_light", foreground="white" , underline=True,font=("Arial", 15, "bold"))
        self.editor.tag_configure("err_fin", foreground="white" , background="red",font=("Arial", 15, "bold"))
        self.editor.bind("<KeyRelease>",lambda event: tablex.resaltar_palabras(self.editor,label_counter_tokens,label_counter_err,0,event))

    def setSelecionada(self,opcion):
        self.is_seleccionada=opcion


class Boton(tk.Button):
    def __init__(self, nav_bar, nombre, color, tamano, command=None):
        super().__init__(nav_bar, text=nombre, fg=color, bg="#3c3c3c", relief="flat", command=command)
        self.pack(fill="x", padx=10, pady=5)


def actualizar_seleccion(visualizador_archivos, archivos_array):
    pestaña_activa = visualizador_archivos.select()  
    for archivo in archivos_array:
        if str(archivo) == str(pestaña_activa): 
            archivo.setSelecionada(True)
        else:
            archivo.setSelecionada(False)  



def nuevo_archivo(root, visualizador_archivos,archivos_array,label_counter_tokens,label_counter_err):
    ventana_input = VentanaInput(root)
    root.wait_window(ventana_input)  
    if ventana_input.texto: 
        archivo = Archivo(visualizador_archivos, ventana_input.texto,label_counter_tokens,label_counter_err)
        archivos_array.append(archivo)
        messagebox.showinfo("Nuevo Archivo", f"Se ha creado un archivo: {ventana_input.texto}.orange")
    else:
        messagebox.showwarning("Advertencia!!", "No se creó el archivo. El nombre estaba vacío.")
    


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
    root.title("MiniStudioIDE")
    root.geometry("1000x600")
    root.config(bg="#3c3c3c") 
    array_archivos=[]
    contador_errores=0
    contador_tokens=0


    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    menubar = tk.Menu(root,bg="#3c3c3c", fg="white",font=("Arial", 10, "bold"))

    style = ttk.Style()

    style.configure("TNotebook", background="black", tabbackground="black", foreground="white")
    style.configure("TNotebook.Tab", background="black", foreground="white", font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", "#333333")], foreground=[("selected", "white")])

    visualizador_archivos = VisualizadorArchivos(main_frame)
    cargar_imagen(visualizador_archivos)

    navbar = tk.Frame(main_frame, bg="#2e2e2e", width=150)
    navbar.pack(side="left", fill="y")

    boton_compilar = Boton(navbar, "Compilar", "White", 20,lambda: compilar_archivo(visualizador_archivos,label_counter_tokens,array_archivos,label_counter_err))
    boton_guarddar = Boton(navbar, "Guardar", "White", 20,lambda: guardar_archivo(array_archivos, visualizador_archivos))
    boton_abrir = Boton(navbar, "Abrir", "White", 20,lambda: abrir_archivo(array_archivos,visualizador_archivos,label_counter_tokens,label_counter_err))
    boton_delete_arch = Boton(navbar, "X", "White", 20,lambda: elim_archivo(visualizador_archivos,array_archivos,label_counter_tokens))
    boton_delete_arch.config(bg="#660000")
    boton_compilar.config(bg="#000066")

    label_errores = tk.Label(navbar,text="Errores:",font=("Arial",12),bg="red")
    label_errores.pack(pady=20)

    label_counter_err = tk.Label(navbar,text=contador_errores,font=("Arial",12),bg="red")
    label_counter_err.pack(pady=20)

    label_tokens = tk.Label(navbar,text="Tokens:",font=("Arial",12),bg="blue")
    label_tokens.pack(pady=20)

    label_counter_tokens = tk.Label(navbar,text=contador_tokens,font=("Arial",12),bg="blue")
    label_counter_tokens.pack(pady=20)

    file_opcion = tk.Menu(menubar, tearoff=0, bg="#3c3c3c", fg="white")  
    file_opcion.add_command(label="Nuevo", command=lambda: nuevo_archivo(root, visualizador_archivos, array_archivos, label_counter_tokens,label_counter_err), font=("Arial", 10, "bold"))
    file_opcion.add_command(label="Abrir", command=lambda: abrir_archivo(array_archivos,visualizador_archivos,label_counter_tokens,label_counter_err), font=("Arial", 10, "bold"))
    file_opcion.add_command(label="Guardar",command=lambda: guardar_archivo(array_archivos, visualizador_archivos), font=("Arial", 10, "bold"))
    file_opcion.add_separator()
    file_opcion.add_command(label="Cerrar",command=lambda: elim_archivo(visualizador_archivos,array_archivos,label_counter_tokens), font=("Arial", 10, "bold"))
    file_opcion.add_command(label="Salir", command=lambda: salir(root), font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Archivo", menu=file_opcion)

    opciones_menui = tk.Menu(menubar, tearoff=0,bg="#3c3c3c", fg="white")
    opciones_menui.add_command(label="Configuración", command=mostrar_config,font=("Arial", 10, "bold"))
    opciones_menui.add_command(label="Tabla Simbolos", command=tablasimbolos,font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Opciones", menu=opciones_menui)

    compilar = tk.Menu(menubar, tearoff=0,bg="#3c3c3c", fg="white")
    compilar.add_command(label="Compilar",font=("Arial", 10, "bold"),command= lambda: compilar_archivo(visualizador_archivos,label_counter_tokens,array_archivos,label_counter_err))
    compilar.add_command(label="...",font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Compilar", menu=compilar)

    help_menu = tk.Menu(menubar, tearoff=0,bg="#3c3c3c", fg="white")
    help_menu.add_command(label="Acerca de", command=acerca_de,font=("Arial", 10, "bold"))
    menubar.add_cascade(label="Ayuda", menu=help_menu)

    root.config(menu=menubar)


    boton_salir= Boton(navbar, "Salir", "White", 20,lambda: salir(root))
    boton_salir.config(bg="black")


    root.mainloop()


if __name__ == "__main__":
    main()
