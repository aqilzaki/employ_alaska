from flask import request

def get_request_data(include_files=False):
    """
    Support JSON, form-data, and files
    """
    data = {}

    if request.is_json:
        data.update(request.get_json() or {})
    else:
        data.update(request.form.to_dict())

    if include_files:
        data.update(request.files.to_dict())

    return data
