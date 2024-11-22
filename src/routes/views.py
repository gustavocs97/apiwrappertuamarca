# src/routes/views.py
import os

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates


from config import Settings


router = APIRouter()
templates = Jinja2Templates(directory="src/templates")
settings = Settings()  # Instantiate configurations


# Read the API key from the environment
API_KEY = os.getenv("API_KEY_OFWRAPPER")




@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/config")
async def get_config(request: Request):
    try:
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=403, detail="Missing authorization header")

        auth_header = request.headers["Authorization"]
        if auth_header != f"Bearer {settings.API_KEY_OFWRAPPER}":
            raise HTTPException(status_code=403, detail="Invalid API Key")

        return {
            "apiKey": settings.API_KEY_OFWRAPPER
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

