from models.venta import Venta
from repositories.ventas_repository import VentasRepository

class VentasService:
    def __init__(self, repository: VentasRepository):
        self.repository = repository

    def registrar_venta(self, venta: Venta) -> Venta:
        return self.repository.guardar(venta)

    def obtener_ventas(self) -> list[Venta]:
        return self.repository.obtener_todas()
