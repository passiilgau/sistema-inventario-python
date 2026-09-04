
class Producto:
    def __init__(self, id, nombre, precio, stock, categoria):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        

    def disminuir_stock(self, cantidad):
        if cantidad > self.stock:
            raise ValueError(
                f"No puedes quitar más de lo que hay. Stock actual: {self.stock}"
            )
        self.stock -= cantidad
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
                
                
    def aumentar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        self.stock += cantidad
    
    def mostrar_info(self):
        print(
            f"ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Precio: {self.precio} | "
            f"Stock: {self.stock} | "
            f"Categoría: {self.categoria}"
        )
    @classmethod
    def from_fila(cls, fila):
        return cls(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            fila[4]
        ) 
        
    def to_tupla(self):
        return (
            self.id,
            self.nombre,
            self.precio,
            self.stock,
            self.categoria
        )

#INVENTARIO AQUI ABAJO

class Inventario:
    def __init__(self):
        self.productos = []
        
    def agregar_producto(self, producto):
        if self.buscar_producto(producto.id):
            raise ValueError("Ese Producto ya Existe")

        self.productos.append(producto)    
        
    def mostrar_productos(self):
        for producto in self.productos:
            producto.mostrar_info()
    
    def buscar_producto(self, id_buscado):
        for producto in self.productos:
            if producto.id == id_buscado:
                return producto
        return None
    def eliminar_producto(self, id_buscado):
        for producto in self.productos:
            if producto.id == id_buscado:
                self.productos.remove(producto)
                return
        raise ValueError("No se encontró el producto a eliminar")
        

primer_inventario = Inventario()

def menu():
    while True:
        print("Opciones")
        print("1. Agregar un nuevo producto")
        print("2. Mostrar todos los productos")
        print("3. Buscar un producto")
        print("4. Aumentar Stock")
        print("5. Disminuir stock")
        print("6. Eliminar producto")
        print("7. Salir")
#input para el usuario
        opcion = input("Selecciona una opción: ")
        
#Opcion1        
        if opcion == "1":
            print("\n--- AGREGAR NUEVO PRODUCTO ---")
            
            try:
                # 1. Pedimos los datos al usuario. 
                id_prod = int(input("Ingresa el ID (número): "))
                nombre = input("Ingresa el nombre: ")
                precio = float(input("Ingresa el precio: "))
                stock = int(input("Ingresa el stock: "))
                categoria = input("Ingresa la categoría: ")
            except ValueError:
                print("Error: Asegúrate de ingresar números en ID, Precio y Stock.")
                continue
                
            nuevo_producto = Producto(id_prod, nombre, precio, stock, categoria)
            
            try:
                primer_inventario.agregar_producto(nuevo_producto)
            except ValueError as error:
                print(error)   
            
#Opcion2
        elif opcion == "2":
            print("\n--- LISTA DE PRODUCTOS ---")
            primer_inventario.mostrar_productos()
#Opcion3
        elif opcion == "3":
            try:
                id_prod = int(input("Ingresa el ID del producto:"))
            except ValueError:
                print("Debes ingresar un número valido, no letras")
                continue
            
            producto_encontrado = primer_inventario.buscar_producto(id_prod)
            
            if producto_encontrado != None:
                    print("\n--- RESULTADO DE LA BÚSQUEDA ---")
                    print(f"¡Producto encontrado! Nombre: {producto_encontrado.nombre} | Precio: ${producto_encontrado.precio} | Stock: {producto_encontrado.stock}")
            else:
                print("\nEl producto con ese ID no existe.")
#Opcion4
        elif opcion == "4":
            try:
                id_prod = int(input("Ingresa el ID (número): "))
                cantidad = int(input("Ingrese la cantidad: "))
            except ValueError:
                print("Debes ingresar un número valido, no letras")
                continue
            
            producto_encontrado = primer_inventario.buscar_producto(id_prod)
            if producto_encontrado != None:   
                try:
                    producto_encontrado.aumentar_stock(cantidad)
                except ValueError as error:
                    print(error)
            else:
                print("No se encontró el producto")
#Opcion5 
        elif opcion == "5":
            try:
                id_prod = int(input("Ingresa el ID (número): "))
                cantidad = int(input("Ingrese la cantidad: "))
            except ValueError:
                    print("Debes ingresar un número valido, no letras")
                    continue
            
            producto_encontrado = primer_inventario.buscar_producto(id_prod)
            if producto_encontrado != None:
                try:
                    producto_encontrado.disminuir_stock(cantidad)
                except ValueError as error:
                    print(error)
            else:
                print("No se encontró el producto")
#Opción6
        elif opcion == "6":
            try:
                id_prod = int(input("Ingresa el ID (número): "))
            except ValueError:
                        print("Debes ingresar un número valido, no letras")
                        continue
            try:
                primer_inventario.eliminar_producto(id_prod)
            except ValueError as error:
                print(error)
#Opción7
        elif opcion == "7":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")
        
            


                         
                
            
            

        
            






