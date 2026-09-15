from produto_repository import ProductoRepository


class InventarioService:

    def __init__(self, repository):
        self.repository = repository
        
    def agregar_producto(self, producto):
        producto_existente = self.repository.buscar_por_id(producto.id)
        
        if producto_existente is not None:
            raise ValueError(f"No se puede agregar: Ya existe un producto con el ID {producto.id}.")
        
        if producto.id <= 0:
            raise ValueError("El ID debe ser mayor que 0.")

        if not producto.nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if producto.precio <= 0:
            raise ValueError("El precio debe ser mayor que 0.")

        if producto.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        if not producto.categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")
            
        self.repository.guardar(producto)
        return producto

    def buscar_producto(self, id):
        producto_existente = self.repository.buscar_por_id(id)  
        
        if producto_existente is None:
            raise ValueError("Producto no encontrado")
        return producto_existente

    def aumentar_stock(self, id, cantidad):
            producto_existente = self.repository.buscar_por_id(id)
            
            if producto_existente is None:
                raise ValueError(f"Error: No se encontró ningún producto con el ID {id}.")
    
            producto_existente.aumentar_stock(cantidad)
            
            self.repository.actualizar(producto_existente)
            
            return producto_existente


    def disminuir_stock(self, id, cantidad):
        producto_existente = self.repository.buscar_por_id(id)
        
        if producto_existente is None:
            raise ValueError(f"Error: No se encontró ningún producto con el ID {id}.")    
        producto_existente.disminuir_stock(cantidad) 
        self.repository.actualizar(producto_existente)
        
        return producto_existente

    def eliminar_producto(self, id):
        producto_existente = self.repository.buscar_por_id(id)  
        
        if producto_existente is None:
            raise ValueError("No puedes eliminar algo que no existe")
        self.repository.eliminar(id)
        
    def obtener_productos(self):
        return self.repository.obtener_todos()
    
    
    def modificar_producto(self, id, nombre, precio, categoria):
        producto = self.repository.buscar_por_id(id)

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que 0.")
        
        if not categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")

        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria

        self.repository.actualizar(producto)

        return producto