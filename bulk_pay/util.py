class MissingFields(Exception):
    def __init__(self, message):
        self.message = message

def get_form_fields(request, field_list):
    values = []
    missing = []
    for field in field_list:
        if field not in request.form:
            missing.append(field)
            continue
        value = request.form[field]

        if value == "":
            missing.append(field)
        else:
            values.append(value)

    if len(missing) != 0:
        msg = "Please provide missing field(s): " + ", ".join(missing)
        raise MissingFields(msg)

    return values
