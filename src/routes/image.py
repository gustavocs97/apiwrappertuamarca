#src/routes/image.py

from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.image_service import ImageService
from services.image_storage_service import ImageStorageService
from config import Settings
import os
import asyncio

router = APIRouter()

# Inicializando os serviços
image_service = ImageService()
storage_service = ImageStorageService()
settings = Settings()

# Modelo Pydantic para os parâmetros da requisição
class GenerateImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = "Ugly, unrealistic"
    auto_delete: bool = True

class GenerateImageResponse(BaseModel):
    success: bool
    image_url: str
    expires_in: int = None

# Define the security scheme (used only in routes that require auth)
security = HTTPBearer()

# Image generation route with authentication (API Key required)
@router.post("/generate", response_model=GenerateImageResponse)
async def generate_image(
    request: Request,
    generate_request: GenerateImageRequest,
    credentials: HTTPAuthorizationCredentials = Security(security)  # Security applied here
):
    # Verifica se o token Bearer corresponde à chave API esperada
    if credentials.credentials != os.getenv("API_KEY_OFWRAPPER"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    try:
        # Gera a imagem usando os parâmetros do corpo da requisição
        image_data = await image_service.generate_image(generate_request.prompt, generate_request.negative_prompt)

        # Salva a imagem temporária no diretório
        image_hash = storage_service.save_temporary(image_data)

        # Gera a URL pública da imagem (no need for authentication to access this URL)
        image_url = f"{request.base_url}api/v1/images/download/{image_hash}"

        # Caso tenha auto-delete, agenda a exclusão da imagem após o tempo máximo
        if generate_request.auto_delete:
            asyncio.create_task(delete_image_after_timeout(image_hash))

        return {
            "success": True,
            "image_url": image_url,
            "expires_in": settings.MAX_IMAGE_STORAGE_TIME if generate_request.auto_delete else None
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar a imagem: {str(e)}")

# Função para agendar a exclusão da imagem após o tempo máximo
async def delete_image_after_timeout(image_hash: str):
    await asyncio.sleep(settings.MAX_IMAGE_STORAGE_TIME)
    image_path = os.path.join(settings.IMAGE_STORAGE_PATH, image_hash)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Imagem {image_hash} excluída após o tempo limite.")

# Image download route (public access, no authentication)
@router.get("/download/{file_id}")
async def download_image(file_id: str):
    # No authentication required here; anyone can access the image
    file_path = storage_service.get_file_path(file_id)
    print(f"Tentando acessar o arquivo: {file_path}")
    
    # Se o arquivo não for encontrado, retorna um erro 404
    if not file_path:
        raise HTTPException(status_code=404, detail="Imagem não encontrada ou expirada")
    
    # Retorna o arquivo de imagem como resposta
    return FileResponse(file_path)
