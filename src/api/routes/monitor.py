# Rotas de Monitoramento
from fastapi import APIRouter
from src.utils.monitor import get_status_recursos, get_info_completa

router = APIRouter(prefix="/monitor", tags=["Monitor"])


@router.get("/status")
def status_recursos():
    """Status simplificado dos recursos"""
    return get_status_recursos()


@router.get("/info")
def info_recursos():
    """Informações completas dos recursos"""
    return get_info_completa()