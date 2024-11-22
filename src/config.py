# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):




    # Configurações Gerais
    PORT: int = 5051
    API_KEY_OFWRAPPER: str  # Chave para autenticar o wrapper


    # Configurão da API original de audio
    ORIGINAL_API_URL: str
    API_KEY: str  # Chave da API do serviço original de audio
    STORAGE_PATH: str = "./temp_audio"
    MAX_STORAGE_TIME: int = 120  # segundos



    # Configurações de Imagem 
    IMAGE_API_URL: str
    IMAGE_API_KEY: str
    IMAGE_STORAGE_PATH: str = "./temp_images"
    MAX_IMAGE_STORAGE_TIME: int = 300  # Tempo máximo em segundos para as imagens


    # INSERIR NOVAS CONFIGURAÇÕES AQUI
    # Para adicionar um novo wrapper:
    # 1. Declare as variáveis de configuração específicas do novo wrapper.
    #    Exemplo:
    #        NOVO_WRAPPER_API_URL: str  # URL do novo serviço
    #        NOVO_WRAPPER_API_KEY: str  # Chave de autenticação do novo serviço
    #        NOVO_STORAGE_PATH: str = "./temp_novo_wrapper"  # Caminho de armazenamento para arquivos
    #        NOVO_MAX_STORAGE_TIME: int = 300  # Tempo máximo de armazenamento (em segundos)







    class Config:
        env_file = ".env"  # Carrega as variáveis de ambiente a partir do arquivo .env








# Instância das configurações
settings = Settings()
