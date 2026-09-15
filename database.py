import sqlite3


RUTA_BD = "inventario.db"


class DatabaseError(RuntimeError):
    """Error de persistencia que la aplicación puede mostrar al usuario."""


def conectar(ruta_bd=None):
    try:
        return sqlite3.connect(ruta_bd or RUTA_BD)
    except sqlite3.Error as error:
        raise DatabaseError("No se pudo conectar con la base de datos.") from error


def crear_tabla(ruta_bd=None):
    conexion = None
    try:
        conexion = conectar(ruta_bd)
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,
                categoria TEXT NOT NULL
            )
            """
        )
        conexion.commit()
    except sqlite3.Error as error:
        if conexion is not None:
            conexion.rollback()
        raise DatabaseError("No se pudo crear o preparar la tabla de productos.") from error
    finally:
        if conexion is not None:
            conexion.close()
