# Rotas de Compras
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from src.models.compra import CompraCreate, CompraResponse
from src.services.compra_service import compra_service

router = APIRouter(prefix="/compras", tags=["Compras"])


@router.get("/", response_model=List[CompraResponse])
def listar_compras(data: Optional[str] = None):
    """Lista compras"""
    return compra_service.listar(data)


@router.get("/do-dia", response_model=List[CompraResponse])
def listar_compras_do_dia():
    """Lista compras do dia"""
    return compra_service.get_compras_do_dia()


@router.get("/{compra_id}", response_model=CompraResponse)
def buscar_compra(compra_id: str):
    """Busca compra por ID"""
    compra = compra_service.buscar_por_id(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    return compra


@router.post("/")
def criar_compra(dados: CompraCreate):
    """Cria nova compra"""
    resultado = compra_service.criar(dados)
    if "erro" in resultado:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return resultado