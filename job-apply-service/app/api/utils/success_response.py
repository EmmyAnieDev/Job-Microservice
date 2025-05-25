from fastapi.responses import JSONResponse

def success_response(status_code, message, data):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "success": True,
            "message": message,
            "data": data
        }
    )