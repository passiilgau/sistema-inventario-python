from fastapi import FastAPI

from database import crear_tabla
from produto_repository import ProductoRepository
from inventario_service import InventarioService
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate
from fastapi import FastAPI, HTTPException
from producto import Producto


app = FastAPI(title="Sistema de Inventario")

crear_tabla()

repository = ProductoRepository()
service = InventarioService(repository)


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

