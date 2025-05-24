def success_response(status_code, message, data):
    return {
        "status_code": status_code,
        "success": True,
        "message": message,
        "data": data
    }, status_code