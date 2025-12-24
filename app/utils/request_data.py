from flask import request

def get_request_data(include_files=False):
    data = {}

    # JSON (AMAN)
    if request.is_json:
        json_data = request.get_json(silent=True)
        if json_data:
            data.update(json_data)

    # FORM
    if request.form:
        data.update(request.form.to_dict())

    # FILE (INI KUNCI)
    if include_files:
        for key in request.files:
            data[key] = request.files.get(key)

    return data
