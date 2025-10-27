# Dockerfile

# 1. Imagem base
FROM python:3.10-slim

# 2. Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Instalar dependências do sistema
#    Necessárias para compilar psycopg2 e para o Pillow (libjpeg)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     libpq-dev \
     libjpeg-dev \
     zlib1g-dev \
  && rm -rf /var/lib/apt/lists/*

# 4. Definir diretório de trabalho
WORKDIR /app

# 5. Instalar dependências do Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# 6. Copiar o código do projeto
COPY . .

# 7. Expor a porta (usada pelo runserver/gunicorn)
EXPOSE 8000