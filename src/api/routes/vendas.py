# Rotas de Vendas
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from src.models.venda import VendaCreate, VendaResponse
from src.services.venda_service import venda_service

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.get("/", response_model=List[VendaResponse])
def listar_vendas(data: Optional[str] = None):
    """Lista vendas"""
    return venda_service.listar(data)


@router.get("/do-dia", response_model=List[VendaResponse])
def listar_vendas_do_dia():
    """Lista vendas do dia"""
    return venda_service.get_vendas_do_dia()


@router.get("/{venda_id}", response_model=VendaResponse)
def buscar_venda(venda_id: str):
    """Busca venda por ID"""
    venda = venda_service.buscar_por_id(venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


@router.post("/")
def criar_venda(dados: VendaCreate):
    """Cria nova venda"""
    resultado = venda_service.criar(dados)
    if "erro" in resultado:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return resultado