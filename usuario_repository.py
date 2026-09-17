from database import conectar


class UsuarioRepository:

    def buscar_por_username(self, username):
        conexion = conectar()

        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, username, password_hash, nombre, rol
                    FROM usuarios
                    WHERE username = %s
                    """,
                    (username,)
                )

                return cursor.fetchone()

        finally:
            conexion.close()