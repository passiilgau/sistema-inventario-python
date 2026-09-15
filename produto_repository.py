import sqlite3

from database import DatabaseError, conectar
from producto import Producto


class ProductoRepository:
    def guardar(self, producto):
        conexion = None
        try:
            conexion = conectar()
            conexion.execute(
                """
                INSERT INTO productos (id, nombre, precio, stock, categoria)
                VALUES (?, ?, ?, ?, ?)
                """,
                producto.to_tupla(),
            )
            conexion.commit()
        except sqlite3.IntegrityError as error:
            if conexion is not None:
                conexion.rollback()
            raise ValueError(
                f"No se puede agregar: Ya existe un producto con el ID {producto.id}."
            ) from error
        except sqlite3.Error as error:
            if conexion is not None:
                conexion.rollback()
            raise DatabaseError("No se pudo guardar el producto en la base de datos.") from error
        finally:
            if conexion is not None:
                conexion.close()

    def obtener_todos(self):
        conexion = None
        try:
            conexion = conectar()
            filas = conexion.execute("SELECT * FROM productos").fetchall()
            return [Producto.from_fila(fila) for fila in filas]
        except sqlite3.Error as error:
            raise DatabaseError("No se pudieron obtener los productos.") from error
        finally:
            if conexion is not None:
                conexion.close()

    def buscar_por_id(self, id_buscado):
        conexion = None
        try:
            conexion = conectar()
            fila = conexion.execute(
                "SELECT * FROM productos WHERE id = ?", (id_buscado,)
            ).fetchone()
            return Producto.from_fila(fila) if fila is not None else None
        except sqlite3.Error as error:
            raise DatabaseError("No se pudo buscar el producto.") from error
        finally:
            if conexion is not None:
                conexion.close()

    def eliminar(self, id_eliminar):
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.execute("DELETE FROM productos WHERE id = ?", (id_eliminar,))
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as error:
            if conexion is not None:
                conexion.rollback()
            raise DatabaseError("No se pudo eliminar el producto.") from error
        finally:
            if conexion is not None:
                conexion.close()

    def actualizar(self, producto):
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.execute(
                """
                UPDATE productos
                SET nombre = ?, precio = ?, stock = ?, categoria = ?
                WHERE id = ?
                """,
                (producto.nombre, producto.precio, producto.stock, producto.categoria, producto.id),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as error:
            if conexion is not None:
                conexion.rollback()
            raise DatabaseError("No se pudo actualizar el producto.") from error
        finally:
            if conexion is not None:
                conexion.close()
