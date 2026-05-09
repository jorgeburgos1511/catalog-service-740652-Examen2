import re

RFC_REGEX = r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$"
PHONE_REGEX = r"^\+?\d{10,15}$"


def is_valid_rfc(rfc: str) -> bool:
    if not rfc:
        return False
    return re.match(RFC_REGEX, rfc.upper()) is not None


def is_valid_phone(phone: str) -> bool:
    if not phone:
        return False
    return re.match(PHONE_REGEX, phone) is not None