FROM python:3.9-slim

# Instalação de dependências do sistema para o python-ldap
RUN apt-get update && apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    ldap-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto da aplicação
COPY . .

# Expor a porta do backend
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "run.py"] 