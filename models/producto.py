
class Producto:
    def __init__(self, id, nombre, precio, stock, categoria):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        

    def disminuir_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")

        if cantidad > self.stock:
            raise ValueError(
                f"No puedes quitar más de lo que hay. Stock actual: {self.stock}"
            )

        self.stock -= cantidad
                
                
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

# class Inventario:
#     def __init__(self):
#         self.productos = []
        
#     def agregar_producto(self, producto):
#         if self.buscar_producto(producto.id):
#             raise ValueError("Ese Producto ya Existe")

#         self.productos.append(producto)    
        
#     def mostrar_productos(self):
#         for producto in self.productos:
#             producto.mostrar_info()
    
#     def buscar_producto(self, id_buscado):
#         for producto in self.productos:
#             if producto.id == id_buscado:
#                 return producto
#         return None
#     def eliminar_producto(self, id_buscado):
#         for producto in self.productos:
#             if producto.id == id_buscado:
#                 self.productos.remove(producto)
#                 return
#         raise ValueError("No se encontró el producto a eliminar")
        
        
            


                         
                
            
            

        
            






