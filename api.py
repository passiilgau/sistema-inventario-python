from fastapi.middleware.cors import CORSMiddleware
from produto_repository import ProductoRepository
from inventario_service import InventarioService
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate, StockUpdate
from fastapi import FastAPI, HTTPException
from producto import Producto
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from usuario_repository import UsuarioRepository
from auth import verify_password, crear_access_token
from typing import Annotated
from fastapi import Depends
from auth import obtener_usuario_actual
from auth import requiere_rol
UsuarioActual = Annotated[dict, Depends(obtener_usuario_actual)]



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



@app.get("/productos", response_model=list[ProductoResponse])
def obtener_productos(usuario: UsuarioActual):
    return service.obtener_productos()

@app.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, usuario: UsuarioActual):

    try:
        return service.buscar_producto(id)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@app.post("/productos", response_model=ProductoResponse)
def crear_producto(datos: ProductoCreate, usuario=Depends(requiere_rol("admin"))):

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
def modificar_producto(id: int, datos: ProductoUpdate, usuario=Depends(requiere_rol("admin"))):

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
def aumentar_stock(id: int, datos: StockUpdate, usuario: UsuarioActual):

    try:
        producto = service.aumentar_stock(id, datos.cantidad)
        return producto

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.patch("/productos/{id}/stock/disminuir", response_model=ProductoResponse)
def disminuir_stock(id: int, datos: StockUpdate, usuario: UsuarioActual):

    try:
        producto = service.disminuir_stock(id, datos.cantidad)
        return producto

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
        
@app.delete("/productos/{id}")
def eliminar_producto(
    id: int,
    usuario=Depends(requiere_rol("admin"))
):
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
        
usuario_repository = UsuarioRepository()

@app.post("/auth/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    usuario = usuario_repository.buscar_por_username(
        form_data.username
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_hash_db = usuario[2]

    if not verify_password(
        form_data.password,
        password_hash_db
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_access_token(
        username=usuario[1],
        rol=usuario[4]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/usuarios/me")
def usuario_actual(
    usuario: Annotated[dict, Depends(obtener_usuario_actual)]
):
    return usuario
