import sqlite3

def conectar():
    conexion = sqlite3.connect("inventario.db")
    return conexion
def crear_tabla():
    conexion =conectar()
    
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()
    
def insertar_producto(id, nombre, precio, stock, categoria):
    conexion = conectar()
    
    cursor = conexion.cursor()
    
    cursor.execute(
        """
        INSERT INTO productos
        (id, nombre, precio, stock, categoria)
        VALUES (?, ?, ?, ?, ?)
        """,
        (id, nombre, precio, stock, categoria)
    )
     
    conexion.commit()
    conexion.close()
    


