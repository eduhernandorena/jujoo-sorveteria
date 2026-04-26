# Rotas de Produtos
from fastapi import APIRouter, HTTPException
from typing import List
from src.models.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from src.services.produto_service import produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos():
    """Lista todos os produtos"""
    return produto_service.listar()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: str):
    """Busca produto por ID"""
    produto = produto_service.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.get("/categoria/{categoria}", response_model=List[ProdutoResponse])
def listar_por_categoria(categoria: str):
    """Lista produtos por categoria"""
    return produto_service.buscar_por_categoria(categoria)


@router.post("/", response_model=ProdutoResponse)
def criar_produto(dados: ProdutoCreate):
    """Cria novo produto"""
    return produto_service.criar(dados)


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: str, dados: ProdutoUpdate):
    """Atualiza produto"""
    produto = produto_service.atualizar(produto_id, dados)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.delete("/{produto_id}")
def deletar_produto(produto_id: str):
    """Deleta produto"""
    if produto_service.deletar(produto_id):
        return {"mensagem": "Produto deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Produto não encontrado")