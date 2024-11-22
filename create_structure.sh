#!/bin/bash

# ----------------------------
# Criação de diretórios principais do projeto
# ----------------------------
mkdir -p src/routes          # Diretório para as rotas da aplicação
mkdir -p src/services        # Diretório para os serviços da aplicação
mkdir -p src/static/css      # Diretório para os arquivos CSS estáticos
mkdir -p src/static/js       # Diretório para os arquivos JavaScript estáticos
mkdir -p src/templates       # Diretório para os templates HTML
mkdir -p tests               # Diretório para os testes

# ----------------------------
# Criação de arquivos principais
# ----------------------------
touch Dockerfile             # Arquivo para a configuração do Docker
touch docker-compose.yml     # Arquivo de configuração do Docker Compose
touch requirements.txt       # Arquivo com as dependências do projeto
touch .env.example           # Arquivo de exemplo para variáveis de ambiente
touch .gitignore             # Arquivo de configuração do Git para ignorar arquivos/diretórios
touch README.md              # Arquivo de README para documentação do projeto

# ----------------------------
# Criação de arquivos do código-fonte
# ----------------------------
touch src/__init__.py        # Arquivo para tornar o diretório src um pacote Python
touch src/main.py            # Arquivo principal da aplicação (pode ser o ponto de entrada)
touch src/config.py          # Arquivo para as configurações do projeto

# ----------------------------
# Criação de arquivos para as rotas (endpoints da API)
# ----------------------------
touch src/routes/__init__.py        # Arquivo para tornar o diretório routes um pacote Python
touch src/routes/audio.py           # Rota para a API de áudio
touch src/routes/image.py           # Nova rota para a API de imagem
touch src/routes/novo_wrapper_exemplo.py  # Nova rota para um wrapper de exemplo
touch src/routes/views.py           # Rota para visualização de dados, se necessário

# ----------------------------
# Criação de arquivos para os serviços (lógica de negócios)
# ----------------------------
touch src/services/__init__.py      # Arquivo para tornar o diretório services um pacote Python
touch src/services/audio_service.py # Serviço para lógica da API de áudio
touch src/services/image_service.py # Novo serviço para lógica da API de imagem
touch src/services/novo_service_exemplo.py  # Novo serviço de exemplo
touch src/services/storage_service.py    # Serviço para armazenamento de dados

# ----------------------------
# Criação de arquivos estáticos (CSS e JS)
# ----------------------------
touch src/static/css/style.css     # Arquivo CSS principal para o estilo da aplicação
touch src/static/js/main.js        # Arquivo JavaScript principal para funcionalidades da aplicação

# ----------------------------
# Criação de templates HTML
# ----------------------------
touch src/templates/base.html      # Template base para o layout da aplicação
touch src/templates/index.html     # Template para a página inicial

# ----------------------------
# Criação de arquivos de testes
# ----------------------------
touch tests/__init__.py            # Arquivo para tornar o diretório tests um pacote Python
touch tests/test_audio_service.py  # Testes para o serviço de áudio

# ----------------------------
# Mensagem de confirmação
# ----------------------------
echo "Estrutura do projeto criada com sucesso!"
