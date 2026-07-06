from datetime import date, datetime

from rest_framework.exceptions import ValidationError


def validate_age(token):
    birthdate = token.get("birthdate")

    if birthdate is None:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()

    today = date.today()

    age = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day)))

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")