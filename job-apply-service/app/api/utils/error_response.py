from fastapi.responses import JSONResponse

def error_response(status_code, message):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "success": False,
            "message": message,
            "data": None
        }
    )
