import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

CLIENTES_TABLE = os.getenv("CLIENTES_TABLE", "clientes")
DOMICILIOS_TABLE = os.getenv("DOMICILIOS_TABLE", "domicilios")
PRODUCTOS_TABLE = os.getenv("PRODUCTOS_TABLE", "productos")

SERVICE_NAME = "catalog-service"
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8001"))