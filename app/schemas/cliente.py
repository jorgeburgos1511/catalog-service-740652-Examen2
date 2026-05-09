from pydantic import BaseModel, EmailStr, field_validator
from app.utils.validators import is_valid_rfc, is_valid_phone


class ClienteBase(BaseModel):
    razon_social: str
    nombre_comercial: str
    rfc: str
    correo: EmailStr
    telefono: str

    @field_validator("razon_social", "nombre_comercial")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Debe tener al menos 2 caracteres")
        return value

    @field_validator("rfc")
    @classmethod
    def validate_rfc(cls, value: str) -> str:
        value = value.strip().upper()
        if not is_valid_rfc(value):
            raise ValueError("RFC inválido")
        return value

    @field_validator("telefono")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        value = value.strip()
        if not is_valid_phone(value):
            raise ValueError("Teléfono inválido")
        return value


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: str