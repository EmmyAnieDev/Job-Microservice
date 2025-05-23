def error_response(status_code, message):
    return {
        "status_code": status_code,
        "success": False,
        "message": message,
        "data": None
    }, status_code