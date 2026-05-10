import time
from fastapi import FastAPI, Request
from app.routes import clientes, domicilios, productos
from app.config import SERVICE_NAME, ENVIRONMENT
from app.services.metrics_service import put_http_metric, put_latency_metric

app = FastAPI(
    title="Catalog Service",
    description="Microservicio de catálogos: clientes, domicilios y productos",
    version="2.0.0",
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000

    endpoint = f"{request.method} {request.url.path}"
    put_http_metric(response.status_code)
    put_latency_metric(duration_ms, endpoint)

    return response


@app.get("/")
def root():
    return {"service": SERVICE_NAME, "environment": ENVIRONMENT, "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME}


app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(domicilios.router, prefix="/domicilios", tags=["Domicilios"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])