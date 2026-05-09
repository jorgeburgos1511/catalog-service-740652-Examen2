from uuid import uuid4
from fastapi import APIRouter, HTTPException
from app.config import DOMICILIOS_TABLE, CLIENTES_TABLE
from app.schemas.domicilio import DomicilioCreate, DomicilioResponse, DomicilioUpdate
from app.services.dynamodb_service import (
    put_item, scan_items, get_item_by_id, update_item_by_id, delete_item_by_id,
)

router = APIRouter()


@router.post("/", response_model=DomicilioResponse)
def crear_domicilio(domicilio: DomicilioCreate):
    if not get_item_by_id(CLIENTES_TABLE, domicilio.cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    nuevo = {
        "id": str(uuid4()),
        "cliente_id": domicilio.cliente_id,
        "domicilio": domicilio.domicilio,
        "colonia": domicilio.colonia,
        "municipio": domicilio.municipio,
        "estado": domicilio.estado,
        "tipo_direccion": domicilio.tipo_direccion,
    }
    put_item(DOMICILIOS_TABLE, nuevo)
    return nuevo


@router.get("/", response_model=list[DomicilioResponse])
def listar_domicilios():
    return scan_items(DOMICILIOS_TABLE)


@router.get("/{domicilio_id}", response_model=DomicilioResponse)
def obtener_domicilio(domicilio_id: str):
    d = get_item_by_id(DOMICILIOS_TABLE, domicilio_id)
    if not d:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    return d


@router.put("/{domicilio_id}", response_model=DomicilioResponse)
def actualizar_domicilio(domicilio_id: str, data: DomicilioUpdate):
    if not get_item_by_id(DOMICILIOS_TABLE, domicilio_id):
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    if not get_item_by_id(CLIENTES_TABLE, data.cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return update_item_by_id(DOMICILIOS_TABLE, domicilio_id, {
        "cliente_id": data.cliente_id,
        "domicilio": data.domicilio,
        "colonia": data.colonia,
        "municipio": data.municipio,
        "estado": data.estado,
        "tipo_direccion": data.tipo_direccion,
    })


@router.delete("/{domicilio_id}")
def eliminar_domicilio(domicilio_id: str):
    if not delete_item_by_id(DOMICILIOS_TABLE, domicilio_id):
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    return {"message": "Domicilio eliminado correctamente"}