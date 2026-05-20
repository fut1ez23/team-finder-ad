import re

from django.core.exceptions import ValidationError


PHONE_PATTERN = re.compile(r"^(8\d{10}|\+7\d{10})$")


def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    if phone.startswith("8") and len(phone) == 11:
        return "+7" + phone[1:]
    return phone


def validate_phone(value: str) -> str:
    if not PHONE_PATTERN.match(value):
        raise ValidationError(
            "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
        )
    return normalize_phone(value)


def validate_github_url(value: str) -> str:
    if not value:
        return value
    if "github.com" not in value:
        raise ValidationError("Ссылка должна вести на GitHub")
    return value
