import boto3
from app.config import AWS_REGION, ENVIRONMENT, SERVICE_NAME

cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)

NAMESPACE = "Examen2/Microservicios"


def _get_range(status_code: int) -> str:
    if 200 <= status_code < 300:
        return "2xx"
    elif 400 <= status_code < 500:
        return "4xx"
    elif 500 <= status_code < 600:
        return "5xx"
    return "other"


def put_http_metric(status_code: int):
    status_range = _get_range(status_code)
    try:
        cloudwatch.put_metric_data(
            Namespace=NAMESPACE,
            MetricData=[{
                "MetricName": f"HTTPStatus_{status_range}",
                "Dimensions": [
                    {"Name": "Service", "Value": SERVICE_NAME},
                    {"Name": "Environment", "Value": ENVIRONMENT},
                ],
                "Value": 1,
                "Unit": "Count",
            }],
        )
    except Exception as e:
        print(f"[metrics] Error HTTP metric: {e}")


def put_latency_metric(duration_ms: float, endpoint: str):
    try:
        cloudwatch.put_metric_data(
            Namespace=NAMESPACE,
            MetricData=[{
                "MetricName": "EndpointLatency",
                "Dimensions": [
                    {"Name": "Service", "Value": SERVICE_NAME},
                    {"Name": "Environment", "Value": ENVIRONMENT},
                    {"Name": "Endpoint", "Value": endpoint},
                ],
                "Value": duration_ms,
                "Unit": "Milliseconds",
            }],
        )
    except Exception as e:
        print(f"[metrics] Error latency metric: {e}")