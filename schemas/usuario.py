from pydantic import BaseModel


class UsuarioResponse(BaseModel):
    id: int
    username: str
    nombre: str
    rol: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
