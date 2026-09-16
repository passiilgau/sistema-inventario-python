import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

conexion = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("Conexión exitosa a PostgreSQL")

conexion.close()