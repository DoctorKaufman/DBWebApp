from datetime import datetime
import re

from app.controllers.handler.exceptions import ValidationException


def is_adult(birth_date_str):
    MINIMUM_AGE = 18
    birth_date = parse_date(birth_date_str)
    current_date = datetime.now().date()

    age = current_date.year - birth_date.year - (
            (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    if age >= MINIMUM_AGE:
        return True
    else:
        print('Employee age should be greater or equal to 18')
        return False


def parse_date(date_string):
    try:
        birth_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        return birth_date
    except ValueError:
        print("Invalid birth date format of birth date. Please use YYYY/MM/DD.")
        raise ValidationException("Invalid birth date format of birth date. Please use YYYY/MM/DD.")


def validate_phone_number(phone_number):
    MAX_LENGTH = 13
    if not phone_number or len(phone_number) > MAX_LENGTH:
        return False
    pattern = re.compile(r'^\+\d{12}$')
    if not pattern.match(phone_number):
        return False
    return True
