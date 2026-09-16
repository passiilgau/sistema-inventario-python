
from database import DatabaseError, conectar
from producto import Producto
import psycopg


class ProductoRepository:
    def guardar(self, producto):
        conexion = None

        try:
            conexion = conectar()

            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO productos
                    (id, nombre, precio, stock, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    producto.to_tupla()
                )

            conexion.commit()

        except psycopg.errors.UniqueViolation as error:
            if conexion:
                conexion.rollback()

            raise ValueError(
                f"No se puede agregar: Ya existe un producto con el ID {producto.id}."
            ) from error

        except psycopg.Error as error:
            if conexion:
                conexion.rollback()

            raise DatabaseError(
                "No se pudo guardar el producto en la base de datos."
            ) from error

        finally:
            if conexion:
                conexion.close()

    def obtener_todos(self):
        conexion = None

        try:
            conexion = conectar()

            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos")
                filas = cursor.fetchall()

            return [Producto.from_fila(fila) for fila in filas]

        except psycopg.Error as error:
            raise DatabaseError(
                "No se pudieron obtener los productos."
            ) from error

        finally:
            if conexion:
                conexion.close()

    def buscar_por_id(self, id_buscado):
        conexion = None

        try:
            conexion = conectar()

            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM productos WHERE id = %s",
                    (id_buscado,)
                )

                fila = cursor.fetchone()

            return Producto.from_fila(fila) if fila is not None else None

        except psycopg.Error as error:
            raise DatabaseError(
                "No se pudo buscar el producto."
            ) from error

        finally:
            if conexion:
                conexion.close()

    def eliminar(self, id_eliminar):
        conexion = None

        try:
            conexion = conectar()

            with conexion.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM productos WHERE id = %s",
                    (id_eliminar,)
                )

                eliminado = cursor.rowcount > 0

            conexion.commit()

            return eliminado

        except psycopg.Error as error:
            if conexion:
                conexion.rollback()

            raise DatabaseError(
                "No se pudo eliminar el producto."
            ) from error

        finally:
            if conexion:
                conexion.close()

    def actualizar(self, producto):
        conexion = None

        try:
            conexion = conectar()

            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE productos
                    SET nombre = %s,
                        precio = %s,
                        stock = %s,
                        categoria = %s
                    WHERE id = %s
                    """,
                    (
                        producto.nombre,
                        producto.precio,
                        producto.stock,
                        producto.categoria,
                        producto.id
                    )
                )

                actualizado = cursor.rowcount > 0

            conexion.commit()

            return actualizado

        except psycopg.Error as error:
            if conexion:
                conexion.rollback()

            raise DatabaseError(
                "No se pudo actualizar el producto."
            ) from error

        finally:
            if conexion:
                conexion.close()

