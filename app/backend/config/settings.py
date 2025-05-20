from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSettings(BaseModel):
    url: str = os.getenv("DATABASE_URL", "mysql+pymysql://omnicorp_user:omnicorp_password@omnicorp_mysql:3306/omnicorp")

class AuthSettings(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY", "sua_chave_secreta_muito_segura")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class LdapSettings(BaseModel):
    server: str = os.getenv("AD_SERVER", "10.98.132.248")
    domain: str = os.getenv("AD_DOMAIN", "SSODC.Local")
    base_dn: str = os.getenv("AD_BASE_DN", "OU=Usuarios,DC=SSODC,DC=Local")
    username: str = os.getenv("AD_USERNAME", "ldap_service_account")
    password: str = os.getenv("AD_PASSWORD", "ldap_service_password")

class Settings(BaseSettings):
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    ldap: LdapSettings = LdapSettings()

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permite variáveis extras no .env

settings = Settings() 