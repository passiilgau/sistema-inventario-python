from produto_repository import ProductoRepository


class InventarioService:

    def __init__(self, repository):
        self.repository = repository
        
    def agregar_producto(self, producto):
        producto_existente = self.repository.buscar_por_id(producto.id)
        
        if producto_existente is not None:
            raise ValueError(f"No se puede agregar: Ya existe un producto con el ID {producto.id}.")
            
        self.repository.guardar(producto)

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