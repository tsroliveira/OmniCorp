import redis
import json
from datetime import timedelta
from app.backend.config.settings import settings

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
        self.expiration_time = timedelta(hours=24)

    def get_user_permissions(self, user_id: int) -> dict:
        """Obtém as permissões do usuário do cache."""
        key = f"user:{user_id}:permissions"
        cached_data = self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def set_user_permissions(self, user_id: int, permissions: dict):
        """Armazena as permissões do usuário no cache."""
        key = f"user:{user_id}:permissions"
        self.redis_client.setex(
            key,
            self.expiration_time,
            json.dumps(permissions)
        )

    def delete_user_permissions(self, user_id: int):
        """Remove as permissões do usuário do cache."""
        key = f"user:{user_id}:permissions"
        self.redis_client.delete(key)

    def get_profile_permissions(self, profile_id: int) -> dict:
        """Obtém as permissões do perfil do cache."""
        key = f"profile:{profile_id}:permissions"
        cached_data = self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def set_profile_permissions(self, profile_id: int, permissions: dict):
        """Armazena as permissões do perfil no cache."""
        key = f"profile:{profile_id}:permissions"
        self.redis_client.setex(
            key,
            self.expiration_time,
            json.dumps(permissions)
        )

    def delete_profile_permissions(self, profile_id: int):
        """Remove as permissões do perfil do cache."""
        key = f"profile:{profile_id}:permissions"
        self.redis_client.delete(key)

    def clear_all_permissions(self):
        """Remove todas as permissões do cache."""
        for key in self.redis_client.keys("*:permissions"):
            self.redis_client.delete(key)

# Instância global do serviço Redis
redis_service = RedisService() 