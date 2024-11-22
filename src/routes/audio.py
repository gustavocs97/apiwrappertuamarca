import os
from fastapi import APIRouter, HTTPException, Request
from services.audio_service import AudioService
from services.storage_service import StorageService
from fastapi.responses import FileResponse
import datetime
from config import Settings

router = APIRouter()
audio_service = AudioService()
storage_service = StorageService()
settings = Settings()  # Instantiate configurations

# Read the API key from the environment
API_KEY = os.getenv("API_KEY_OFWRAPPER")

@router.post("/speech")
async def create_speech(request: Request):
    # Verify the presence of the Authorization header
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=403, detail="Missing authorization header")

    auth_header = request.headers["Authorization"]
    if auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        request_data = await request.json()
        print(f"Received request data: {request_data}")

        # Forward request to original API
        audio_data = await audio_service.generate_speech(request_data)
        print("Audio data generated successfully.")

        # Temporarily save
        file_id = await storage_service.save_temporary(audio_data)
        
        return {
            "url": f"{request.base_url}api/v1/download/{file_id}",
            "expires_in": storage_service.settings.MAX_STORAGE_TIME
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/download/{file_id}")
async def download_audio(file_id: str):
    file_path = storage_service.get_file_path(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Audio not found or expired")
    return FileResponse(file_path)

@router.get("/health")
async def health_check():
    api_health = await audio_service.health_check()
    storage_health = storage_service.check_storage()
    
    return {
        "status": "healthy" if api_health and storage_health else "unhealthy",
        "original_api": "up" if api_health else "down",
        "storage": "ok" if storage_health else "error",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@router.get("/voices/all")
async def get_all_voices():
    try:
        voices_data = await audio_service.fetch_voices()
        return {"voices": voices_data["voices"]}  # Format response correctly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





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

