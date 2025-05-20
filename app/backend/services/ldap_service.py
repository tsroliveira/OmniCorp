import ldap
import logging
import traceback
import re
from typing import Optional, Dict, Any, List
from app.backend.config.settings import settings

logger = logging.getLogger(__name__)

class LDAPService:
    def __init__(self):
        logger.debug("Inicializando serviço LDAP")
        self.server = settings.ldap.server
        self.domain = settings.ldap.domain
        self.base_dn = settings.ldap.base_dn
        self.username = settings.ldap.username
        self.password = settings.ldap.password
        logger.debug(f"Configuração LDAP: server={self.server}, domain={self.domain}")

    def log_exception(self, e: Exception, context: str = ""):
        """Registra exceção com traceback completo"""
        logger.error(f"ERRO LDAP em {context}: {str(e)}")
        logger.error(f"TRACEBACK LDAP: {''.join(traceback.format_exception(None, e, e.__traceback__))}")

    def extract_cn_name(self, dn: str) -> str:
        """Extrai o nome do CN de um DN"""
        match = re.search(r"CN=([^,]+)", dn)
        if match:
            return match.group(1)
        return dn

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica um usuário no AD/LDAP e retorna seus dados.
        Busca o usuário por email nos repositórios e subrepositórios do AD.
        
        Args:
            username: Nome de usuário ou email
            password: Senha do usuário
            
        Returns:
            Dict: Dicionário com dados do usuário ou None se falhar
        """
        logger.debug(f"Tentando autenticar usuário {username} via LDAP")
        try:
            logger.debug(f"Inicializando conexão LDAP para servidor {self.server}")
            conn = ldap.initialize(f"ldap://{self.server}")
            conn.protocol_version = ldap.VERSION3
            conn.set_option(ldap.OPT_REFERRALS, 0)
            
            # Extrai o nome de usuário do email
            original_username = username
            username = username.split('@')[0]
            logger.debug(f"Username extraído: {username} (original: {original_username})")
            
            # Conecta com as credenciais do usuário
            bind_dn = f"{username}@{self.domain}"
            logger.debug(f"Tentando bind com DN: {bind_dn}")
            conn.simple_bind_s(bind_dn, password)
            logger.debug("Bind LDAP bem sucedido")
            
            # Busca o usuário no AD, incluindo subrepositórios
            search_filter = f"(&(objectClass=user)(mail={original_username}))"
            logger.debug(f"Executando busca LDAP: base_dn={self.base_dn}, filtro={search_filter}")
            result = conn.search_s(
                self.base_dn,
                ldap.SCOPE_SUBTREE,
                search_filter,
                ["sAMAccountName", "mail", "displayName", "memberOf"]
            )
            
            logger.debug(f"Resultado da busca LDAP: {result}")
            
            if not result:
                return None
                
            # Processando resultado para extrair dados do usuário
            user_dn, user_attrs = result[0]
            
            # Extraindo informações
            display_name = user_attrs.get('displayName', [b''])[0].decode('utf-8') if 'displayName' in user_attrs else username
            email = user_attrs.get('mail', [b''])[0].decode('utf-8') if 'mail' in user_attrs else original_username
            sam_account = user_attrs.get('sAMAccountName', [b''])[0].decode('utf-8') if 'sAMAccountName' in user_attrs else username
            
            # Processando grupos
            member_of = []
            if 'memberOf' in user_attrs:
                for group_dn in user_attrs['memberOf']:
                    group_name = self.extract_cn_name(group_dn.decode('utf-8'))
                    member_of.append(group_name)
            
            logger.debug(f"Grupos do usuário: {member_of}")
            
            user_data = {
                "username": original_username,
                "sam_account": sam_account,
                "display_name": display_name,
                "email": email,
                "groups": member_of if member_of else ["Usuários"]
            }
            
            logger.debug(f"Dados do usuário LDAP: {user_data}")
            return user_data
            
        except ldap.INVALID_CREDENTIALS:
            logger.warning(f"Credenciais inválidas para o usuário {username}")
            return None
        except Exception as e:
            self.log_exception(e, f"autenticação LDAP para {username}")
            return None
        finally:
            if 'conn' in locals():
                logger.debug("Desconectando da sessão LDAP")
                conn.unbind_s()

# Criando e exportando a instância do serviço LDAP
ldap_service = LDAPService() 