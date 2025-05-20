#!/bin/bash

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para verificar se um container está rodando
container_running() {
    docker ps -q -f name="$1" | grep -q .
}

# Função para verificar se um container está saudável
container_healthy() {
    docker inspect -f '{{.State.Health.Status}}' "$1" 2>/dev/null | grep -q "healthy"
}

# Parar todos os containers
echo "Parando todos os containers..."
docker-compose down

# Limpar volumes antigos
echo "Limpando volumes antigos..."
docker volume prune -f

# Criar diretório do banco de dados se não existir
echo "Verificando diretório do banco de dados..."
mkdir -p ./db
chmod 777 ./db

# Iniciar o MySQL
echo "Iniciando MySQL..."
docker-compose up -d db

# Aguardar o MySQL estar pronto
echo "Aguardando MySQL estar pronto..."
while ! docker exec omnicorp_mysql mysqladmin ping -h localhost -u root -proot_password --silent; do
    echo "MySQL ainda não está pronto. Aguardando..."
    sleep 5
done

echo "MySQL está pronto!"

# Iniciar PHPMyAdmin
echo "Iniciando PHPMyAdmin..."
docker-compose up -d phpmyadmin

# Aguardar um pouco para o PHPMyAdmin inicializar
sleep 5

# Iniciar o backend
echo "Iniciando backend..."
docker-compose up -d backend

# Aguardar um pouco para o backend inicializar
sleep 10

# Iniciar o frontend
echo "Iniciando frontend..."
docker-compose up -d frontend

# Iniciar o Redis
echo "Iniciando Redis..."
docker-compose up -d redis

echo "Todos os serviços foram iniciados!"
echo "Acesse:"
echo "- Frontend: http://localhost:3000"
echo "- Backend: http://localhost:8000"
echo "- PHPMyAdmin: http://localhost:8080"
echo "- Redis: localhost:6379"

echo "Credenciais:"
echo "- Usuário: administrator"
echo "- Senha: administrator"

# Mostrar logs do backend
echo "Mostrando logs do backend..."
docker-compose logs -f backend

docker ps

docker exec -it omnicorp_mysql mysql -uomnicorp_user -pomnicorp_password omnicorp

docker logs omnicorp_mysql 