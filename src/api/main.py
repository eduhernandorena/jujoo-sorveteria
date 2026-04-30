# API Principal do Jujoo Sorveteria
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from src.api.routes import produtos, estoque, caixa, vendas, compras, producao, relatorios, monitor
from src.core.config import API_TITLE, API_VERSION, CORS_ORIGINS
from src.utils.logger import logger

# Criar aplicação FastAPI
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="Sistema de gerenciamento para sorveterias"
)

# Configurar CORS
if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    logger.info("CORS não configurado (CORS_ORIGINS vazio); origens explícitas necessárias para habilitar CORS.")

# Rota para o frontend
@app.get("/frontend")
def get_frontend():
    """Serve o frontend HTML"""
    frontend_path = Path(__file__).parent.parent.parent / "frontend.html"
    if not frontend_path.exists():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Frontend não disponível")
    return FileResponse(frontend_path)

# Incluir routers
app.include_router(produtos.router, prefix="/api")
app.include_router(estoque.router, prefix="/api")
app.include_router(caixa.router, prefix="/api")
app.include_router(vendas.router, prefix="/api")
app.include_router(compras.router, prefix="/api")
app.include_router(producao.router, prefix="/api")
app.include_router(relatorios.router, prefix="/api")
app.include_router(monitor.router, prefix="/api")


@app.get("/")
def root():
    """Rota raiz"""
    return {
        "nome": API_TITLE,
        "versao": API_VERSION,
        "status": "online",
        "documentacao": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check"""
    return {"status": "healthy"}


# Evento de startup
@app.on_event("startup")
async def startup_event():
    logger.info(f"Iniciando {API_TITLE} v{API_VERSION}")


# Evento de shutdown
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Encerrando API")


if __name__ == "__main__":
    import uvicorn
    from src.core.config import API_HOST, API_PORT
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)
