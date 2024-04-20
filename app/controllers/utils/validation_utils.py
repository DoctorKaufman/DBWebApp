from datetime import datetime
import re


def is_adult(birth_date_str):
    MINIMUM_AGE = 18
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        current_date = datetime.now().date()

        age = current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        if age >= MINIMUM_AGE:
            return True
        else:
            return False

    except ValueError:
        print("Invalid birth date format of birth date. Please use YYYY-MM-DD.")
        return False


def validate_phone_number(phone_number):
    MAX_LENGTH = 13
    if not phone_number or len(phone_number) > MAX_LENGTH:
        return False
    pattern = re.compile(r'^\+\d{12}$')
    if not pattern.match(phone_number):
        return False
    return True
