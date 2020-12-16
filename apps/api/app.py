import json

from fastapi.responses import JSONResponse

from apps.api.domain.library import DomainException

APP_NAME = "Fast API Example"

from apps.api import context
from apps.api.routes import default, book

from fastapi import FastAPI

app = FastAPI()
context = context.Context()

app.include_router(default.router)
app.include_router(book.router)


@app.exception_handler(DomainException)
def handle_invalid_usage(response, error):
    return JSONResponse(error.to_dict(), status_code=error.status_code)