#novo_storage_service_exemplo.py
import os
import shutil
from fastapi import HTTPException
from config import Settings
from typing import Optional
from datetime import datetime, timedelta
import uuid

# Serviço para armazenamento de arquivos
class NovoStorageService:
    def __init__(self):
        self.settings = Settings()  # Carrega configurações

    #Salva um arquivo no diretório especificado e retorna o caminho do arquivo salvo.
    async def save_file(self, file, directory: str) -> str:
        try:
            # Verifica se o diretório existe, se não, cria
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Gera um nome único para o arquivo
            file_name = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = os.path.join(directory, file_name)
            
            # Salva o arquivo no diretório
            with open(file_path, "wb") as f:
                content = await file.read()  # Lê o conteúdo do arquivo
                f.write(content)
            
            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

    #Retorna o caminho de um arquivo no diretório baseado no ID fornecido.
    def get_file_path(self, file_id: str, directory: str) -> Optional[str]:
        try:
            for file_name in os.listdir(directory):
                if file_name.startswith(file_id):
                    return os.path.join(directory, file_name)
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar o arquivo: {str(e)}")

    #Move o arquivo para um novo diretório e retorna o caminho do novo arquivo.
    def move_file_to_directory(self, file_path: str, destination_directory: str) -> str:
        try:
            # Garante que o diretório de destino exista
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            # Gera um novo caminho para o arquivo no diretório de destino
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(destination_directory, file_name)

            # Move o arquivo
            shutil.move(file_path, destination_path)

            return destination_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao mover o arquivo: {str(e)}")

    #Limpa arquivos antigos no diretório que ultrapassaram o tempo máximo de retenção.
    def cleanup_old_files(self, directory: str, max_age: int) -> None:
        try:
            current_time = os.path.getmtime(directory)  # Obtém o tempo atual em segundos
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                file_mod_time = os.path.getmtime(file_path)
                
                # Se o arquivo for mais antigo que o tempo máximo
                if current_time - file_mod_time > max_age:
                    os.remove(file_path)
                    print(f"Arquivo {file_name} removido, pois excedeu o tempo máximo.")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao limpar arquivos: {str(e)}")
