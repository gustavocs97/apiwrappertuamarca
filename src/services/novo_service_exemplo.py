#novo_service_exemplo.py
import os
import asyncio
from fastapi import HTTPException
from typing import Optional
from config import Settings
import shutil

# Serviço responsável pelo processamento de arquivos
class NovoWrapperService:
    def __init__(self):
        self.settings = Settings()  # Carrega configurações
        self.timeout = 30.0  # Timeout de 30 segundos para processamento

    async def process_file(self, file_path: str) -> dict:
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo {file_path} não encontrado para processamento.")
        
        try:
            # Simula o processamento do arquivo (por exemplo, análise de dados)
            await asyncio.sleep(5)  # Simula 5 segundos de processamento
            
            # Retorno simulado após o processamento
            processed_data = {
                "file_path": file_path,
                "status": "processed",
                "message": "Processamento concluído com sucesso!"
            }
            
            return processed_data

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

    async def move_file_to_processed(self, file_path: str) -> str:
        # Diretório onde os arquivos processados serão armazenados
        processed_dir = self.settings.PROCESSED_FILES_PATH
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)  # Cria o diretório se não existir
        
        try:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(processed_dir, file_name)
            
            # Move o arquivo para o diretório de 'processados'
            shutil.move(file_path, destination_path)
            return destination_path

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao mover arquivo: {str(e)}")

    async def cleanup_old_files(self, directory: str, max_age: int) -> None:
        # Limpeza de arquivos antigos
        try:
            current_time = asyncio.get_event_loop().time()
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                file_mod_time = os.path.getmtime(file_path)
                
                # Remove arquivos que ultrapassaram o tempo máximo configurado
                if current_time - file_mod_time > max_age:
                    os.remove(file_path)
                    print(f"Arquivo {file_name} removido, pois excedeu o tempo máximo.")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao limpar arquivos: {str(e)}")
