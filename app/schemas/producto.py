from pydantic import BaseModel, Field, field_validator


class ProductoBase(BaseModel):
    nombre: str
    unidad_medida: str
    precio_base: float = Field(gt=0)

    @field_validator("nombre", "unidad_medida")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Debe tener al menos 2 caracteres")
        return value


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoResponse(ProductoBase):
    id: str