from fastapi import FastAPI
from fastapi.responses import JSONResponse

from apps.api import APP_NAME, DESCRIPTION, VERSION, context
from apps.api.config import configure_logging
from apps.api.domain.library import DomainException
from apps.api.routes import default, book

configure_logging()

app = FastAPI(title=f"{APP_NAME} API", description=DESCRIPTION, version=VERSION)
context.Context()

app.include_router(default.router)
app.include_router(book.router)


@app.exception_handler(DomainException)
def handle_invalid_usage(response, error):
    return JSONResponse(error.to_dict(), status_code=error.status_code)
