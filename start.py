import os
import subprocess
import sys
import time
from threading import Thread

def run_backend():
    """Executa o backend"""
    print("Iniciando o backend...")
    os.system('python run.py')

def run_frontend():
    """Executa o frontend"""
    print("Iniciando o frontend...")
    os.chdir('app/frontend')
    if sys.platform == 'win32':
        os.system('npm start')
    else:
        os.system('npm start')

def run_docker():
    """Executa o docker-compose"""
    print("Iniciando o banco de dados com Docker...")
    os.system('docker-compose up -d')

if __name__ == "__main__":
    # Inicializa o Docker
    run_docker()
    print("Aguardando o banco de dados iniciar...")
    time.sleep(5)  # Aguarda o banco iniciar
    
    # Inicia o backend e frontend em threads separadas
    backend_thread = Thread(target=run_backend)
    frontend_thread = Thread(target=run_frontend)
    
    backend_thread.daemon = True
    frontend_thread.daemon = True
    
    backend_thread.start()
    time.sleep(3)  # Aguarda o backend iniciar antes do frontend
    frontend_thread.start()
    
    try:
        # Mantém o script principal em execução
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando o ambiente...")
        os.system('docker-compose down')
        print("Ambiente encerrado.") 