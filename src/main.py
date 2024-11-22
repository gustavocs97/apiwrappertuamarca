# src/main.py






# Aqui estão as instruções sobre como adicionar novos wrappers à API.
# Estas instruções servem para facilitar a adição de novos módulos/funcionalidades na API.

# INSERIR NOVAS CONFIGURAÇÕES AQUI
# Para adicionar suporte a um novo wrapper:
# 1. Crie o arquivo do roteador em `src/routes/novo_wrapper.py`.
#    Exemplo: `src/routes/novo_wrapper.py`
#
# 2. Importe o roteador aqui:
#    Exemplo: 
#    from routes import novo_wrapper
#
# 3. Inclua o roteador no app usando `include_router`:
#    Exemplo:
#    app.include_router(novo_wrapper.router, prefix="/api/v1/novo", tags=["novo_wrapper"])
#
# 4. Se necessário, monte um diretório estático para arquivos (caso o novo wrapper manipule arquivos temporários):
#    Exemplo:
#    app.mount("/temp_novo", StaticFiles(directory="temp_novo_wrapper"), name="temp_novo")


# src/main.py

# Importação das dependências essenciais do FastAPI, para criação da API
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates  # Usado para renderizar templates HTML
from fastapi.staticfiles import StaticFiles  # Usado para servir arquivos estáticos (CSS, JS, etc.)
from fastapi.responses import FileResponse  # Usado para retornar arquivos como resposta
import uvicorn  # Usado para rodar o servidor
from config import Settings  # Importa a classe Settings para acessar configurações

# Importação das rotas específicas da aplicação
from routes import audio, views, image  # Roteadores para áudio, views e imagens

# Criação da instância principal da aplicação FastAPI
app = FastAPI(title="Audio Wrapper API")

# Configuração para servir arquivos estáticos da pasta "src/static", como imagens ou arquivos JS/CSS
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Inicialização do Jinja2 para renderização de templates HTML. Aqui a pasta de templates é definida.
templates = Jinja2Templates(directory="src/templates")

# Inclusão das rotas da API. Cada uma delas tem um prefixo e tags para organização:
# - A rota "audio" responde à prefixo "/api/v1/audio".
# - A rota "views" pode servir páginas HTML ou outros recursos.
# - A rota "image" responde para manipulação de imagens (geração, download, etc.)
app.include_router(audio.router, prefix="/api/v1", tags=["audio"])
app.include_router(views.router)

# Inclusão da rota de imagens, com o prefixo "/api/v1/images" e a tag "images"
app.include_router(image.router, prefix="/api/v1/images", tags=["images"])

# Monta o diretório de arquivos estáticos para imagens temporárias. 
# Isso permite acessar imagens via URL, por exemplo, `/temp_images/<image_file>`
app.mount("/temp_images", StaticFiles(directory="temp_images"), name="temp_images")


# Este código é executado quando o script é rodado diretamente, iniciando o servidor com Uvicorn.
# O servidor será iniciado no endereço 0.0.0.0 (toda a rede) e na porta configurada em Settings().PORT.
# O `reload=True` significa que o servidor será recarregado automaticamente durante o desenvolvimento
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=Settings().PORT, reload=True)
