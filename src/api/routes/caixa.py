# Rotas de Caixa
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from src.models.caixa import MovimentoCaixaCreate, MovimentoCaixaResponse, FechamentoDiario, FechamentoMensal
from src.services.caixa_service import caixa_service

router = APIRouter(prefix="/caixa", tags=["Caixa"])


@router.get("/movimentos", response_model=List[MovimentoCaixaResponse])
def listar_movimentos(data: Optional[str] = None, tipo: Optional[str] = None):
    """Lista movimentos de caixa"""
    return caixa_service.listar_movimentos(data, tipo)


@router.get("/saldo")
def get_saldo():
    """Retorna saldo atual do caixa"""
    return {
        "saldo_atual": caixa_service.get_saldo_atual(),
        "saldo_do_dia": caixa_service.get_saldo_do_dia()
    }


@router.post("/movimento", response_model=MovimentoCaixaResponse)
def criar_movimento(dados: MovimentoCaixaCreate):
    """Cria novo movimento de caixa"""
    return caixa_service.criar_movimento(dados)


@router.post("/fechamento-diario")
def fazer_fechamento_diario(data: Optional[str] = None):
    """Faz fechamento diário"""
    return caixa_service.fazer_fechamento_diario(data)


@router.post("/fechamento-mensal")
def fazer_fechamento_mensal(mes: Optional[str] = None):
    """Faz fechamento mensal"""
    return caixa_service.fazer_fechamento_mensal(mes)