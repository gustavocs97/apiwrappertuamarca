#novo_wrapper_exemplo.py
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
from services.novo_service import process_item
from services.novo_storage_service import save_file, cleanup_old_files
from config import Settings
import os
import asyncio

# Criação de um roteador para a API (responsável por agrupar rotas)
router = APIRouter()

# Carrega as configurações da aplicação e define a chave da API
settings = Settings()
API_KEY_OFWRAPPER = os.getenv("API_KEY_OFWRAPPER")  # Chave de autenticação para a API

# Modelo Pydantic para a requisição, utilizado para validação de dados
class ProcessRequest(BaseModel):
    auto_delete: bool  # Flag para controlar a exclusão automática após o processamento
    
# Endpoint para processar arquivos enviados via POST
@router.post("/process")
async def process_novo_wrapper(request: Request, file: UploadFile = File(...), process_request: ProcessRequest = ProcessRequest(auto_delete=True)):
    # Verificação da presença de cabeçalho de autenticação
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=403, detail="Missing authorization header")
    
    # Validação da chave de autenticação
    auth_header = request.headers["Authorization"]
    if auth_header != f"Bearer {API_KEY_OFWRAPPER}":
        raise HTTPException(status_code=403, detail="Invalid API Key")

    try:
        # Salva o arquivo temporariamente no diretório especificado
        file_path = await save_file(file, directory="temp_novo_wrapper")

        # Processa o arquivo salvo
        result = await process_item(file_path)

        # Limpeza de arquivos antigos no diretório temporário
        cleanup_old_files(directory="temp_novo_wrapper", max_age=300)

        # Geração da URL de download do arquivo processado
        file_url = f"{request.base_url}api/v1/novo_wrapper/download/{os.path.basename(file_path)}"

        # Se a opção de auto_delete estiver habilitada, agenda a exclusão do arquivo após o tempo configurado
        if process_request.auto_delete:
            asyncio.create_task(delete_file_after_timeout(file_path))

        # Resposta com sucesso e detalhes do processamento
        return {"status": "success", "data": result, "file_url": file_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

# Função que agenda a exclusão do arquivo após o tempo configurado
async def delete_file_after_timeout(file_path: str):
    await asyncio.sleep(settings.MAX_STORAGE_TIME)  # Aguarda o tempo configurado
    if os.path.exists(file_path):
        os.remove(file_path)  # Exclui o arquivo
        print(f"Arquivo {file_path} excluído após o tempo limite.")

# Endpoint para download de arquivos processados
@router.get("/download/{file_name}")
async def download_processed_file(file_name: str):
    # Verifica o caminho completo do arquivo a ser baixado
    file_path = os.path.join("temp_novo_wrapper", file_name)
    
    # Caso o arquivo não seja encontrado, retorna um erro 404
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado ou expirado")

    # Retorna o arquivo como resposta
    return FileResponse(file_path)
