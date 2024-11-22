# src/services/image_storage_service.py
import os
import uuid
import time
from threading import Thread
from config import Settings
import shutil

class ImageStorageService:
    def __init__(self):
        self.settings = Settings()

        # Cria o diretório para armazenar as imagens, caso não exista
        os.makedirs(self.settings.IMAGE_STORAGE_PATH, exist_ok=True)

        # Rotina para limpar arquivos expirados
        self.cleanup_thread = Thread(target=self._cleanup_expired_files, daemon=True)
        self.cleanup_thread.start()

    def save_temporary(self, image_data: bytes) -> str:
        file_id = f"{uuid.uuid4().hex}_{int(time.time())}.png"
        file_path = os.path.join(self.settings.IMAGE_STORAGE_PATH, file_id)

        # Salva os dados da imagem
        with open(file_path, "wb") as file:
            file.write(image_data)

        return file_id

    def get_file_path(self, file_id: str) -> str:
        file_path = os.path.join(self.settings.IMAGE_STORAGE_PATH, file_id)
        if os.path.exists(file_path):
            return file_path
        return None

    def _cleanup_expired_files(self):
        while True:
            now = time.time()
            for file_name in os.listdir(self.settings.IMAGE_STORAGE_PATH):
                file_path = os.path.join(self.settings.IMAGE_STORAGE_PATH, file_name)
                if os.path.isfile(file_path):
                    creation_time = os.path.getctime(file_path)
                    if now - creation_time > self.settings.MAX_IMAGE_STORAGE_TIME:
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Erro ao remover o arquivo {file_path}: {str(e)}")

            time.sleep(60)  # Intervalo de 60 segundos antes da próxima verificação
