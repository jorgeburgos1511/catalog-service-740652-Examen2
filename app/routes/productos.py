from uuid import uuid4
from fastapi import APIRouter, HTTPException
from app.config import PRODUCTOS_TABLE
from app.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from app.services.dynamodb_service import (
    put_item, scan_items, get_item_by_id, update_item_by_id, delete_item_by_id,
)

router = APIRouter()


@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate):
    nuevo = {
        "id": str(uuid4()),
        "nombre": producto.nombre,
        "unidad_medida": producto.unidad_medida,
        "precio_base": producto.precio_base,
    }
    put_item(PRODUCTOS_TABLE, nuevo)
    return nuevo


@router.get("/", response_model=list[ProductoResponse])
def listar_productos():
    return scan_items(PRODUCTOS_TABLE)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: str):
    p = get_item_by_id(PRODUCTOS_TABLE, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: str, data: ProductoUpdate):
    if not get_item_by_id(PRODUCTOS_TABLE, producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return update_item_by_id(PRODUCTOS_TABLE, producto_id, {
        "nombre": data.nombre,
        "unidad_medida": data.unidad_medida,
        "precio_base": data.precio_base,
    })


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: str):
    if not delete_item_by_id(PRODUCTOS_TABLE, producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}