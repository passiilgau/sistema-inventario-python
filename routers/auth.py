from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import crear_access_token, obtener_usuario_actual, verify_password
from repositories.usuario_repository import UsuarioRepository
from schemas.usuario import TokenResponse


router = APIRouter(tags=["Autenticación"])
usuario_repository = UsuarioRepository()


@router.post("/auth/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = usuario_repository.buscar_por_username(form_data.username)

    if usuario is None or not verify_password(form_data.password, usuario[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_access_token(
    usuario_id=usuario[0],
    username=usuario[1],
    rol=usuario[4]
)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/usuarios/me")
def usuario_actual(usuario: Annotated[dict, Depends(obtener_usuario_actual)]):
    return usuario
