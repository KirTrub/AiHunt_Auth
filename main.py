from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from exceptions.exceptions import AppException
from handlers.api import app
from handlers.error_handlers import app_exception_handler, unexpected_exception_handler

load_dotenv()

app.add_exception_handler(AppException, app_exception_handler)

app.add_exception_handler(Exception, unexpected_exception_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )