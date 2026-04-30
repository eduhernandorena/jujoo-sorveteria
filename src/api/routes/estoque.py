# Rotas de Matérias-Primas / Estoque
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.models.materia_prima import MateriaPrimaCreate, MateriaPrimaUpdate, MateriaPrimaResponse
from src.services.estoque_service import estoque_service

router = APIRouter(prefix="/estoque", tags=["Estoque"])

class QuantidadeRequest(BaseModel):
    """Payload para quantidade de estoque."""
    quantidade: float



@router.get("/", response_model=List[MateriaPrimaResponse])
def listar_estoque():
    """Lista todas as matérias-primas"""
    return estoque_service.listar()


@router.get("/baixo", response_model=List[MateriaPrimaResponse])
def listar_estoque_baixo():
    """Lista matérias-primas com estoque baixo"""
    return estoque_service.buscar_estoque_baixo()


@router.get("/resumo")
def get_resumo_estoque():
    """Retorna resumo do estoque"""
    return estoque_service.get_resumo_estoque()


@router.get("/{materia_id}", response_model=MateriaPrimaResponse)
def buscar_materia(materia_id: str):
    """Busca matéria-prima por ID"""
    materia = estoque_service.buscar_por_id(materia_id)
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")
    return materia


@router.post("/", response_model=MateriaPrimaResponse)
def criar_materia(dados: MateriaPrimaCreate):
    """Cria nova matéria-prima"""
    return estoque_service.criar(dados)


@router.put("/{materia_id}", response_model=MateriaPrimaResponse)
def atualizar_materia(materia_id: str, dados: MateriaPrimaUpdate):
    """Atualiza matéria-prima"""
    materia = estoque_service.atualizar(materia_id, dados)
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")
    return materia


@router.post("/{materia_id}/adicionar")
def adicionar_estoque(materia_id: str, quantidade: float | None = None, payload: QuantidadeRequest | None = None):
    """Adiciona quantidade ao estoque"""
    # Validação básica: quantidade deve ser positiva
    if quantidade is None:
        if payload is not None:
            quantidade = payload.quantidade
    if quantidade is None or quantidade <= 0:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")
    materia = estoque_service.adicionar_estoque(materia_id, quantidade)
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")
    return {"mensagem": "Estoque atualizado", "materia": materia}


@router.post("/{materia_id}/remover")
def remover_estoque(materia_id: str, quantidade: float | None = None, payload: QuantidadeRequest | None = None):
    """Remove quantidade do estoque"""
    # Validação básica: quantidade deve ser positiva
    if quantidade is None:
        if payload is not None:
            quantidade = payload.quantidade
    if quantidade is None or quantidade <= 0:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")
    materia = estoque_service.remover_estoque(materia_id, quantidade)
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")
    return {"mensagem": "Estoque atualizado", "materia": materia}


@router.delete("/{materia_id}")
def deletar_materia(materia_id: str):
    """Deleta matéria-prima"""
    if estoque_service.deletar(materia_id):
        return {"mensagem": "Matéria-prima deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Matéria-prima não encontrada")
