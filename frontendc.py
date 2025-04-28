import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from backendc import Persona, Cliente, Trabajador, Producto, Bebida, Pedido, Personalizacion
import os

Persona.cargar_usuarios()
Cliente.cargar_clientes()
Trabajador.cargar_trabajadores()
Producto.cargar_productos()
Bebida.cargar_bebidas()
Pedido.cargar_pedidos()
Personalizacion.cargar_personalizaciones()


def ventana_principal():
    global root
    root = tk.Tk()
    root.title("Sistema de pedidos de Cafeteria")
    root.geometry("900x700+0+0")
    root.iconbitmap("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//cafeteria.ico")

    try:
        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondocafe.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
        fondo_label = tk.Label(root, image=imagen_fondo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error al cargar imagen de fondo: {e}")

    titulo = tk.Label(root, text="Cafeteria", font=("Helvetica", 24, "bold"), bg="white", fg="navy")
    titulo.place(relx=0.5, rely=0.1, anchor="center")

    frame_botones = tk.Frame(root, bg="white", bd=5, relief="solid")
    frame_botones.place(relx=0.5, rely=0.5, anchor="center")

    def abrir_cliente():
        root.withdraw()
        ventana_cliente()

    def abrir_trabajador():
        root.withdraw()
        ventana_trabajador()

    boton_cliente = tk.Button(frame_botones, text="Cliente", command=abrir_cliente, width=20, height=3, 
                            font=("Helvetica", 14, "bold"), bg="lightblue", fg="black")
    boton_cliente.pack(pady=10)

    boton_trabajador = tk.Button(frame_botones, text="Trabajador", command=abrir_trabajador, width=20, height=3, 
                               font=("Helvetica", 14, "bold"), bg="lightblue", fg="black")
    boton_trabajador.pack(pady=10)

    root.mainloop()


def ventana_cliente():
    cliente_window = tk.Toplevel()
    cliente_window.title("Ventana de clientes")
    cliente_window.geometry("900x700")

    imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondocliente.jpg")
    imagen_fondo = imagen_fondo.resize((900,700))
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    fondo_label = tk.Label(cliente_window, image=imagen_fondo)
    fondo_label.image = imagen_fondo
    fondo_label.place(x=0,y=0, relwidth=1, relheight=1)

    producto_map = {"Pastel de chocolate": "prod001", "Pastel de fresas": "prod002", "Pastel de piña": "prod003", "Galletas": "prod004", "Dona de chocolate": "prod005", "Dona de azucar glass": "prod006", "Pay de queso": "prod007", "Pay de manzana": "prod008", "Pay de calabaza": "prod009", "Flan": "prod010"}
    bebida_map = {"Cafe Americano": "beb001", "Cafe latte": "beb002", "Té verde": "beb003", "Jugo de naranja": "beb004", "Agua mineral": "beb005"}

    boton_regresar = tk.Button(cliente_window,text="Regresar", command=lambda: [cliente_window.destroy(), root.deiconify()], bg="lightblue", font=("Helvetica", 12, "bold"))
    boton_regresar.place(relx=0.05, rely=0.9)

    frame_registro = tk.Frame(cliente_window, bg="white", bd=5, relief="solid")
    frame_registro.place(relx=0.5, rely=0.3, anchor="center")
    
    global Lista_productos, Lista_bebidas, entry_id_cliente
    
    tk.Label(frame_registro, text="ID Cliente:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_id_cliente = tk.Entry(frame_registro)
    entry_id_cliente.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(frame_registro, text="Registro de Cliente", font=("Helvetica", 14, "bold")).grid(row=0, columnspan=2, pady=10)

    tk.Label(frame_registro, text="ID:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_id = tk.Entry(frame_registro)
    entry_id.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_registro, text="Nombre:").grid(row=2,column=0, sticky="e", padx=5, pady=5)
    entry_nombre = tk.Entry(frame_registro)
    entry_nombre.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_registro, text="Edad:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_edad = tk.Entry(frame_registro)
    entry_edad.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame_registro, text="Alergias:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_alergias = tk.Entry(frame_registro)
    entry_alergias.grid(row=4, column=1, padx=5, pady=5)
    
    def obtener_productos_seleccionados():
        """Obtiene los IDS de los productos seleccionados de la interfaz"""
        try:
            if 'Listaproductos' in globals() and Lista_productos.curselection():
                seleccionados =  [Lista_productos.get(i) for i in Lista_productos.curselection()]
                return [producto_map[nombre] for nombre in seleccionados if nombre in producto_map]
        except Exception as e:
            print(f"Error al obtener productos seleccionados: {e}")
        return []
    
    def obtener_bebidas_seleccionadas():
        """Obtiene los IDS de las bebidas seleccionads en la interfaz"""
        try:
            if 'Lista_bebidas' in globals() and Lista_bebidas.curselection():
                seleccionados = [Lista_bebidas.get(i) for i in Lista_bebidas.curselection()]
                return [bebida_map[nombre] for nombre in seleccionados if nombre in bebida_map]
        except Exception as e:
            print(f"Error al obtener bebidas seleccionadas: {e}")
        return []

    def registrar_cliente():
        id_cliente = entry_id.get()
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        alergias = entry_alergias.get()

        if not id_cliente or not nombre or not edad:
            messagebox.showerror("Error", "ID, Nombre y Edad son campos obligatorios")
            return
        
        try:
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número")
            return
        
        for cliente in Cliente.Lista_clientes:
            if cliente.id == id_cliente:
                messagebox.showerror("Error", "El ID ya está registrado")
                return
            
        nuevo_cliente = Cliente(id_cliente, nombre, "Cliente", edad, alergias)
        Cliente.guardar_clientes()
        Persona.guardar_usuarios()

        messagebox.showinfo("Exito", "Cliente registrado correctamente")
        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_alergias.delete(0, tk.END)

    btn_registrar = tk.Button(frame_registro, text="Registrar", command=registrar_cliente)
    btn_registrar.grid(row=5, columnspan=2, pady=10)

    def ver_lista_clientes():
        ventana_lista = tk.Toplevel()
        ventana_lista.title("Lista de clientes")
        ventana_lista.geometry("800x600")

        tree = ttk.Treeview(ventana_lista, columns=("ID","Nombre", "Edad", "Alergias"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Edad", text="Edad")
        tree.heading("Alergias", text="Alergias")

        Cliente.cargar_clientes()

        for cliente in Cliente.Lista_clientes:
            tree.insert("", tk.END, values=(cliente['id'], cliente['nombre'], cliente['edad'], cliente.get('alergias', '')))

        tree.pack(expand=True, fill="both", padx=20, pady=20)

    def seleccionar_productos():

        ventana_selec_prod = tk.Toplevel(cliente_window)
        ventana_selec_prod.title("Seleccionar Producto")
        ventana_selec_prod.geometry("900x700")

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondopostres.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label = tk.Label(ventana_selec_prod, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame_productos = tk.Frame(ventana_selec_prod, bg="white", bd=5, relief="solid")
        frame_productos.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        tk.Label(frame_productos, text="Seleccione sus productos", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        productos = ["Pastel de chocolate","Pastel de fresas", "Pastel de piña", "Galletas", "Dona de chocolate", "Dona de azucar glass", "Pay de queso", "Pay de manzana", "Pay de calabaza", "Flan"]

        producto_map = {"Pastel de chocolate": "prod001", "Pastel de fresas": "prod002", "Pastel de piña": "prod003", "Galletas": "prod004", "Dona de chocolate": "prod005", "Dona de azucar glass": "prod006", "Pay de queso": "prod007", "Pay de manzana": "prod008", "Pay de calabaza": "prod009", "Flan": "prod010"}

        Lista_productos = tk.Listbox(frame_productos, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        for producto in productos:
            Lista_productos.insert(tk.END, producto)
        Lista_productos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        productos_seleccionados = []
        
        def agregar_al_pedido():
            seleccionados = [Lista_productos.get(i) for i in Lista_productos.curselection()]
            if seleccionados:
                messagebox.showinfo("Productos selecionados", f"Has seleccionado: {','.join(seleccionados)}")
            else:
                messagebox.showwarning("Advertencia", "No has seleccionado ningun producto")

        tk.Button(frame_productos, text="Agregar al pedido", command=agregar_al_pedido, bg="lightgreen").pack(pady=10)

    def seleccionar_bebidas():
        
        ventana_selec_bebi = tk.Toplevel(cliente_window)
        ventana_selec_bebi.title("Seleccionar Bebida")
        ventana_selec_bebi.geometry("900x700")

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondobebidas.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label = tk.Label(ventana_selec_bebi, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0,y=0, relwidth=1, relheight=1)

        frame_bebidas = tk.Frame(ventana_selec_bebi, bg="white", bd=5, relief="solid")
        frame_bebidas.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        tk.Label(frame_bebidas, text="Seleciione sus bebidas", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        bebidas = ["Cafe Americano", "Cafe latte", "Té verde", "Jugo de naranja", "Agua mineral"]
        Lista_bebidas = tk.Listbox(frame_bebidas, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        for bebida in bebidas:
            Lista_bebidas.insert(tk.END, bebida)
        Lista_bebidas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        def agregar_al_pedido():
            seleccionados = [Lista_bebidas.get(i) for i in Lista_bebidas.curselection()]
            
            if seleccionados:
                messagebox.showinfo("Bebidas seleccionadas", f"Has seleccionado:{''.join(seleccionados)}")
            else:
                messagebox.showwarning("Advertencia", "No has seleccionado ninguna bebida")

        tk.Button(frame_bebidas, text="Agregar al pedido", command=agregar_al_pedido, bg="lightblue").pack(pady=10)

        def finalizar_pedido():
            id_cliente =  entry_id_cliente.get()
            if not id_cliente:
                messagebox.showerror("Error", "Debe ingresar in ID de cliente")
                return
            
            productos = obtener_productos_seleccionados()
            bebidas = obtener_bebidas_seleccionadas()

            if not productos and not bebidas:
                messagebox.showerror("Error", "Debe seleccionar al menos un producto o bebida")
                return

            try:
                pedido = Pedido.crear_pedido(id_cliente, productos, bebidas)
                messagebox.showinfo("Exito", f"Pedido #{pedido['id']} creado!\nTotal:${pedido['total']:.2f}")

                if 'Lista_productos' in globals():
                    Lista_productos.selection_clear(0, tk.END)
                if 'Lista_bebidas' in globals():
                    Lista_bebidas.selection_clear(0, tk.END)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el pedido: {str(e)}")

        boton_finalizar = tk.Button(cliente_window, text="Finalizar Pedido", command=finalizar_pedido, width=20, height=3)
        boton_finalizar.place(x=50, y=550)

    def personalizar_productos():
        ventana_pers_prod = tk.Toplevel(cliente_window)
        ventana_pers_prod.title("Personalizar Producto")
        ventana_pers_prod.geometry("900x700")

        base_var = tk.StringVar()
        extras_vars = {"Chocolate": tk.BooleanVar(), "Frutas": tk.BooleanVar(),"Crema batida": tk.BooleanVar(), "Nueces": tk.BooleanVar(), "Caramelo": tk.BooleanVar()}
        notas_var = tk.StringVar()

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondopostres.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label = tk.Label(ventana_pers_prod, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame_pers = tk.Frame(ventana_pers_prod, bg="white", bd=5, relief="solid")
        frame_pers.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        tk.Label(frame_pers, text="Personalice su producto", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        tk.Label(frame_pers, text="Selecciones un producto base:", bg="white").pack()
        productos_base = ["Pastel", "Galletas", "Donas", "Pay"]
        combo_productos = ttk.Combobox(frame_pers, textvariable=base_var, values=productos_base, state="readonly")
        combo_productos.pack(pady=5)

        tk.Label(frame_pers, text="Selecccione ingredientes extras:", bg="white").pack()
        
        for ingrediente, var in extras_vars.items():
            cb = tk.Checkbutton(frame_pers, text=ingrediente, variable=var, bg="white")
            cb.pack(anchor="w", padx=50)
        
        tk.Label(frame_pers, text="Notas especiales", bg="white").pack()
        entry_notas = tk.Entry(frame_pers, textvariable=notas_var, width=40)
        entry_notas.pack(pady=5)
    
        def obtener_id_pedido_actual():
            """Obtiene el ID del ultimo pedido por el cliente"""
            if Pedido.Lista_pedidos:
                return str(max(int(p['id']) for p in Pedido.Lista_pedidos))
            return None

        def confirmar_personalizacion():
            base = base_var.get()
            extras = [ingrediente for ingrediente, var in extras_vars.items() if var.get()]
            notas = notas_var.get()

            if not base:
                messagebox.showerror("Error", "Debe seleccionar un producto base")
                return
            
            id_pedido = obtener_id_pedido_actual()

            nueva_personalizacion = Personalizacion( id_pedido=id_pedido, tipo="producto", base=base, extras=extras, notas=notas)
            messagebox.showinfo("Personalizacion","Producto personalizado guardado!")
            ventana_pers_prod.destroy()
            

        tk.Button(frame_pers, text="Confirmar", command=confirmar_personalizacion, bg="lighgreen").pack(pady=15)

    def personalizar_bebidas():
        ventana_pers_bebi = tk.Toplevel(cliente_window)
        ventana_pers_bebi.title("Personalizar Bebida")
        ventana_pers_bebi.geometry("900x700")

        base_var = tk.StringVar()
        modificadores_vars = {"Leche": tk.BooleanVar(), "Azucar": tk.BooleanVar(), "Edulcorante": tk.BooleanVar(), "Hielo": tk.BooleanVar(), "Canela": tk.BooleanVar()}
        intensidad_var = tk.IntVar(value=3)
        notas_var = tk.StringVar()

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondobebidas.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label=tk.Label(ventana_pers_bebi, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame_pers = tk.Frame(ventana_pers_bebi, bg="white", bd=5, relief="solid")
        frame_pers.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        tk.Label(frame_pers, text="Personalice su bebida", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(frame_pers, text="Seleccione una bebida base:", bg="white").pack()
        bebidas_base=["Cafe","Te", "Chocolate caliente", "Jugo natural"]
        combo_bebidas = ttk.Combobox(frame_pers, textvariable=base_var, values=bebidas_base, state="readonly")
        combo_bebidas.pack(pady=5)

        tk.Label(frame_pers, text="Selecciones modificadores", bg="white").pack()
        
        for modificador, var in modificadores_vars.items():
            cb = tk.Checkbutton(frame_pers, text=modificador, variable=var, bg="white")
            cb.pack(anchor="w", padx=50)

        tk.Label(frame_pers, text="Intensidad", bg="white").pack()
        tk.Scale(frame_pers, from_=1, to=5, orient="horizontal", variable=intensidad_var, bg="white").pack()

        tk.Label(frame_pers, text="Notas especiales:", bg="white").pack()
        tk.Entry(frame_pers, textvariable=notas_var, width=40).pack(pady=5)

        def confirmar_personalizacion():
            base = base_var.get()
            modificadores = [mod for mod, var in modificadores_vars.items() if var.get()]
            intensidad = intensidad_var.get()
            notas = notas_var.get()

            if not base:
                messagebox.showerror("Error", "Debe seleccionar una bebida base")
                return
            
            id_pedido = obtener_id_pedido_actual()
            
            nueva_personalizacion = Personalizacion( id_pedido= id_pedido, tipo="bebida", base=base, extras={ "modificadores": modificadores, "intensidad": intensidad}, notas = notas)
            messagebox.showinfo("Personalizacion", "Bebida personalizada guardada!")
            ventana_pers_bebi.destroy()
        
        def obtener_id_pedido_actual():
            """Obtiene el ID del ultimo pedido por el cliente"""
            if Pedido.Lista_pedidos:
                return str(max(int(p['id']) for p in Pedido.Lista_pedidos))
            return None
            
        tk.Button(frame_pers, text="Confirmar", command=confirmar_personalizacion, bg="lightblue").pack(pady=15)

        
    boton_seleccionar_productos = tk.Button(cliente_window, text="Seleccionar producto", command=seleccionar_productos, width=20, height=3)
    boton_seleccionar_productos.place(x=50, y=50)

    boton_seleccionar_bebidas = tk.Button(cliente_window, text="Seleccionar bebidas", command=seleccionar_bebidas, width=20, height=3)
    boton_seleccionar_bebidas.place(x=50, y=150)

    boton_personalizar_productos = tk.Button(cliente_window, text="Personalizar producto", command=personalizar_productos, width=20, height=3)
    boton_personalizar_productos.place(x=50, y=250)

    boton_personalizar_bebidas = tk.Button(cliente_window, text="Personalizar bebida", command=personalizar_bebidas, width=20, height=3)
    boton_personalizar_bebidas.place(x=50,y=350)

    boton_ver_clientes = tk.Button(cliente_window, text="Ver clientes", command=ver_lista_clientes, width=20, height=3)
    boton_ver_clientes.place(x=50, y=450)
    

    def on_closing():
        cliente_window.destroy()
        root.deiconify()
    
    cliente_window.protocol("WM_DELETE_WINDOW", on_closing)
    cliente_window.mainloop()
    pass

def ventana_trabajador():
    trabajador_window = tk.Toplevel()
    trabajador_window.title("Ventana de trabajadores")
    trabajador_window.geometry("900x700")

    imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondotrabajador.jpg")
    imagen_fondo = imagen_fondo.resize((900, 700))
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    fondo_label = tk.Label(trabajador_window, image=imagen_fondo)
    fondo_label.image = imagen_fondo
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
     
    boton_regresar = tk.Button(trabajador_window, text="Regresar", command=lambda: [trabajador_window.destroy(), root.deiconify()], bg="lightblue", font=("Helvetica", 12, "bold"))
    boton_regresar.place(relx=0.05, rely=0.9)

    frame_botones = tk.Frame(trabajador_window, bg="white", bd=5, relief="solid")
    frame_botones.place(x=50, y=50, width=200, height=500)

    frame_registro = tk.Frame(trabajador_window, bg="white", bd=5, relief="solid")
    frame_registro.place(x=300, y=50, width=500, height=500)

    tk.Label(frame_registro, text="Registro de Trabajador", font=("Helvetica", 14, "bold")).grid(row=0, columnspan=2, pady=10)
    
    tk.Label(frame_registro, text="ID:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_id = tk.Entry(frame_registro)
    entry_id.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_registro, text="Nombre:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_nombre = tk.Entry(frame_registro)
    entry_nombre.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_registro, text="Especialidad:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_especialidad = tk.Entry(frame_registro)
    entry_especialidad.grid(row=3, column=1, padx=5, pady=5)

    def registrar_trabajador():
        id_trabajador = entry_id.get()
        nombre = entry_nombre.get()
        especialidad = entry_especialidad.get()

        if not id_trabajador or not nombre:
            messagebox.showerror("Error","ID y Nombre son campos obligatorios")
            return
        
        for trabajador in Trabajador.Lista_trabajadores:
            if trabajador.id == id_trabajador:
                messagebox.showerror("Error", "El ID ya está registrado")
                return
            
        nuevo_trabajador = Trabajador(id_trabajador, nombre, "Trabajador", especialidad)
        Trabajador.guardar_trabajadores()
        Persona.guardar_usuarios()

        messagebox.showinfo("Éxito", "Trabajador registrado correctamente")
        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_especialidad.delete(0, tk.END)

    btn_registrar = tk.Button(frame_registro, text="Registrar", command=registrar_trabajador)
    btn_registrar.grid(row=4, columnspan=2, pady=10)

    def ver_lista_trabajadores():
        ventana_lista = tk.Toplevel()
        ventana_lista.title("Lista de Trabajadores")
        ventana_lista.geometry("800x600")

        tree = ttk.Treeview(ventana_lista, columns=("ID", "Nombre", "Especialidad"), show="headings")
        tree. heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Especialidad", text="Especialidad")

        Trabajador.cargar_trabajadores()

        for trabajador in Trabajador.Lista_trabajadores:
            tree.insert("", tk.END, values=(trabajador['id'], trabajador['nombre'], trabajador['especialidad']))
            
        tree.pack(expand=True, fill="both")

    def ver_productos():
        ventana_productos = tk.Toplevel(trabajador_window)
        ventana_productos.title("Gestion de productos")
        ventana_productos.geometry("900x700")

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondopostres.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
    
        fondo_label = tk.Label(ventana_productos, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        Producto.cargar_productos()

        frame_principal = tk.Frame(ventana_productos, padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")

        tree = ttk.Treeview(frame_principal, columns=("ID", "Nombre", "Precio", "Descripicion", "Categoria"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio ($)")
        tree.heading("Descripcion", text="Descripcion")
        tree.heading("Categoria", text="Categoria")

        scrollbar = ttk.Scrollbar(frame_principal, orient = "vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(expand=True, fill="both")

        for producto in Producto.Lista_productos:
            tree.insert("", tk.END, values=(producto.id, producto.nombre, f"${producto.precio:.2f}", producto.descripcion, producto.categoria))

        def actualizar_treeview():
            for item in tree.get_children():
                tree.delete(item)
            Producto.cargar_productos()
            for producto in Producto.Lista_productos:
                tree.insert("", tk.END, values=(producto.id, producto.nombre, f"${producto.precio:.2f}", producto.descripcion, producto.categoria))
            
        btn_actualizar = tk.Button(frame_principal, text="Actualizar Lista", command=actualizar_treeview)
        btn_actualizar.pack(pady=10)
    
    def agregar_productos():
        ventana_agregar_prod = tk.Toplevel(trabajador_window)
        ventana_agregar_prod.title("Agregar productos")
        ventana_agregar_prod.geometry("900x700")

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondopostres.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
    
        fondo_label = tk.Label(ventana_agregar_prod, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        id_var = tk.StringVar()
        nombre_var = tk.StringVar()
        precio_var = tk.StringVar()
        descripcion_var = tk.StringVar()
        categoria_var = tk.StringVar()

        frame_form = tk.Frame(ventana_agregar_prod, padx=20, pady=20)
        frame_form.pack(expand=True, fill="both")

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable = id_var).grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable = nombre_var).grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Precio:").grid(row=2, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable = precio_var).grid(row=2, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Descripcion:").grid(row=3, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable = descripcion_var).grid(row=3, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Categoria:").grid(row=4, column=0, sticky="e", pady=5)
        categorias = ["Pastel", "Galleta", "Dona", "Pay", "Otro"]
        ttk.Combobox(frame_form, textvariable = categoria_var, values = categorias, state="readonly").grid(row=4, column=1, pady=5, sticky="ew")

        def guardar_producto():
            if not all([id_var.get(), nombre_var.get(), precio_var.get()]):
                messagebox.showerror("Error", "ID, Nombre y Precio son obligatorios")
                return
            try:
                precio = float(precio_var.get())
                if precio <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número postivo")
                return

            if any(p.id == id_var.get() for p in Producto.Lista_productos):
                messagebox.showerror("Error", "El ID ya está registrado")
                return
            
            nuevo_producto = Producto(id_var.get(), nombre_var.get(), precio, descripcion_var.get(), categoria_var.get() if categoria_var.get() else "Otro")
            Producto.Lista_productos.append(nuevo_producto)
            Producto.guardar_productos()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            ventana_agregar_prod.destroy()
        
        tk.Button(frame_form, text="Guardar Producto", command=guardar_producto).grid(row=5, columnspan=2, pady=20)

    def ver_bebidas():
        ventana_bebidas = tk.Toplevel(trabajador_window)
        ventana_bebidas.title("Gestion de bebidas")
        ventana_bebidas.geometry("900x700")

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondobebidas.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
    
        fondo_label = tk.Label(ventana_bebidas, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        Bebida.cargar_bebidas()

        frame_principal = tk.Frame(ventana_bebidas, padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")

        tree = ttk.Treeview(frame_principal, columns=("ID", "Nombre", "Precio", "Temperatura"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio ($)")
        tree.heading("Temperatura", text="Temperatura")

        for bebida in Bebida.Lista_bebidas:
            tree.insert("", tk.END, values=(bebida.id, bebida.nombre, bebida.precio, bebida.temperatura))
        tree.pack(expand=True, fill="both")

        btn_actualizar = tk.Button(frame_principal, text="Actualizar_lista", command=lambda: [Bebida.cargar_bebidas(), actualizar_treeview()])
        btn_actualizar.pack(pady=10)

        def actualizar_treeview():
            for item in tree.get_children():
                tree.delete(item)
            for bebida in Bebida.Lista_bebidas:

                tree.insert("", tk.END, values=(bebida.id, bebida.nombre, bebida.precio, bebida.temperatura))

    def agregar_bebidas():
        ventana_agregar_bebi = tk.Toplevel(trabajador_window)
        ventana_agregar_bebi.title("Agregar bebidas")
        ventana_agregar_bebi.geometry("900x700")

        imagen_fondo = Image.open("C://Users//monse//OneDrive//Escritorio//Roberto VF 2024//Programas//Gestion_Cafe//fondobebidas.jpg")
        imagen_fondo = imagen_fondo.resize((900,700))
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
    
        fondo_label = tk.Label(ventana_agregar_bebi, image=imagen_fondo_tk)
        fondo_label.image = imagen_fondo_tk
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        id_var = tk.StringVar()
        nombre_var = tk.StringVar()
        precio_var = tk.StringVar()
        descripcion_var = tk.StringVar()
        temperatura_var = tk.StringVar(value="caliente")

        frame_form = tk.Frame(ventana_agregar_bebi, padx=20, pady=20)
        frame_form.pack(expand=True, fill="both")

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable=id_var).grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable=nombre_var).grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Precio:").grid(row=2, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable=precio_var).grid(row=2, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Descripción:").grid(row=3, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable=descripcion_var).grid(row=3, column=1, pady=5, sticky="ew")

        tk.Label(frame_form, text="Temperatura:").grid(row=4, column=0, sticky="e", pady=5)
        tk.Entry(frame_form, textvariable=temperatura_var).grid(row=4, column=1, pady=5, sticky= "ew")

        tk.Radiobutton(frame_form, text="Caliente", variable=temperatura_var, value="caliente").grid(row=4, column=1, sticky="w")
        tk.Radiobutton(frame_form, text="Fria", variable=temperatura_var, value="fria").grid(row=5, column=1, sticky="w")

        def guardar_bebida():
            if not all([id_var.get(), nombre_var.get(), precio_var.get()]):
                messagebox.showerror("Error", "ID, Nombre y Precio son obligatorios")
                return
            try:
                precio = float(precio_var.get())
                if precio <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser número positivo")
                return
            
            if any(b.id == id_var.get()for b in Bebida.Lista_bebidas):
                messagebox.showerror("Error", "El Id ya está registrado")
                return

            nueva_bebida = Bebida( id_var.get(), nombre_var.get(), precio, descripcion_var.get(), temperatura_var.get())

            Bebida.Lista_bebidas.append(nueva_bebida)
            Bebida.guardar_bebidas()

            messagebox.showinfo("Éxito", "Bebida  agregada correctamente")
            ventana_agregar_bebi.destroy()
            
        tk.Button(frame_form, text="Guardar Bebida", command= guardar_bebida).grid(row=6, columnspan=2, pady=20)

    def ver_pedidos_cliente(id_cliente):
        ventana_pedidos = tk.Toplevel()
        ventana_pedidos.title("Mis Pedidos")

        pedidos = Pedido.obtener_pedidos_por_cliente(id_cliente)

        if not pedidos:
            tk.Label(ventana_pedidos, text="No tienes pedidos registrados").pack()
            return
        
        tree = ttk.Treeview(ventana_pedidos, columns=("ID", "Fecha", "Productos", "Bebidas","Personalizaciones", "Total", "Estado"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Productos", text="Productos")
        tree.heading("Bebidas", text="Bebidas")
        tree.heading("Personalizaciones", text="Personalizaciones")
        tree.heading("Total", text="Total")
        tree.heading("Estado", text="Estado")

        for pedido in pedidos:
            nombres_productos = [p.nombre for p in Producto.Lista_productos if p.id in pedido['productos']]
            nombres_bebidas = [b.nombre for b in Bebida.Lista_bebidas if b.id in pedido['bebidas']]

            personalizaciones = "\n".join([f"{p['tipo']}: {p['base']}" for p in pedido.get('personalizaciones', [])])

            tree.insert("", tk.END, values=(pedido['id'], pedido['fecha'], ", ".join(nombres_productos), ", ".join(nombres_bebidas), personalizaciones, f"${pedido['total']:.2f}", pedido['estado']))

    boton_ver_productos = tk.Button(frame_botones, text="Ver productos", command=ver_productos, width=20, height=3, bg="lightblue")
    boton_ver_productos.pack(pady=10)

    boton_agregar_productos = tk.Button(frame_botones, text="Agregar productos", command=agregar_productos, width=20, height=3, bg="lightblue")
    boton_agregar_productos.pack(pady=10)

    boton_ver_bebidas = tk.Button(frame_botones, text="Ver bebidas", command=ver_bebidas, width=20, height=3, bg="lightblue")
    boton_ver_bebidas.pack(pady=10)

    boton_agregar_bebidas = tk.Button(frame_botones, text="Agregar bebidas", command=agregar_bebidas, width=20, height=3, bg="lightblue")
    boton_agregar_bebidas.pack(pady=10)

    boton_ver_trabajadores = tk.Button(frame_botones, text="Ver Trabajadores", command=ver_lista_trabajadores, width=20, height=3, bg="lightblue") 
    boton_ver_trabajadores.pack(pady=10)

    boton_ver_pedidos = tk.Button(frame_botones, text="Ver Pedidos", command=lambda: ver_pedidos_cliente("id_ejemplo"), width=20, heigth=3, bg="ligthblue")
    boton_ver_pedidos.pack(pady=10)

    def on_closing():
        trabajador_window.destroy()
        root.deiconify()
    
    trabajador_window.protocol("WM_DELETE_WINDOW", on_closing)
    trabajador_window.mainloop()
    pass

if __name__ == "__main__":
    ventana_principal()