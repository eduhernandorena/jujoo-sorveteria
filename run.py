# Script de inicialização do Jujoo Sorveteria
import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.main import app
from src.core.config import API_HOST, API_PORT
from src.utils.logger import logger


def main():
    """Função principal"""
    logger.info("=" * 50)
    logger.info("Iniciando Jujoo Sorveteria")
    logger.info("=" * 50)
    
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )


if __name__ == "__main__":
    main()