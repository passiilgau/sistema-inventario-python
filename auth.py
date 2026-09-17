from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, password_hash_db: str) -> bool:
    return password_hash.verify(password, password_hash_db)

def crear_access_token(username: str, rol: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "rol": rol,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def obtener_usuario_actual(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        # AGREGA ESTO PARA DEBUGEAR:
        print("====== DEBUG TOKEN ======")
        print(payload)
        print("=========================")

        username = payload.get("sub")

        username = payload.get("sub")
        rol = payload.get("rol")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return {
            "username": username,
            "rol": rol
        }

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
        
        
def requiere_rol(rol_requerido: str):
    def verificar_rol(usuario=Depends(obtener_usuario_actual)):
        if usuario["rol"] != rol_requerido:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para realizar esta acción."
            )

        return usuario

    return verificar_rol

