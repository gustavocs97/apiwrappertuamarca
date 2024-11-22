# Dockerfile
# Usando uma imagem base Python 3.11 slim
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema (adicionando ffmpeg para a manipulação de áudio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*  # Limpar cache de pacotes após instalação para reduzir a imagem

# Copiar o arquivo de requisitos e instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretórios para áudio e imagens temporárias e garantir permissões adequadas
RUN mkdir -p /app/temp_audio && \
    chmod 777 /app/temp_audio && \
    mkdir -p /app/temp_images && \
    chmod 777 /app/temp_images

# INSERIR NOVAS CONFIGURAÇÕES AQUI
# Para adicionar suporte a novos wrappers, criar diretórios temporários, se necessário:
# 1. Exemplo para criar um diretório para novos wrappers:
#    RUN mkdir -p /app/temp_novo_wrapper_exempo && \
#        chmod 777 /app/temp_novo_wrapper_exemplo

# 2. Instalar dependências do sistema específicas do novo wrapper:
#    RUN apt-get update && apt-get install -y --no-install-recommends \
#        <nova_dependencia> && \
#        rm -rf /var/lib/apt/lists/*  # Limpar cache de pacotes

# 3. Certifique-se de ajustar permissões adequadas para novos recursos ou diretórios.

# Copiar todos os arquivos do código fonte para dentro do container
COPY . .

# Expor a porta 5051 para acesso à aplicação
EXPOSE 5051

# Comando para rodar a aplicação quando o container for iniciado
CMD ["python", "src/main.py"]
