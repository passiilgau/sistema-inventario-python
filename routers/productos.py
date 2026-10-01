from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from core.auth import obtener_usuario_actual, requiere_rol
from models.producto import Producto
from repositories.producto_repository import ProductoRepository
from schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate, StockUpdate
from services.inventario_service import InventarioService


router = APIRouter(prefix="/productos", tags=["Productos"])
UsuarioActual = Annotated[dict, Depends(obtener_usuario_actual)]

repository = ProductoRepository()
service = InventarioService(repository)


@router.get("", response_model=list[ProductoResponse])
def obtener_productos(usuario: UsuarioActual):
    return service.obtener_productos()


@router.get("/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, usuario: UsuarioActual):
    try:
        return service.buscar_producto(id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("", response_model=ProductoResponse)
def crear_producto(datos: ProductoCreate, usuario=Depends(requiere_rol("admin"))):
    producto = Producto(
        datos.id,
        datos.nombre,
        datos.precio,
        datos.stock,
        datos.categoria,
    )

    try:
        return service.agregar_producto(producto)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.put("/{id}", response_model=ProductoResponse)
def modificar_producto(
    id: int,
    datos: ProductoUpdate,
    usuario=Depends(requiere_rol("admin")),
):
    try:
        return service.modificar_producto(id, datos.nombre, datos.precio, datos.categoria)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/{id}/stock/aumentar", response_model=ProductoResponse)
def aumentar_stock(id: int, datos: StockUpdate, usuario: UsuarioActual):
    try:
        return service.aumentar_stock(id, datos.cantidad)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.patch("/{id}/stock/disminuir", response_model=ProductoResponse)
def disminuir_stock(id: int, datos: StockUpdate, usuario: UsuarioActual):
    try:
        return service.disminuir_stock(id, datos.cantidad)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/{id}")
def eliminar_producto(id: int, usuario=Depends(requiere_rol("admin"))):
    try:
        service.eliminar_producto(id)
        return {"mensaje": f"Producto con ID {id} eliminado correctamente."}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
