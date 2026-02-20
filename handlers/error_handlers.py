# handlers/error_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.exceptions import AppException

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "code": exc.status_code
        },
    )

async def unexpected_exception_handler(request: Request, exc: Exception):
    print(f"CRITICAL ERROR: {exc}") 
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "code": "INTERNAL_SERVER_ERROR"
        },
    )