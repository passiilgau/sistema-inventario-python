from fastapi import FastAPI
import os
from routers.auth import router as auth_router
from routers.productos import router as productos_router
from routers.ventas import router as ventas_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Sistema de Inventario")

app.include_router(auth_router)
app.include_router(productos_router)
app.include_router(ventas_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", 
        "https://tu-proyecto-front.netlify.app" # <- ¡Agrega tu URL real de Netlify aquí! (sin el / al final)
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)