import os
import tkinter as tk
import re

if __name__=="__main__":
    import automata_identificadores as a_i
    import automata_numeros as a_n
else:
    from modulos import automata_identificadores as a_i
    from modulos import automata_numeros as a_n


    

    for palabra in re.findall(r'[!-~]+', contenido):
        
        #AQUI PONER O LLAMAR
        is_id=a_iden.automata(palabra)
        is_num=a_num.automata(palabra)

        if palabra in palabras_en_archivo:
            tokens_totales+=1
            start = "1.0"
            while True:
                start = texto.search(re.escape(palabra), start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(palabra)}c"
                if is_id:
                    texto.tag_add("id_highlight", start, end)
                elif is_num:
                    texto.tag_add("num_highlight", start, end)
                else:
                    texto.tag_add("highlight", start, end)
                start = end
                palabras_resaltadas.add(palabra)
        elif is_id:
            if tipo ==1:
                incrementar_rango()
                escribir_tabla(palabra)
            tokens_totales+=1
            start = "1.0"
            while True:
                start = texto.search(re.escape(palabra), start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(palabra)}c"
                texto.tag_add("id_highlight", start, end)
                start = end
                palabras_resaltadas.add(palabra)
        elif is_num:
            if tipo ==1:
                incrementar_rango()
                escribir_tabla(palabra)
            tokens_totales+=1
            start = "1.0"
            while True:
                start = texto.search(re.escape(palabra), start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(palabra)}c"
                texto.tag_add("num_highlight", start, end)
                start = end
                palabras_resaltadas.add(palabra)
        else:
            start = "1.0"
            while True:
                start = texto.search(re.escape(palabra), start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(palabra)}c"
                if tipo ==0:
                    texto.tag_add("err_light", start, end)
                else:
                    texto.tag_add("err_fin", start, end)
                start = end
            errores_totales+=1


    label_counter_tokens.config(text=str(tokens_totales))
    label_counter_errores.config(text=str(errores_totales))    
    return errores_totales , tokens_totales

if not os.path.exists(archivo):
    with open(archivo, "wb") as f:
        f.write(b" " * (TAM_REGISTRO * 10))



if __name__=="__main__":
    #escribir_dato_counter(0, "160") 
    """
    escribir_dato(0, "citrusint")  #TIPO DATO
    escribir_dato(1, "tanglyfl")    #TIPO DATO
    escribir_dato(2, "peelstr")     #TIPO DATO
    escribir_dato(3, "scent")       #TIPO DATO
    escribir_dato(4, "sweetbool")   #TIPO DATO
    escribir_dato(5, "juice")       #FUNCION    juice()[]
    escribir_dato(6, "craterray")   #ARREGLO    craterray{}
    escribir_dato(7, "zest")        #IF         zest()[]    if(){}
    escribir_dato(8, "pulpest")     #ELSE IF    pulpest()[]     else if(){}
    escribir_dato(9, "pulp")        #ELSE       pulp[]  else{}
    escribir_dato(10, "segment")    #SWITCH     segment()[] switch(){}
    escribir_dato(11, "squeeze")    #CASE       squeeze #   case:
    escribir_dato(12, "stop")       #BREAK      stop    break
    escribir_dato(13, "peel")       #DEFAULT    peel #   default:
    escribir_dato(14, "drip")       #WHILE      drip()[]    while(){}
    escribir_dato(15, "press")      #DO         press[]drip()   do{}while()
    escribir_dato(16, "cycle")      #FOR        cycle()[]   for(){}
    escribir_dato(17, "twist")      #RETURN     twist   return
    escribir_dato(18, "taste")      #TRY        taste[]bitter()[]   try{}catch(){}
    escribir_dato(19, "bitter")     #CATCH      taste[]bitter()[]   try{}catch(){}
    escribir_dato(20, "orange")     #CLASS      orange  class
    escribir_dato(21, "core")       #SUPER      core()    super()
    escribir_dato(22, "fuitof")     #EXTEND     fruitof     extend
    escribir_dato(23, "inherit")    #IMPLEMENT  inherit     implement
    escribir_dato(24, "hollow")     #NULL       hollow      null
    escribir_dato(25, "rise")       #NEW        rise        new
    escribir_dato(26, "slice")      #IMPORT     slice       import
    escribir_dato(27, "ever")       #CONST      ever        const
    escribir_dato(28, "and")        #&&         and     &&
    escribir_dato(29, "or")         #||         or      ||
    escribir_dato(30, "origin")     #ORIGEN     origin  (origen)
    escribir_dato(31, "absorb")     #CALL       absorb  (call)
    escribir_dato(32, "TAIL")       #END        TAIL    (end)

    escribir_dato(33, "true")       #true       true    true
    escribir_dato(34, "false")      #false      false   false
    escribir_dato(35, "LISTDEV")    #LIST P=    LISTDEV LIST P
    escribir_dato(36, "RADIX")      #RADIX      RADIX   RADIX
    escribir_dato(37, "EQU")        #EQU        EQU     EQU
    escribir_dato(38, "START")      #START      START   START
    escribir_dato(39, "HEX_")        #HEX
    escribir_dato(40, "OCT_")        #HEX
    escribir_dato(41, "BIN_")        #HEX
    escribir_dato(42, "$CONFIGURE")
    escribir_dato(43, "$END_CONFIGURE")   
    escribir_dato(44, "$PORT")


    

    escribir_dato(45, "=")
    escribir_dato(46, "*")
    escribir_dato(47, "+")
    escribir_dato(48, "[")
    escribir_dato(49, "]")
    escribir_dato(50, "(")
    escribir_dato(51, ")")
    escribir_dato(52, "{")
    escribir_dato(53, "}")
    escribir_dato(54, "*=")
    escribir_dato(55, "/")
    escribir_dato(56, "/=")
    escribir_dato(57, "==")
    escribir_dato(58, "+=")
    escribir_dato(59, "-=")
    escribir_dato(60, ";")
    escribir_dato(61, "-")

    """

    root = tk.Tk()
    root.title("Resaltado de Palabras en Tkinter")
    contador_tokens=0

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)
    navbar = tk.Frame(main_frame, bg="#2e2e2e", width=150)
    navbar.pack(side="left", fill="y")
    label_tokens = tk.Label(navbar,text="Tokens:",font=("Arial",12),bg="blue")
    label_tokens.pack(pady=20)

    label_counter_tokens = tk.Label(navbar,text=contador_tokens,font=("Arial",12),bg="blue")
    label_counter_tokens.pack(pady=20)

    label_err = tk.Label(navbar,text="Errs:",font=("Arial",12),bg="red")
    label_err.pack(pady=20)

    label_counter_err = tk.Label(navbar,text=contador_tokens,font=("Arial",12),bg="red")
    label_counter_err.pack(pady=20)


    texto = tk.Text(root, height=10, width=40)
    texto.pack()
    texto.tag_configure("highlight",background="green" ,foreground="black")
    texto.tag_configure("id_highlight", background="blue", foreground="white")
    texto.tag_configure("num_highlight", background="yellow", foreground="black")
    texto.tag_configure("err_light", foreground="black" , underline=True)
    texto.tag_configure("err_fin", foreground="black" ,background="red")
    texto.bind("<KeyRelease>",lambda event: resaltar_palabras(texto,label_counter_tokens,label_counter_err,0,event))
    root.mainloop()
