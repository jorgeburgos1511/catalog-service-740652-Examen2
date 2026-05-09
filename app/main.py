from fastapi import FastAPI
from app.routes import clientes, domicilios, productos
from app.config import SERVICE_NAME, ENVIRONMENT

app = FastAPI(
    title="Catalog Service",
    description="Microservicio de catálogos: clientes, domicilios y productos",
    version="2.0.0",
)


@app.get("/")
def root():
    return {"service": SERVICE_NAME, "environment": ENVIRONMENT, "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME}


app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(domicilios.router, prefix="/domicilios", tags=["Domicilios"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])