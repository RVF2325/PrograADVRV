import os
import json
from datetime import datetime

USUARIOS_JSON = "Usuarios01.json"
CLIENTES_JSON = "Clientes01.json"
TRABAJADORES_JSON = "Trabajadores01.json"
PRODUCTOS_JSON = "Productos01.json"
BEBIDAS_JSON = "Bebidas01.json"
PEDIDOS_JSON = "Pedidos01.json"
PERSONALIZACIONES_JSON = "Personalizaciones01.json"

def inicializar_archivos():
    archivos = [USUARIOS_JSON, CLIENTES_JSON, TRABAJADORES_JSON, PRODUCTOS_JSON, BEBIDAS_JSON, PEDIDOS_JSON, PERSONALIZACIONES_JSON]

    for archivo in archivos:
        if not os.path.exist(archivo):
            with open(archivo, "w") as f:
                json.dump([], f)

class Persona:
    Lista_usuarios = []
    
    @classmethod
    def cargar_usuarios(cls):
        try:
            with open(USUARIOS_JSON, "r") as f:
                data = json.load(f)
                cls.Lista_usuarios = data
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_usuarios = []
    
    @classmethod
    def guardar_usuarios(cls):
        with open(USUARIOS_JSON, "w") as f:
            json.dump(cls.Lista_usuarios, f, indent=4)
    
    def __init__(self, id, nombre, tipo):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        if not any (u['id'] == id for u in self.Lista_usuarios):
            self.Lista_usuarios.append({"id": id, "nombre": nombre, "tipo": tipo})
            self.guardar_usuarios()

class Cliente(Persona):
    Lista_clientes = []
    
    @classmethod
    def cargar_clientes(cls):
        try:
            with open(CLIENTES_JSON, "r") as f:
                cls.Lista_clientes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_clientes = []
    
    @classmethod
    def guardar_clientes(cls):
        with open(CLIENTES_JSON, "w") as f:
            json.dump(cls.Lista_clientes, f, indent=4)
    
    def __init__(self, id, nombre, tipo, edad, alergias=""):
        super().__init__(id, nombre, tipo)
        self.edad = edad
        self.alergias = alergias

        cliente_existente = next((c for c in self.Lista_clientes if c['id'] == id), None)

        if not cliente_existente:
            nuevo_cliente = {"id": id, "nombre": nombre, "edad": edad, "alergias": alergias, "pedidos": []}
        self.Lista_clientes.append(nuevo_cliente)
        self.guardar_clientes()

class Trabajador(Persona):
    Lista_trabajadores = []
    
    @classmethod
    def cargar_trabajadores(cls):
        try:
            with open(TRABAJADORES_JSON, "r") as f:
                cls.Lista_trabajadores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_trabajadores = []
    
    @classmethod
    def guardar_trabajadores(cls):
        with open(TRABAJADORES_JSON, "w") as f:
            json.dump(cls.Lista_trabajadores, f, indent=4)
    
    def __init__(self, id, nombre, tipo, especialidad):
        super().__init__(id, nombre, tipo)
        self.especialidad = especialidad
        if not any(t['id'] == id for t in self.Lista_trabajadores):
            self.Lista_trabajadores.append({"id": id, "nombre": nombre, "especialidad": especialidad, "tipo":tipo})
            self.guardar_trabajadores()

class Producto:
    Lista_productos = []
    
    @classmethod
    def cargar_productos(cls):
        try:
            with open(PRODUCTOS_JSON, "r") as f:
                cls.Lista_productos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_productos = []
    
    @classmethod
    def guardar_productos(cls):
        with open(PRODUCTOS_JSON, "w") as f:
            json.dump(cls.Lista_productos, f, indent=4)
    
    def __init__(self, id, nombre, precio, descripcion="", categoria="Otro"):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
        if not any(p['id'] == id for p in self.Lista_productos):
            self.Lista_productos.append({
                "id": id, 
                "nombre": nombre, 
                "precio": precio, 
                "descripcion": descripcion, 
                "categoria": categoria
            })
        self.guardar_productos()

class Bebida:
    Lista_bebidas = []
    
    @classmethod
    def cargar_bebidas(cls):
        try:
            with open(BEBIDAS_JSON, "r") as f:
                cls.Lista_bebidas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_bebidas = []
    
    @classmethod
    def guardar_bebidas(cls):
        with open(BEBIDAS_JSON, "w") as f:
            json.dump(cls.Lista_bebidas, f, indent=4)
    
    def __init__(self, id, nombre, precio, descripcion="", temperatura="caliente"):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.temperatura = temperatura
        if not any(b['id'] == id for b in self.Lista_bebidas):
            self.Lista_bebidas.append({
                "id": id,
                "nombre": nombre,
                "precio": precio,
                "descripcion": descripcion,
                "temperatura": temperatura
            })
            self.guardar_bebidas()

class Pedido:
    Lista_pedidos = []
    contador_id = 1
    
    @classmethod
    def cargar_pedidos(cls):
        try:
            with open("pedidos.json", "r") as f:
                cls.Lista_pedidos = json.load(f)
                if cls.Lista_pedidos:
                    cls.contador_id = max(int(p['id']) for p in cls.Lista_pedidos) + 1
        except (FileNotFoundError, ValueError):
            cls.Lista_pedidos = []
    
    @classmethod
    def guardar_pedidos(cls):
        with open(PEDIDOS_JSON, "w") as f:
            json.dump(cls.Lista_pedidos, f, indent=4)
    
    @classmethod
    def crear_pedido(cls, id_cliente, productos, bebidas):
        cliente_existe = any(c.id == id_cliente for c in Cliente.Lista_clientes)
        if not cliente_existe:
            raise ValueError("Cliente no encontrado")
        
        productos_obj = [p for p in Producto.Lista_productos if p.id in productos]
        bebidas_obj = [b for b in Bebida.Lista_bebidas if b.id in bebidas]

        total = sum(p.precio for p in productos_obj) + sum(b.preccio for b in bebidas_obj)

        pedido = {
            "id": str(cls.contador_id),
            "id_cliente": id_cliente,
            "productos": productos,
            "bebidas": bebidas,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estado": "pendiente",
            "total": total,
            "personalizaciones": []
        }

        for personalizacion in Personalizacion.Lista_personalizaciones:
            if personalizacion.get('id_pedido') == str(cls.contador_id):
                pedido['personalizaciones'].append(personalizacion)
        
        cls.Lista_pedidos.append(pedido)
        cls.contador_id += 1
        cls.guardar_pedidos()

        for cliente in Cliente.Lista_clientes:
            if cliente['id'] == id_cliente:
                cliente['pedidos'].append(str(pedido['id']))
                Cliente.guardar_clientes()
                break

        return pedido
    
    @classmethod
    def obtener_pedidos_por_cliente(cls, id_cliente):
        return [p for p in cls.Lista_pedidos if p['id_cliente'] == id_cliente]
    
class Personalizacion:
    Lista_personalizaciones = []

    @classmethod
    def cargar_personalizaciones(cls):
        try:
            with open(PERSONALIZACIONES_JSON, "r") as f:
                cls.Lista_personalizaciones = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Lista_personalizaciones = []
    
    @classmethod
    def guardar_personalizaciones(cls):
        with open(PERSONALIZACIONES_JSON, "w") as f:
            json.dump(cls.Lista_personalizaciones, f, indent=4)
    
    def __init__(self, id_pedido, tipo, base, extras, notas):
        self.id_pedido = id_pedido
        self.tipo = tipo
        self.base = base
        self.extras = extras
        self.notas = notas
        if not any(p['id'] == id for p in self.Lista_personalizaciones):
            self.Lista_personalizaciones.append({"id_pedido": id_pedido, "tipo": tipo, "base": base, "extras": extras, "notas": notas})
            self.guardar_personalizaciones()