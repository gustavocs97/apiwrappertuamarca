# API Wrapper de Áudio e Imagem + EXEMPLO
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-blue)

## Visão Geral
Este projeto é uma API para integração com serviços de áudio e imagem, construída com FastAPI e Docker. A arquitetura foi projetada para permitir a fácil adição de novos wrappers e serviços.

## Funcionalidades
- ✨ Integração com serviços de áudio
- 🖼️ Suporte para API de imagem (exemplo)
- 🔌 Arquitetura extensível para novos wrappers
- 💾 Sistema de armazenamento configurável
- 🐳 Containerização com Docker
- ⚙️ Configuração via variáveis de ambiente



### Interactive API docs¶
Acesse http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI)

## Estrutura do Projeto
```
audio-wrapper-api/
├── src/
│   ├── routes/
│   │   ├── audio.py            # Rotas do serviço de áudio
│   │   ├── image.py            # Rotas do serviço de imagem
│   │   └── novo_wrapper.py     # Template para novos wrappers
│   ├── services/
│   │   ├── audio_service.py          # Lógica do serviço de áudio
│   │   ├── image_service.py          # Lógica do serviço de imagem
│   │   ├── storage_service.py        # Gerenciamento de armazenamento
│   │   └── image_storage_service.py  # Armazenamento específico de imagens
│   ├── main.py                 # Arquivo principal da aplicação
│   └── config.py               # Configurações e variáveis de ambiente
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   └── test_audio_service.py
├── temp_audio/                 # Diretório temporário para áudios
├── temp_images/                # Diretório temporário para imagens
├── Dockerfile                  # Configuração do container
├── docker-compose.yml          # Orquestração de containers
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
└── README.md                  # Esta documentação
```

## Pré-requisitos
- Docker e Docker Compose (recomendado)
- Python 3.11+ (caso não use Docker)
- Git

## Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/audio-wrapper-api.git
cd audio-wrapper-api
```

### 2. Configure as Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

Exemplo de configuração do `.env`:
```env
# Configurações Gerais
API_KEY_OFWRAPPER=sua_chave_api
PORT=8000
LOG_LEVEL=info

# Configurações do Serviço de Áudio
AUDIO_API_URL=https://api.audio.com
AUDIO_API_KEY=sua_chave_audio

# Configurações do Serviço de Imagem
IMAGE_API_URL=https://api.imagem.com
IMAGE_API_KEY=sua_chave_imagem
```

### 3. Execução com Docker (Recomendado)
```bash
# Construa e inicie os containers
docker-compose up --build

# Para executar em background
docker-compose up -d --build
```



## Endpoints da API

### Serviço de Áudio
- `POST /api/v1/audio/process`
  ```bash
  curl -X POST "http://localhost:8000/api/v1/audio/process" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@audio.mp3"
  ```

- `GET /api/v1/audio/status/{job_id}`
  ```bash
  curl "http://localhost:8000/api/v1/audio/status/12345"
  ```

### Serviço de Imagem
- `POST /api/v1/image/process`
- `GET /api/v1/image/status/{job_id}`

## Adicionando Novos Wrappers e Funcionalidades

### 1. Crie os Arquivos Necessários
```bash
touch src/routes/novo_wrapper.py
touch src/services/novo_service.py
touch src/services/novo_storage_service.py
```


### Estrutura para Adicionar um Novo Wrapper

1. **`src/routes/novo_wrapper_exemplo.py`:**  
   - Define as rotas expostas para o wrapper.
   - Responsável por lidar com requisições HTTP e direcioná-las aos serviços adequados.

2. **`src/services/novo_service_exemplo.py`:**  
   - Contém a lógica principal de processamento do wrapper.
   - Este arquivo implementa as funções principais que realizam as operações do wrapper.

3. **`src/services/novo_storage_service_exemplo.py`:**  
   - Gerencia o armazenamento temporário ou persistente relacionado ao wrapper.
   - Responsável por salvar, recuperar e limpar arquivos do wrapper.





### 2. Configure o Armazenamento

   No `Dockerfile` e no `docker-compose.yml`, configure os diretórios para o novo wrapper:
   - Adicione no `Dockerfile`:
     ```dockerfile
     RUN mkdir -p /app/temp_novo_wrapper_exemplo && chmod 777 /app/temp_novo_wrapper_exemplo
     ```
   - Configure no `docker-compose.yml`:
     ```yaml
     volumes:
       - /home/ubuntu/TuaMarca/DockerImagensProprias/apiwrappertuamarca/temp_novo_wrapper_exemplo:/app/temp_novo_wrapper_exemplo
     ```

### 3. Registre as Rotas

Em `src/main.py`:
   ```python
   from routes import novo_wrapper

   app.include_router(novo_wrapper.router, prefix="/api/v1/novo", tags=["novo_wrapper"])
   app.mount("/temp_novo", StaticFiles(directory="temp_novo_wrapper_exemplo"), name="temp_novo")
   ```

### 4. Adicione Configurações

Em `src/config.py`:
```python
NOVO_WRAPPER_API_KEY = os.getenv("NOVO_WRAPPER_API_KEY")
NOVO_WRAPPER_BASE_URL = os.getenv("NOVO_WRAPPER_BASE_URL")
```

## Testes

### Executando Testes
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_audio_service.py -v

# Com cobertura
pytest --cov=src tests/
```

## Resolução de Problemas

### Problemas Comuns

1. **Erro de Permissão nos Diretórios Temporários**
```bash
sudo chown -R $USER:$USER temp_*
chmod 777 temp_*
```

2. **Conflito de Portas**
```bash
# Verifique se a porta está em uso
lsof -i :8000

# Altere a porta no .env se necessário
PORT=8001
```

3. **Problemas com Docker**
```bash
# Limpe containers e volumes antigos
docker-compose down -v
docker system prune
```




## Contribuindo

Obrigado por considerar contribuir para este projeto! Para enviar suas alterações, siga os passos abaixo:

1. **Fork o repositório**
   - Vá até a página do repositório e clique no botão "Fork" no canto superior direito para criar uma cópia do repositório na sua conta do GitHub.

2. **Clone o repositório para o seu computador**
   - No seu terminal, clone a versão forkada do repositório:
     ```bash
     git clone https://github.com/seu-usuario/audio-wrapper-api.git
     cd audio-wrapper-api
     ```

3. **Crie uma branch para sua feature**
   - Crie uma nova branch para a funcionalidade que você está trabalhando:
     ```bash
     git checkout -b feature/nova-funcionalidade
     ```

4. **Faça as alterações e commite**
   - Faça as alterações no código e adicione um commit com uma mensagem descritiva:
     ```bash
     git add .
     git commit -am "Adiciona nova funcionalidade"
     ```

5. **Envie as alterações para o seu repositório forkado**
   - Use o comando `git push` para enviar suas alterações para o repositório forkado:
     ```bash
     git push origin feature/nova-funcionalidade
     ```

6. **Crie um Pull Request**
   - Vá para a página do seu repositório no GitHub e clique no botão **"Compare & pull request"**.
   - Descreva suas alterações e crie o Pull Request para que possamos revisar e possivelmente mesclar suas contribuições no repositório principal.



## Dependências Principais
```
fastapi==0.109.2
uvicorn==0.27.1
python-multipart==0.0.9
httpx==0.26.0
jinja2==3.1.3
python-dotenv==1.0.1
pydantic-settings==2.1.0
aiofiles==23.2.1
```

---


## Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Suporte
- Abra uma issue para reportar bugs
- Discussões e sugestões são bem-vindas

---

