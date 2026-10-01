import psycopg

from core.database import DatabaseError, conectar
from models.venta import Venta
from models.venta import Venta, DetalleVenta


class VentasRepository:

    def guardar(self, venta: Venta) -> Venta:
        try:
            with conectar() as conn:
                with conn.transaction():

                    with conn.cursor() as cursor:

                        # 1. Verificar productos, obtener precios y bloquear filas
                        for detalle in venta.detalles:

                            cursor.execute(
                                """
                                SELECT precio, stock
                                FROM productos
                                WHERE id = %s
                                FOR UPDATE
                                """,
                                (detalle.producto_id,)
                            )

                            producto = cursor.fetchone()

                            if producto is None:
                                raise ValueError(
                                    f"El producto {detalle.producto_id} no existe."
                                )

                            precio, stock = producto

                            if stock < detalle.cantidad:
                                raise ValueError(
                                    f"Stock insuficiente para el producto "
                                    f"{detalle.producto_id}."
                                )

                            detalle.precio_unitario = float(precio)

                        # 2. Calcular el total
                        total = venta.total

                        # 3. Crear la venta
                        cursor.execute(
                            """
                            INSERT INTO ventas (usuario_id, total)
                            VALUES (%s, %s)
                            RETURNING id, fecha
                            """,
                            (venta.usuario_id, total)
                        )

                        venta.id, venta.fecha = cursor.fetchone()

                        # 4. Crear los detalles y descontar stock
                        for detalle in venta.detalles:

                            cursor.execute(
                                """
                                INSERT INTO detalle_venta (
                                    venta_id,
                                    producto_id,
                                    cantidad,
                                    precio_unitario,
                                    subtotal
                                )
                                VALUES (%s, %s, %s, %s, %s)
                                """,
                                (
                                    venta.id,
                                    detalle.producto_id,
                                    detalle.cantidad,
                                    detalle.precio_unitario,
                                    detalle.subtotal
                                )
                            )

                            cursor.execute(
                                """
                                UPDATE productos
                                SET stock = stock - %s
                                WHERE id = %s
                                """,
                                (
                                    detalle.cantidad,
                                    detalle.producto_id
                                )
                            )

                return venta

        except ValueError:
            raise

        except psycopg.Error as e:
            raise DatabaseError(
                f"Error al guardar la venta: {e}"
            ) from e

    def buscar_por_id(self, venta_id: int) -> Venta | None:
        try:
            with conectar() as conn:
                with conn.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT
                            v.id,
                            v.usuario_id,
                            v.fecha,
                            v.total,
                            dv.producto_id,
                            dv.cantidad,
                            dv.precio_unitario,
                            dv.subtotal
                        FROM ventas v
                        JOIN detalle_venta dv
                            ON dv.venta_id = v.id
                        WHERE v.id = %s
                        ORDER BY dv.id
                        """,
                        (venta_id,)
                    )

                    filas = cursor.fetchall()

                    if not filas:
                        return None

                    detalles = [
                        DetalleVenta(
                            producto_id=fila[4],
                            cantidad=fila[5],
                            precio_unitario=float(fila[6])
                        )
                        for fila in filas
                    ]

                    return Venta(
                        id=filas[0][0],
                        usuario_id=filas[0][1],
                        fecha=filas[0][2],
                        detalles=detalles
                    )

        except psycopg.Error as e:
            raise DatabaseError(
                f"Error al buscar la venta: {e}"
            ) from e

    def obtener_todas(self) -> list[Venta]:
        try:
            with conectar() as conn:
                with conn.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT
                            v.id,
                            v.usuario_id,
                            v.fecha,
                            v.total,
                            dv.producto_id,
                            dv.cantidad,
                            dv.precio_unitario
                        FROM ventas v
                        JOIN detalle_venta dv
                            ON dv.venta_id = v.id
                        ORDER BY v.id DESC, dv.id
                        """
                    )

                    filas = cursor.fetchall()

                    # 1. Diccionario temporal (aún no instanciamos Venta)
                    ventas_temporales: dict[int, dict] = {}

                    for fila in filas:
                        venta_id = fila[0]

                        if venta_id not in ventas_temporales:
                            ventas_temporales[venta_id] = {
                                "id": venta_id,
                                "usuario_id": fila[1],
                                "fecha": fila[2],
                                "detalles": [],
                            }

                        ventas_temporales[venta_id]["detalles"].append(
                            DetalleVenta(
                                producto_id=fila[4],
                                cantidad=fila[5],
                                precio_unitario=float(fila[6]),
                            )
                        )

                    # 2. Construimos las Venta ya con detalles completos
                    return [
                        Venta(
                            id=data["id"],
                            usuario_id=data["usuario_id"],
                            fecha=data["fecha"],
                            detalles=data["detalles"],
                        )
                        for data in ventas_temporales.values()
                    ]

        except psycopg.Error as e:
            raise DatabaseError(
                f"Error al obtener las ventas: {e}"
            ) from e