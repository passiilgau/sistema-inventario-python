from datetime import datetime

from pydantic import BaseModel, Field


class VentaDetalleCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class VentaCreate(BaseModel):
    detalles: list[VentaDetalleCreate] = Field(min_length=1)


class VentaDetalleResponse(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float


class VentaResponse(BaseModel):
    id: int
    fecha: datetime
    detalles: list[VentaDetalleResponse]
    total: float