import re

def validate_data(data):
    data = dict(data)
    csrfmiddlewaretoken = data.pop('csrfmiddlewaretoken')

    values = {}
    errors = {}
    for field_key in data.keys():
        field_value = data.get(field_key, "")
        if field_value in [None, ""]:
            errors[field_key] =  f"{field_key.title()} is required"

        if field_key == "email" and field_value not in [None, ""] and not re.fullmatch(
            r"[^@]+@[^@]+\.[^@]+", field_value
        ):
            errors[field_key] =  "Invalid email format"

        values[field_key] = field_value

    return values, errors