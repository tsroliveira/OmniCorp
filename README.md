# OmniCorp - Sistema Corporativo

Sistema corporativo modular com autenticação via Active Directory, desenvolvido com Python (FastAPI) no backend e React no frontend. A aplicação é containerizada usando Docker, permitindo fácil implantação e escalabilidade.

## Tecnologias Utilizadas

### Backend
- Python 3.9+
- FastAPI (framework web)
- SQLAlchemy (ORM)
- Python-LDAP (autenticação com Active Directory)
- JWT (tokens de autenticação)
- MySQL (banco de dados)

### Frontend
- React 18
- Material-UI (componentes de interface)
- Redux (gerenciamento de estado)
- React Router (roteamento)
- Axios (requisições HTTP)

### Infraestrutura
- Docker & Docker Compose (para MySQL e PHPMyAdmin)

## Características

- Arquitetura MVC e modular
- Autenticação via Active Directory
- Gestão de perfis e permissões
- Usuário administrador local
- Interface responsiva e moderna
- Preparado para expansão com microserviços

## Instalação e Configuração

### Requisitos

- Python 3.9+
- Node.js 16+
- Docker e Docker Compose
- Acesso ao servidor Active Directory

### Configuração Inicial

1. Clone o repositório:
   ```
   git clone https://github.com/sua-organizacao/omnicorp.git
   cd omnicorp
   ```

2. Configure o arquivo `.env` com suas informações:
   ```
   # Configurações do Banco de Dados
   DATABASE_URL=mysql+pymysql://omnicorp_user:omnicorp_password@localhost:3306/omnicorp

   # Configurações da Aplicação
   SECRET_KEY=sua_chave_secreta_muito_segura
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=True

   # Configurações do Active Directory
   AD_SERVER=10.98.132.248
   AD_DOMAIN=SSODC.Local
   AD_BASE_DN=OU=Usuarios,DC=SSODC,DC=Local
   AD_USERNAME=ldap_service_account
   AD_PASSWORD=ldap_service_password
   ```

3. Inicie o banco de dados com Docker:
   ```
   docker-compose up -d
   ```

4. Instale as dependências do backend:
   ```
   pip install -r requirements.txt
   ```

5. Instale as dependências do frontend:
   ```
   cd app/frontend
   npm install
   ```

### Execução

1. Inicie o backend:
   ```
   python run.py
   ```

2. Inicie o frontend (em outro terminal):
   ```
   cd app/frontend
   npm start
   ```

3. Acesse a aplicação em: http://localhost:3000

## Usuário Padrão

- Username: administrator
- Senha: admin@123

## Estrutura do Projeto

```
/
├── app/
│   ├── backend/
│   │   ├── config/        # Configurações
│   │   ├── controllers/   # Controladores
│   │   ├── models/        # Modelos
│   │   ├── schemas/       # Schemas de validação
│   │   ├── services/      # Serviços
│   │   ├── utils/         # Utilitários
│   │   └── main.py        # Aplicação principal
│   │
│   └── frontend/          # Aplicação React
│
├── db/                    # Dados do MySQL
├── docker-compose.yaml    # Configuração do Docker
├── requirements.txt       # Dependências Python
└── run.py                 # Script de inicialização
```

## Configurações e Arquivos Importantes
- **docker-compose.yaml**: Define os serviços Docker, incluindo MySQL, PHPMyAdmin, backend e frontend. Configura volumes, redes e variáveis de ambiente.
- **docker-start.sh**: Script para iniciar todos os serviços Docker, garantindo que o MySQL esteja pronto antes de iniciar outros serviços.
- **init.sql**: Script SQL para inicializar o banco de dados MySQL com usuários e permissões.

## Principais Componentes e Funcionalidades
### Backend
- **settings.py**: Configurações globais, incluindo variáveis de ambiente e configurações de autenticação.
- **database.py**: Configuração do banco de dados usando SQLAlchemy.
- **auth_controller.py**: Controlador de autenticação, gerencia login e verificação de tokens JWT.
- **user_controller.py**: Controlador de usuários, gerencia operações CRUD para usuários.
- **user.py (Model)**: Define o modelo de dados para usuários, incluindo campos e relacionamentos.
- **auth_service.py**: Serviço de autenticação, inclui funções para autenticar usuários e gerar tokens JWT.
- **ldap_service.py**: Serviço para autenticação LDAP, usado para autenticar usuários contra um servidor LDAP.

### Frontend
- **authSlice.js**: Gerencia o estado de autenticação no Redux, incluindo ações para login e verificação de usuários.
- **userSlice.js**: Gerencia o estado dos usuários no Redux, incluindo ações para buscar e criar usuários.
- **Login.js**: Página de login, permite que os usuários façam login na aplicação.

## Extensibilidade
O sistema foi projetado para ser facilmente extensível com novos módulos/microserviços:

1. Crie novos controladores no backend
2. Adicione rotas na aplicação principal
3. Crie componentes React para as novas funcionalidades
4. Registre os novos módulos no banco de dados com as permissões apropriadas

## Instruções de Uso
1. **Configuração Inicial**:
   - Certifique-se de que o Docker e o Docker Compose estão instalados.
   - Configure as variáveis de ambiente necessárias no `docker-compose.yaml`.

2. **Iniciar a Aplicação**:
   - Execute o script `docker-start.sh` para iniciar todos os serviços.
   - Acesse o frontend em `http://localhost:3000` e o PHPMyAdmin em `http://localhost:8080`.

3. **Autenticação e Uso**:
   - Use o endpoint de login para obter um token JWT.
   - Use o token para acessar endpoints protegidos no backend.

## Logs de Erro Recentes
Os logs recentes indicam um problema com a decodificação do token JWT, onde o token está sendo passado como `None`. Isso pode ser devido a um token não fornecido ou inválido. Certifique-se de que o token JWT está sendo passado corretamente no cabeçalho de autorização das requisições.

## Resumo dos Prompts de Criação
O projeto foi criado com o objetivo de desenvolver um sistema corporativo modular com autenticação via Active Directory. As principais características incluem:
- IP do Active Directory: 10.98.132.248
- Domínio: SSODC.Local
- Base DN: OU=Usuarios,DC=SSODC,DC=Local
- Usuário de Serviço LDAP: ldap_service_account
- Senha do Serviço LDAP: ldap_service_password
- Autenticação JWT para segurança
- Estrutura modular para fácil expansão e manutenção

Este README combina informações detalhadas sobre a configuração, execução e estrutura do projeto, além de fornecer um resumo dos objetivos e características principais.

## Arquitetura de Autenticação e Autorização

### Abordagem de Autenticação
O sistema utiliza uma combinação de JWT e Redis para autenticação e autorização, oferecendo um equilíbrio ideal entre desempenho, segurança e simplicidade.

#### Por que JWT + Redis?
1. **JWT (JSON Web Tokens)**
   - Autenticação sem estado (stateless)
   - Armazena informações básicas do usuário
   - Tempo de expiração configurável
   - Reduz a necessidade de consultas ao banco de dados
   - Ideal para APIs REST

2. **Redis**
   - Armazenamento em memória de alta performance
   - Cache de dados de sessão detalhados
   - Tempo de expiração configurável
   - Reduz a carga no servidor LDAP/AD
   - Permite atualização periódica de dados

3. **Benefícios da Combinação**
   - Melhor desempenho: Cache de dados de autorização
   - Maior segurança: Tokens JWT assinados
   - Flexibilidade: Fácil atualização de permissões
   - Escalabilidade: Reduz carga no AD/LDAP
   - Simplicidade: Implementação direta e manutenção facilitada

### Estrutura de Perfis
O sistema implementa três perfis principais:
1. **Administrador**
   - Acesso total ao sistema
   - Gerenciamento de usuários e perfis
   - Configurações do sistema

2. **Analista**
   - Acesso a funcionalidades específicas
   - Gerenciamento de dados
   - Relatórios e análises

3. **Usuário**
   - Acesso básico ao sistema
   - Funcionalidades restritas
   - Visualização limitada

### Gerenciamento de Permissões
- CRUD completo de perfis
- Associação de usuários a múltiplos perfis
- Controle granular de permissões
- Interface administrativa para gestão

## Configurações e Arquivos Importantes
- **docker-compose.yaml**: Define os serviços Docker, incluindo MySQL, PHPMyAdmin, backend e frontend. Configura volumes, redes e variáveis de ambiente.
- **docker-start.sh**: Script para iniciar todos os serviços Docker, garantindo que o MySQL esteja pronto antes de iniciar outros serviços.
- **init.sql**: Script SQL para inicializar o banco de dados MySQL com usuários e permissões.

## Principais Componentes e Funcionalidades
### Backend
- **settings.py**: Configurações globais, incluindo variáveis de ambiente e configurações de autenticação.
- **database.py**: Configuração do banco de dados usando SQLAlchemy.
- **auth_controller.py**: Controlador de autenticação, gerencia login e verificação de tokens JWT.
- **user_controller.py**: Controlador de usuários, gerencia operações CRUD para usuários.
- **user.py (Model)**: Define o modelo de dados para usuários, incluindo campos e relacionamentos.
- **auth_service.py**: Serviço de autenticação, inclui funções para autenticar usuários e gerar tokens JWT.
- **ldap_service.py**: Serviço para autenticação LDAP, usado para autenticar usuários contra um servidor LDAP.

### Frontend
- **authSlice.js**: Gerencia o estado de autenticação no Redux, incluindo ações para login e verificação de usuários.
- **userSlice.js**: Gerencia o estado dos usuários no Redux, incluindo ações para buscar e criar usuários.
- **Login.js**: Página de login, permite que os usuários façam login na aplicação.

## Extensibilidade
O sistema foi projetado para ser facilmente extensível com novos módulos/microserviços:

1. Crie novos controladores no backend
2. Adicione rotas na aplicação principal
3. Crie componentes React para as novas funcionalidades
4. Registre os novos módulos no banco de dados com as permissões apropriadas

## Instruções de Uso
1. **Configuração Inicial**:
   - Certifique-se de que o Docker e o Docker Compose estão instalados.
   - Configure as variáveis de ambiente necessárias no `docker-compose.yaml`.

2. **Iniciar a Aplicação**:
   - Execute o script `docker-start.sh` para iniciar todos os serviços.
   - Acesse o frontend em `http://localhost:3000` e o PHPMyAdmin em `http://localhost:8080`.

3. **Autenticação e Uso**:
   - Use o endpoint de login para obter um token JWT.
   - Use o token para acessar endpoints protegidos no backend.

## Logs de Erro Recentes
Os logs recentes indicam um problema com a decodificação do token JWT, onde o token está sendo passado como `None`. Isso pode ser devido a um token não fornecido ou inválido. Certifique-se de que o token JWT está sendo passado corretamente no cabeçalho de autorização das requisições.

## Resumo dos Prompts de Criação
O projeto foi criado com o objetivo de desenvolver um sistema corporativo modular com autenticação via Active Directory. As principais características incluem:
- IP do Active Directory: 10.98.132.248
- Domínio: SSODC.Local
- Base DN: OU=Usuarios,DC=SSODC,DC=Local
- Usuário de Serviço LDAP: ldap_service_account
- Senha do Serviço LDAP: ldap_service_password
- Autenticação JWT para segurança
- Estrutura modular para fácil expansão e manutenção

Este README combina informações detalhadas sobre a configuração, execução e estrutura do projeto, além de fornecer um resumo dos objetivos e características principais. 



# Para usar no Macos
docker-compose -f docker-compose-macos.yaml up -d
docker-compose -f docker-compose-macos.yaml down
docker-compose -f docker-compose-macos.yaml ps