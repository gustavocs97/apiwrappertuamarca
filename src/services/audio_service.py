import httpx
from fastapi import HTTPException
from config import Settings
import asyncio
from typing import Optional

class AudioService:
    def __init__(self):
        self.settings = Settings()
        self.timeout = httpx.Timeout(30.0)  # 30 segundos timeout

    async def generate_speech(self, request_data: dict) -> bytes:
        headers = {
            "Authorization": f"Bearer {self.settings.API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.settings.ORIGINAL_API_URL}/v1/audio/speech",
                    headers=headers,
                    json=request_data
                )

                response.raise_for_status()  # Levanta um erro para códigos de status não 200
                return response.content

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Request timeout")
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error connecting to original API: {str(e)}")
        except Exception as e:
            # Logando erro inesperado
            print(f"Unexpected error in generate_speech: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    async def fetch_voices(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self.settings.API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.settings.ORIGINAL_API_URL}/v1/voices/all", headers=headers)
                response.raise_for_status()
                return response.json()

        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error connecting to original API: {str(e)}")
        except Exception as e:
            # Logando erro inesperado
            print(f"Unexpected error in fetch_voices: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    async def health_check(self) -> Optional[bool]:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.settings.API_KEY}"
                }
                response = await client.get(f"{self.settings.ORIGINAL_API_URL}/v1/models", headers=headers)
                return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {str(e)}")
            return False
