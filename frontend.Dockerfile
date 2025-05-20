FROM node:16-alpine

WORKDIR /app

# Copiar package.json e package-lock.json
COPY app/frontend/package.json app/frontend/package-lock.json* ./

# Instalar dependências
RUN npm install

# Copiar arquivos do frontend
COPY app/frontend/ ./

# Expor a porta do frontend
EXPOSE 3000

# Comando para iniciar a aplicação em modo de desenvolvimento
CMD ["npm", "start"] 