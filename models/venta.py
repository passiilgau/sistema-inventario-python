from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DetalleVenta:
    producto_id: int
    cantidad: int
    precio_unitario: float | None = None

    def __post_init__(self) -> None:
        if self.producto_id <= 0:
            raise ValueError("El ID del producto debe ser mayor que 0.")

        if self.cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor que 0.")

        if self.precio_unitario is not None and self.precio_unitario <= 0:
            raise ValueError("El precio unitario debe ser mayor que 0.")

    @property
    def subtotal(self) -> float:
        if self.precio_unitario is None:
            raise ValueError("El precio unitario aún no ha sido asignado.")

        return self.cantidad * self.precio_unitario


@dataclass
class Venta:
    detalles: list[DetalleVenta]
    usuario_id: int
    id: int | None = None
    fecha: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if self.usuario_id <= 0:
            raise ValueError("El ID del usuario debe ser mayor que 0.")

        if not self.detalles:
            raise ValueError("Una venta debe tener al menos un detalle.")

    @property
    def total(self) -> float:
        return sum(detalle.subtotal for detalle in self.detalles)