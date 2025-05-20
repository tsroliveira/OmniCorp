from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.backend.config.database import get_db, engine, Base
from app.backend.services.auth_service import create_initial_data
from app.backend.controllers import auth_controller, user_controller, module_controller
from app.backend.controllers.profile_controller import router as profile_router
from app.backend.controllers.permission_controller import router as permission_router

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OmniCorp",
    description="Sistema corporativo OmniCorp",
    version="1.0.0",
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adiciona rotas
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(module_controller.router)
app.include_router(profile_router, prefix="/api", tags=["profiles"])
app.include_router(permission_router, prefix="/api", tags=["permissions"])


@app.on_event("startup")
async def startup_event():
    # Inicializa dados iniciais
    db = next(get_db())
    create_initial_data(db)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"} 