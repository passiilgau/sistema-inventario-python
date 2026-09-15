from pydantic import BaseModel


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    categoria: str
    
    
class ProductoCreate(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    categoria: str
    
class ProductoUpdate(BaseModel):
    nombre: str
    precio: float
    categoria: str