from fastapi.middleware.cors import CORSMiddleware
from produto_repository import ProductoRepository
from inventario_service import InventarioService
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate, StockUpdate
from fastapi import FastAPI, HTTPException
from producto import Producto



app = FastAPI(title="Sistema de Inventario")

repository = ProductoRepository()
service = InventarioService(repository)

app.add_middleware(
    CORSMiddleware,
    # Ese puerto 5500 es el clásico del "Live Server" de VS Code. ¡Está perfecto!
    allow_origins=["http://127.0.0.1:5500"],  
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {"mensaje": "API de inventario funcionando"}


@app.get("/saludo")
def saludo():
    return {"mensaje": "Hola desde mi API"}


@app.get("/productos", response_model=list[ProductoResponse])
def obtener_productos():
    return service.obtener_productos()

@app.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto(id: int):

    try:
        return service.buscar_producto(id)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@app.post("/productos", response_model=ProductoResponse)
def crear_producto(datos: ProductoCreate):

    producto = Producto(
        datos.id,
        datos.nombre,
        datos.precio,
        datos.stock,
        datos.categoria
    )

    try:
        producto_guardado = service.agregar_producto(producto)
        return producto_guardado

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

@app.put("/productos/{id}", response_model=ProductoResponse)
def modificar_producto(id: int, datos: ProductoUpdate):

    try:
        producto = service.modificar_producto(
            id,
            datos.nombre,
            datos.precio,
            datos.categoria
        )

        return producto

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
        
@app.patch("/productos/{id}/stock/aumentar", response_model=ProductoResponse)
def aumentar_stock(id: int, datos: StockUpdate):

    try:
        producto = service.aumentar_stock(id, datos.cantidad)
        return producto

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.patch("/productos/{id}/stock/disminuir", response_model=ProductoResponse)
def disminuir_stock(id: int, datos: StockUpdate):

    try:
        producto = service.disminuir_stock(id, datos.cantidad)
        return producto

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
        
@app.delete("/productos/{id}")
def eliminar_producto(id: int):

    try:
        service.eliminar_producto(id)

        return {
            "mensaje": f"Producto con ID {id} eliminado correctamente."
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
