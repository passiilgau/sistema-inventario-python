from database import crear_tabla
from produto_repository import Producto, ProductoRepository

crear_tabla()
repositorio = ProductoRepository()

print("\n--- PRUEBA 5: ACTUALIZAR STOCK ---")

# 1. Guardamos un producto nuevo para la prueba
producto_prueba = Producto(50, "Cámara Digital", 500, 10, "Fotografía")
repositorio.guardar(producto_prueba)

# 2. Lo buscamos desde la base de datos y lo mostramos
producto_bd = repositorio.buscar_por_id(50)
print("\nStock ANTES de actualizar:")
producto_bd.mostrar_info()

# 3. Modificamos el objeto en la memoria usando TU método de la clase
print("\nLlegaron 5 cámaras nuevas. Aumentando stock...")
producto_bd.aumentar_stock(5)  # Ahora el stock debería ser 15

# 4. Le pedimos al repositorio que guarde este cambio en la Base de Datos
repositorio.actualizar(producto_bd)

# 5. Lo volvemos a buscar para confirmar que la Base de Datos sí cambió
producto_final = repositorio.buscar_por_id(50)
print("\nStock DESPUÉS de actualizar (Extraído de SQLite):")
producto_final.mostrar_info()

# Limpieza (opcional, para que puedas correr la prueba varias veces)
repositorio.eliminar(50)