from sqlalchemy.orm import Session
from app.backend.models.user import User

def get_user_by_username(db: Session, username: str) -> User:
    """
    Busca um usuário pelo nome de usuário.
    
    Args:
        db: Sessão do banco de dados
        username: Nome de usuário a ser buscado
        
    Returns:
        User: Objeto do usuário encontrado ou None se não existir
    """
    return db.query(User).filter(User.username == username).first() 