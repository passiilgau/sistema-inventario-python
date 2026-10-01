from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import obtener_usuario_actual
from models.venta import DetalleVenta, Venta
from repositories.ventas_repository import VentasRepository
from schemas.venta import VentaCreate, VentaDetalleResponse, VentaResponse
from services.ventas_service import VentasService


router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

ventas_repository = VentasRepository()
ventas_service = VentasService(ventas_repository)


@router.post(
    "",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_venta(
    datos: VentaCreate,
    usuario: Annotated[dict, Depends(obtener_usuario_actual)]
):
    try:
        detalles = [
            DetalleVenta(
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad
            )
            for detalle in datos.detalles
        ]

        venta = Venta(
            detalles=detalles,
            usuario_id=usuario["id"]
        )

        venta = ventas_service.registrar_venta(venta)

        return VentaResponse(
            id=venta.id,
            fecha=venta.fecha,
            detalles=[
                VentaDetalleResponse(
                    producto_id=detalle.producto_id,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                    subtotal=detalle.subtotal
                )
                for detalle in venta.detalles
            ],
            total=venta.total
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.get("", response_model=list[VentaResponse])
def obtener_ventas(
    usuario: Annotated[dict, Depends(obtener_usuario_actual)]
):
    ventas = ventas_service.obtener_ventas()

    return [
        VentaResponse(
            id=venta.id,
            fecha=venta.fecha,
            detalles=[
                VentaDetalleResponse(
                    producto_id=detalle.producto_id,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                    subtotal=detalle.subtotal
                )
                for detalle in venta.detalles
            ],
            total=venta.total
        )
        for venta in ventas
    ]
    
@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(
    venta_id: int,
    usuario: Annotated[dict, Depends(obtener_usuario_actual)]
):
    venta = ventas_service.repository.buscar_por_id(venta_id)

    if venta is None:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada."
        )

    return VentaResponse(
        id=venta.id,
        fecha=venta.fecha,
        detalles=[
            VentaDetalleResponse(
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal
            )
            for detalle in venta.detalles
        ],
        total=venta.total
    )