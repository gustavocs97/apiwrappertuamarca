# src/routes/audio.py

import os
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.audio_service import AudioService
from services.storage_service import StorageService
from config import Settings
import datetime

router = APIRouter()
audio_service = AudioService()
storage_service = StorageService()
settings = Settings()  # Instantiate configurations

# Define the security scheme (used only in routes that require auth)
security = HTTPBearer()

# Modelo Pydantic para os parâmetros da requisição
class SpeechRequest(BaseModel):
    input: str  # O texto a ser convertido em fala
    voice: str = "pt-PT-RaquelNeural"  # Valor padrão para a voz
    model: str = "tts-1"  # Valor padrão para o modelo
    response_format: str = "mp3"  # Valor padrão para o formato de resposta

# Rota para gerar fala a partir de texto
@router.post("/speech")
async def create_speech(
    request: Request,
    speech_request: SpeechRequest,  # Usando o modelo Pydantic com valores padrão
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Verifica se o token Bearer corresponde à chave API esperada
    if credentials.credentials != os.getenv("API_KEY_OFWRAPPER"):
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        # 'speech_request.input' contém o texto de entrada, e os outros campos têm valores padrão
        request_data = {
            "input": speech_request.input,
            "voice": speech_request.voice,
            "model": speech_request.model,
            "response_format": speech_request.response_format
        }
        print(f"Received request data: {request_data}")

        # Encaminha a requisição para a API original para gerar a fala
        audio_data = await audio_service.generate_speech(request_data)
        print("Audio data generated successfully.")

        # Salva e retorna a URL do áudio
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




# Rota para download do áudio
@router.get("/download/{file_id}")
async def download_audio(file_id: str):
    file_path = storage_service.get_file_path(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Audio not found or expired")
    return FileResponse(file_path)

# Rota para checar a saúde da API
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

# Rota para buscar todas as vozes disponíveis
@router.get("/voices/all")
async def get_all_voices(
    credentials: HTTPAuthorizationCredentials = Security(security)  # Security applied here
):
    # Verifica se o token Bearer corresponde à chave API esperada
    if credentials.credentials != os.getenv("API_KEY_OFWRAPPER"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    try:
        voices_data = await audio_service.fetch_voices()
        return {"voices": voices_data["voices"]}  # Formata a resposta corretamente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

