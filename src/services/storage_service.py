# src/services/storage_service.py
import os
import uuid
import time
import asyncio
from config import Settings
import shutil

class StorageService:
    def __init__(self):
        self.settings = Settings()
        self.ensure_storage_directory()
        
    def ensure_storage_directory(self):
        os.makedirs(self.settings.STORAGE_PATH, exist_ok=True)
        
    async def save_temporary(self, audio_data: bytes) -> str:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.settings.STORAGE_PATH, f"{file_id}.mp3")
        
        with open(file_path, "wb") as f:
            f.write(audio_data)
            
        # Agenda remoção
        asyncio.create_task(self.delete_after_timeout(file_id))
        return file_id
        
    async def delete_after_timeout(self, file_id: str):
        await asyncio.sleep(self.settings.MAX_STORAGE_TIME)
        self.delete_file(file_id)
        
    def delete_file(self, file_id: str):
        file_path = self.get_file_path(file_id)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            
    def get_file_path(self, file_id: str) -> str:
        file_path = os.path.join(self.settings.STORAGE_PATH, f"{file_id}.mp3")
        if os.path.exists(file_path):
            return file_path
        return None
    


    def check_storage(self) -> bool:
        """Verifica se o armazenamento está funcionando"""
        try:
            # Verifica se o diretório existe e tem permissões
            if not os.path.exists(self.settings.STORAGE_PATH):
                os.makedirs(self.settings.STORAGE_PATH)
                
            # Tenta criar um arquivo temporário
            test_file = os.path.join(self.settings.STORAGE_PATH, ".test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except:
            return False    