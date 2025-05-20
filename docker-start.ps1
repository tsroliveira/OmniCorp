# PowerShell script para inicialização dos serviços

# Parar todos os containers
Write-Host "Parando todos os containers..."
docker-compose down

# Limpar volumes antigos
Write-Host "Limpando volumes antigos..."
docker volume prune -f

# Criar diretório do banco de dados se não existir
Write-Host "Verificando diretório do banco de dados..."
New-Item -ItemType Directory -Force -Path ./db
icacls ./db /grant Everyone:F

# Iniciar o MySQL
Write-Host "Iniciando MySQL..."
docker-compose up -d db

# Aguardar o MySQL estar pronto
Write-Host "Aguardando MySQL estar pronto..."
while (-not (docker exec omnicorp_mysql mysqladmin ping -h localhost -u root -proot_password --silent)) {
    Write-Host "MySQL ainda não está pronto. Aguardando..."
    Start-Sleep -Seconds 5
}

Write-Host "MySQL está pronto!"

# Iniciar PHPMyAdmin
Write-Host "Iniciando PHPMyAdmin..."
docker-compose up -d phpmyadmin

# Aguardar um pouco para o PHPMyAdmin inicializar
Start-Sleep -Seconds 5

# Iniciar o backend
Write-Host "Iniciando backend..."
docker-compose up -d backend

# Aguardar um pouco para o backend inicializar
Start-Sleep -Seconds 10

# Iniciar o frontend
Write-Host "Iniciando frontend..."
docker-compose up -d frontend

# Iniciar o Redis
Write-Host "Iniciando Redis..."
docker-compose up -d redis

Write-Host "Todos os serviços foram iniciados!"
Write-Host "Acesse:"
Write-Host "- Frontend: http://localhost:3000"
Write-Host "- Backend: http://localhost:8000"
Write-Host "- PHPMyAdmin: http://localhost:8080"
Write-Host "- Redis: localhost:6379"

Write-Host "Credenciais:"
Write-Host "- Usuário: administrator"
Write-Host "- Senha: administrator"

# Mostrar logs do backend
Write-Host "Mostrando logs do backend..."
docker-compose logs -f backend

# Monitoramento de logs
Write-Host ""
Write-Host "Para verificar o status dos contêineres, execute: docker ps" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver logs de um contêiner específico, execute: docker logs -f [nome_do_container]" -ForegroundColor Cyan
Write-Host "Exemplos:"
Write-Host "docker logs -f omnicorp_backend"
Write-Host "docker logs -f omnicorp_frontend"
Write-Host "docker logs -f omnicorp_mysql" 