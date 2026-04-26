# Sistema de Logger do Jujoo Sorveteria
import logging
import sys
from pathlib import Path
from datetime import datetime
from src.core.config import LOG_FILE, LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str = "jujoo") -> logging.Logger:
    """Configura e retorna um logger"""
    logger = logging.getLogger(name)
    
    # Evita configuração duplicada
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Formatador
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Logger global
logger = setup_logger()


def log_operacao(modulo: str, operacao: str, detalhes: str = ""):
    """Registra uma operação no log"""
    logger.info(f"[{modulo}] {operacao}: {detalhes}")


def log_erro(modulo: str, erro: Exception, contexto: str = ""):
    """Registra um erro no log"""
    logger.error(f"[{modulo}] Erro em {contexto}: {type(erro).__name__} - {str(erro)}")


def log_warning(modulo: str, mensagem: str):
    """Registra um warning no log"""
    logger.warning(f"[{modulo}] {mensagem}")


def log_debug(modulo: str, mensagem: str):
    """Registra debug no log"""
    logger.debug(f"[{modulo}] {mensagem}")