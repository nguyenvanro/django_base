from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return None

    raw_data = response.data
    if isinstance(raw_data, dict):
        error_values = []
        for key, value in raw_data.values():
            if isinstance(value, list):
                error_values += [str(item) for item in value]
            else:
                error_values.append(str(value))

        message = "; ".join(error_values)
    
    else:
        message = str(raw_data)

    response.data = {
        "status": response.status_code,
        "message": message,
        "errors": raw_data,
    }

    return response
