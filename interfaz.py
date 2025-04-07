import tkinter as tk
from tkinter import ttk, messagebox,filedialog
from PIL import Image, ImageTk
from modulos import creacion_tabla as tablex

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
    


def cargar_imagen(notebook):
    imagen = Image.open("imagenes/logo.png")  
    imagen = imagen.resize((150, 150), Image.Resampling.LANCZOS) 
    imagen_tk = ImageTk.PhotoImage(imagen)

    label_imagen = tk.Label(notebook, image=imagen_tk, bg="black")
    label_imagen.image = imagen_tk 
    label_imagen.place(relx=0.5, rely=0.5, anchor="center")

def abrir_archivo(array_archivos,visualizador_archivos,label_counter_tokens,label_counter_err):
    actualizar_seleccion(visualizador_archivos,array_archivos)
    texter=None
    for arch in array_archivos:
        if arch.is_seleccionada==True:
            texter=arch.editor
            break
    archivo = filedialog.askopenfilename(filetypes=[("Archivos Txt","*.txt")])
    if archivo:
        with open(archivo,"r",encoding="utf-8") as f:
            contenido=f.read()
    else: 
        messagebox.showwarning("Mensaje del Sistema", "No se selecciono contenido.")
        return

    if texter != None:
        texter.delete("1.0",tk.END)
        texter.insert(tk.END,contenido)
        tablex.resaltar_palabras(texter,label_counter_tokens,label_counter_err,0)
    else:
        nombre_archivo = archivo.split("/")[-1].split("\\")[-1].split(".")[0]
        archivo_new = Archivo(visualizador_archivos,nombre_archivo,label_counter_tokens,label_counter_err)
        archivo_new.editor.delete("1.0",tk.END)
        archivo_new.editor.insert(tk.END,contenido)
        tablex.resaltar_palabras(archivo_new.editor,label_counter_tokens,label_counter_err,0)
        array_archivos.append(archivo_new)
        messagebox.showwarning("Mensaje del Sistema", "Se creo un Archivo.")

def elim_archivo(visualizador_archivos,array_archivos,label_counter_tokens):
    actualizar_seleccion(visualizador_archivos,array_archivos)
    for arch in array_archivos:
        if arch.is_seleccionada:
            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que deseas cerrar {arch.nombre_archivo}? puede que sus cambios no se guarden")
            if confirmar:
                label_counter_tokens.config(text="0") 
                index = visualizador_archivos.index(arch)
                visualizador_archivos.forget(index)
                array_archivos.remove(arch)
            break

def guardar_archivo(array_archivos, visualizador_archivos):
    actualizar_seleccion(visualizador_archivos, array_archivos)
    for arch in array_archivos:
        if arch.is_seleccionada:
            contenido = arch.editor.get("1.0", tk.END)  
            archivo_guardar = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt")],
                initialfile=arch.nombre_archivo.replace(".orange", ".txt")
            )

            if archivo_guardar:
                with open(archivo_guardar, "w", encoding="utf-8") as f:
                    f.write(contenido)

                messagebox.showinfo("Guardar Archivo", f"El archivo se ha guardado correctamente como:\n{archivo_guardar}")
            return

    messagebox.showwarning("Guardar Archivo", "No hay un archivo seleccionado para guardar.")



def salir(root):
    root.quit()


def mostrar_config():
    messagebox.showinfo("Configuración", "Abrir configuración")


def tablasimbolos():
    messagebox.showinfo("Tabla de Simbolos", "ORANGE.CONF")



def acerca_de():
    messagebox.showinfo("Acerca de", "MiniStudioIDE - Versión 3.0") 

def compilar_archivo(visualizador_archivos,label_counter_tokens,array_archivos,label_counter_err):
    actualizar_seleccion(visualizador_archivos,array_archivos)
    editor=None
    errores=0
    tokens=0
    for arch in array_archivos:
        print(arch.is_seleccionada)
        if arch.is_seleccionada==True:
            editor = arch.editor
            errores , tokens = tablex.resaltar_palabras(editor,label_counter_tokens,label_counter_err,1)
            messagebox.showinfo("Mensaje Sistema", f"Se compiló el código con: {errores} errores y con: {tokens} tokens identificados.")
            return 0
    messagebox.showwarning("Mensaje Sistema", "No hay archivo a compilar!!")


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
