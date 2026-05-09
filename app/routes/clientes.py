from uuid import uuid4
from fastapi import APIRouter, HTTPException
from app.config import CLIENTES_TABLE
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.dynamodb_service import (
    put_item,
    scan_items,
    get_item_by_id,
    update_item_by_id,
    delete_item_by_id,
)

router = APIRouter()


@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate):
    nuevo = {
        "id": str(uuid4()),
        "razon_social": cliente.razon_social,
        "nombre_comercial": cliente.nombre_comercial,
        "rfc": cliente.rfc,
        "correo": cliente.correo,
        "telefono": cliente.telefono,
    }
    put_item(CLIENTES_TABLE, nuevo)
    return nuevo


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes():
    return scan_items(CLIENTES_TABLE)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: str):
    cliente = get_item_by_id(CLIENTES_TABLE, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: str, data: ClienteUpdate):
    if not get_item_by_id(CLIENTES_TABLE, cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return update_item_by_id(CLIENTES_TABLE, cliente_id, {
        "razon_social": data.razon_social,
        "nombre_comercial": data.nombre_comercial,
        "rfc": data.rfc,
        "correo": data.correo,
        "telefono": data.telefono,
    })


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: str):
    if not delete_item_by_id(CLIENTES_TABLE, cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado correctamente"}