from app.controllers.handler.api_error import APIError


def handle_data_duplicate_exception(error):
    error = APIError(400, error.message)
    json_error = error.serialize()
    return json_error, 400
