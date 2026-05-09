from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Attr
from app.config import AWS_REGION

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


def get_table(table_name: str):
    return dynamodb.Table(table_name)


def convert_floats_to_decimal(data):
    if isinstance(data, float):
        return Decimal(str(data))
    elif isinstance(data, dict):
        return {key: convert_floats_to_decimal(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_floats_to_decimal(item) for item in data]
    return data


def convert_decimal_to_float(data):
    if isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, dict):
        return {key: convert_decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_decimal_to_float(item) for item in data]
    return data


def put_item(table_name: str, item: dict):
    table = get_table(table_name)
    item = convert_floats_to_decimal(item)
    table.put_item(Item=item)
    return convert_decimal_to_float(item)


def scan_items(table_name: str):
    table = get_table(table_name)
    response = table.scan()
    return convert_decimal_to_float(response.get("Items", []))


def get_item_by_id(table_name: str, item_id: str):
    table = get_table(table_name)
    response = table.get_item(Key={"id": item_id})
    item = response.get("Item")
    return convert_decimal_to_float(item) if item else None


def delete_item_by_id(table_name: str, item_id: str):
    table = get_table(table_name)
    response = table.delete_item(Key={"id": item_id}, ReturnValues="ALL_OLD")
    deleted = response.get("Attributes")
    return convert_decimal_to_float(deleted) if deleted else None


def update_item_by_id(table_name: str, item_id: str, update_data: dict):
    table = get_table(table_name)
    update_data = convert_floats_to_decimal(update_data)

    parts = []
    attr_values = {}
    attr_names = {}

    for key, value in update_data.items():
        parts.append(f"#{key} = :{key}")
        attr_names[f"#{key}"] = key
        attr_values[f":{key}"] = value

    response = table.update_item(
        Key={"id": item_id},
        UpdateExpression="SET " + ", ".join(parts),
        ExpressionAttributeNames=attr_names,
        ExpressionAttributeValues=attr_values,
        ReturnValues="ALL_NEW",
    )
    updated = response.get("Attributes")
    return convert_decimal_to_float(updated) if updated else None