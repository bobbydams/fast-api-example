from fastapi import APIRouter

from apps.api import APP_NAME

router = APIRouter()


@router.get("/")
async def index():
    """Index of application
    ---
    responses:
      '200':
        description: Index
        content:
          application/json:
            schema:
              application: string
    """
    return dict(application=f"{APP_NAME} API")
