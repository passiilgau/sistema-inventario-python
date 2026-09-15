from database import crear_tabla
from produto_repository import ProductoRepository
from inventario_service import InventarioService
from producto import Producto


crear_tabla()

repository = ProductoRepository()
service = InventarioService(repository)

     
#Opcion1        
def registrar_producto():
    print("\n--- AGREGAR NUEVO PRODUCTO ---")

    try:
        id_prod = int(input("Ingresa el ID: "))
        nombre = input("Ingresa el nombre: ")
        precio = float(input("Ingresa el precio: "))
        stock = int(input("Ingresa el stock: "))
        categoria = input("Ingresa la categoría: ")

        nuevo_producto = Producto(
            id_prod,
            nombre,
            precio,
            stock,
            categoria
        )

        service.agregar_producto(nuevo_producto)

        print("Producto agregado correctamente.")

    except ValueError as error:
        print(f"Error: {error}") 
    
#Opcion2
def mostrar_productos():
    print("\n--- LISTA DE PRODUCTOS ---")

    productos = service.obtener_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        producto.mostrar_info()
#Opcion3
def buscar_producto():
    print("\n--- BUSCAR PRODUCTO ---")

    try:
        id_prod = int(input("Ingresa el ID del producto: "))

        producto = service.buscar_producto(id_prod)

        producto.mostrar_info()

    except ValueError as error:
        print(error)
#Opcion4
def aumentar_stock():
    print("\n--- AUMENTAR STOCK ---")

    try:
        id_prod = int(input("Ingresa el ID: "))
        cantidad = int(input("Ingrese la cantidad: "))

        producto = service.aumentar_stock(id_prod, cantidad)

        print(f"Nuevo stock de {producto.nombre}: {producto.stock}")

    except ValueError as error:
        print(error)
#Opcion5 
def disminuir_stock():
    print("\n--- DISMINUIR STOCK ---")

    try:
        id_prod = int(input("Ingresa el ID: "))
        cantidad = int(input("Ingrese la cantidad: "))

        producto = service.disminuir_stock(id_prod, cantidad)

        print(f"Nuevo stock de {producto.nombre}: {producto.stock}")

    except ValueError as error:
        print(error)
#Opción6
def eliminar_producto():
    print("\n--- ELIMINAR PRODUCTO ---")

    try:
        id_prod = int(input("Ingresa el ID del producto: "))

        service.eliminar_producto(id_prod)

        print("Producto eliminado correctamente.")

    except ValueError as error:
        print(error)
        
#opcion7
def modificar_producto():
    print("\n--- MODIFICAR PRODUCTO ---")

    try:
        id_prod = int(input("Ingresa el ID del producto: "))

        producto = service.buscar_producto(id_prod)

        print("\nDatos actuales:")
        producto.mostrar_info()

        print("\nIngresa los nuevos datos:")

        nombre = input("Nuevo nombre: ")
        precio = float(input("Nuevo precio: "))
        categoria = input("Nueva categoría: ")

        producto = service.modificar_producto(
            id_prod,
            nombre,
            precio,
            categoria
        )

        print("\nProducto actualizado correctamente.")
        producto.mostrar_info()

    except ValueError as error:
        print(f"Error: {error}")
        
        
def menu():

    while True:

        print("\n===== SISTEMA DE INVENTARIO =====")
        print("1. Agregar un nuevo producto")
        print("2. Mostrar todos los productos")
        print("3. Buscar un producto")
        print("4. Aumentar stock")
        print("5. Disminuir stock")
        print("6. Eliminar producto")
        print("7. Modificar producto")
        print("8. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_producto()

        elif opcion == "2":
            mostrar_productos()

        elif opcion == "3":
            buscar_producto()

        elif opcion == "4":
            aumentar_stock()

        elif opcion == "5":
            disminuir_stock()

        elif opcion == "6":
            eliminar_producto()

        elif opcion == "7":
            modificar_producto()

        elif opcion == "8":
            print("Hasta luego.")
            break

        else:
            print("Opción no válida.")
                
if __name__ == "__main__":
    menu()