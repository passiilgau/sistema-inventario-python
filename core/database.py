import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


class DatabaseError(RuntimeError):
    """Error de persistencia de la aplicación."""


def conectar():
    try:
        return psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

    except psycopg.Error as error:
        raise DatabaseError(
            "No se pudo conectar con la base de datos."
        ) from error
