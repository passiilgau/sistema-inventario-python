import sqlite3
from database import conectar
from producto import Producto


class ProductoRepository:

    def guardar(self, producto):
        datos = producto.to_tupla()
        
        conexion = conectar()
        cursor = conexion.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO productos
                (id, nombre, precio, stock, categoria)
                VALUES (?, ?, ?, ?, ?)
                """,
                datos
            )
            conexion.commit()
            print(f"Producto '{producto.nombre}' guardado correctamente en la BD.")
            
        except sqlite3.IntegrityError:
            print(f"Error: Ya existe un producto con el ID {producto.id}.")
            
        finally:
            conexion.close()

    def obtener_todos(self):
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT * FROM productos")
        
        lista_productos = cursor.fetchall()
        
        conexion.close()
        
        productos = []

        for fila in lista_productos:
            productos.append(Producto.from_fila(fila))

        return productos
    def buscar_por_id(self, id_buscado):
            conexion = conectar()
            cursor = conexion.cursor()
        
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_buscado,))
            
            fila = cursor.fetchone()
            
            conexion.close()
            
            if fila is not None:
                return Producto.from_fila(fila)
            else:
                return None
    def eliminar(self, id_eliminar):
            conexion = conectar()
            cursor = conexion.cursor()
        
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_eliminar,))
            
            filas_afectadas = cursor.rowcount

            conexion.commit()
            conexion.close()
            
            if filas_afectadas > 0:
                print(f"Producto con ID {id_eliminar} eliminado correctamente.")
                return True
            else:
                print(f"No se pudo eliminar: No se encontró ningún producto con el ID {id_eliminar}.")
                return False
            
    def actualizar(self, producto):
            conexion = conectar()
            cursor = conexion.cursor()
            
            try:
                cursor.execute(
                    """
                    UPDATE productos 
                    SET nombre = ?, precio = ?, stock = ?, categoria = ?
                    WHERE id = ?
                    """,
                    (producto.nombre, producto.precio, producto.stock, producto.categoria, producto.id)
                )
                
                filas_afectadas = cursor.rowcount
                conexion.commit()
                
                if filas_afectadas > 0:
                    print(f"Producto con ID {producto.id} actualizado correctamente.")
                    return True
                else:
                    print(f"No se pudo actualizar: No se encontró el ID {producto.id}.")
                    return False
                    
            finally:
                conexion.close()