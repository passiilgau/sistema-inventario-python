from fastapi import FastAPI
import os

from routers.auth import router as auth_router
from routers.productos import router as productos_router
from routers.ventas import router as ventas_router

app = FastAPI(title="Sistema de Inventario")

app.include_router(auth_router)
app.include_router(productos_router)
app.include_router(ventas_router)
