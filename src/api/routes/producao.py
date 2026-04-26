# Rotas de Produção
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from src.models.producao import ProducaoCreate, ProducaoResponse
from src.services.producao_service import producao_service

router = APIRouter(prefix="/producao", tags=["Produção"])


@router.get("/", response_model=List[ProducaoResponse])
def listar_producoes(data: Optional[str] = None):
    """Lista produções"""
    return producao_service.listar(data)


@router.get("/do-dia", response_model=List[ProducaoResponse])
def listar_producoes_do_dia():
    """Lista produções do dia"""
    return producao_service.get_producoes_do_dia()


@router.get("/{producao_id}", response_model=ProducaoResponse)
def buscar_producao(producao_id: str):
    """Busca produção por ID"""
    producao = producao_service.buscar_por_id(producao_id)
    if not producao:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    return producao


@router.post("/")
def criar_producao(dados: ProducaoCreate):
    """Cria nova produção"""
    resultado = producao_service.criar(dados)
    if "erro" in resultado:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return resultado