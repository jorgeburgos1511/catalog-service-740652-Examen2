from typing import Literal
from pydantic import BaseModel, field_validator


class DomicilioBase(BaseModel):
    cliente_id: str
    domicilio: str
    colonia: str
    municipio: str
    estado: str
    tipo_direccion: Literal["FACTURACION", "ENVIO"]

    @field_validator("cliente_id", "domicilio", "colonia", "municipio", "estado")
    @classmethod
    def validate_fields(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Campo inválido o demasiado corto")
        return value


class DomicilioCreate(DomicilioBase):
    pass


class DomicilioUpdate(DomicilioBase):
    pass


class DomicilioResponse(DomicilioBase):
    id: str