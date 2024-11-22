# src/services/image_service.py
import httpx
from fastapi import HTTPException
from config import Settings
import asyncio
from typing import Optional

class ImageService:
    def __init__(self):
        self.settings = Settings()
        self.timeout = httpx.Timeout(30.0)  # Timeout de 30 segundos para requisições

    async def generate_image(self, prompt: str, negative_prompt: Optional[str] = "Ugly, unrealistic") -> bytes:
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }

        headers = {
            "Authorization": f"Bearer {self.settings.IMAGE_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            # Faz a requisição assíncrona para a API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.settings.IMAGE_API_URL,
                    headers=headers,
                    json=payload
                )

                # Levanta uma exceção se a resposta não for bem-sucedida (status 2xx)
                response.raise_for_status()

                return response.content  # Retorna os bytes da imagem gerada

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Request timeout")
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error connecting to the image API: {str(e)}")
        except Exception as e:
            print(f"Unexpected error in generate_image: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
