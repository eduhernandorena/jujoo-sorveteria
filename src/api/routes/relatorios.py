# Rotas de Relatórios
from fastapi import APIRouter
from typing import Optional
from src.services.relatorio_service import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/vendas")
def relatorio_vendas(data_inicio: Optional[str] = None, data_fim: Optional[str] = None):
    """Relatório de vendas"""
    return relatorio_service.relatorio_vendas(data_inicio, data_fim)


@router.get("/compras")
def relatorio_compras(data_inicio: Optional[str] = None, data_fim: Optional[str] = None):
    """Relatório de compras"""
    return relatorio_service.relatorio_compras(data_inicio, data_fim)


@router.get("/lucratividade")
def relatorio_lucratividade(data_inicio: Optional[str] = None, data_fim: Optional[str] = None):
    """Relatório de lucratividade"""
    return relatorio_service.relatorio_lucratividade(data_inicio, data_fim)


@router.get("/estoque")
def relatorio_estoque():
    """Relatório de estoque"""
    return relatorio_service.relatorio_estoque()


@router.get("/caixa")
def relatorio_caixa(data: Optional[str] = None, mes: Optional[str] = None):
    """Relatório de caixa"""
    return relatorio_service.relatorio_caixa(data, mes)


@router.get("/producao")
def relatorio_producao(data: Optional[str] = None):
    """Relatório de produção"""
    return relatorio_service.relatorio_producao(data)


@router.get("/dashboard")
def dashboard():
    """Dashboard com dados gerais"""
    return relatorio_service.dashboard()