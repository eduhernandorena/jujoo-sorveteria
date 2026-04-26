# Modelo de Produto
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.core.constants import STATUS_ATIVO


class ReceitaItem(BaseModel):
    """Item de receita (ingrediente)"""
    materia_prima_id: str
    quantidade: float
    unidade: str


class Produto(BaseModel):
    """Modelo de produto final"""
    id: str
    nome: str
    categoria: str
    descricao: Optional[str] = ""
    preco_venda: float
    custo_producao: float = 0
    receita: List[ReceitaItem] = []
    foto_url: Optional[str] = None
    status: str = STATUS_ATIVO
    data_cadastro: datetime = Field(default_factory=datetime.now)
    data_atualizacao: datetime = Field(default_factory=datetime.now)


class ProdutoCreate(BaseModel):
    """Schema para criar produto"""
    nome: str
    categoria: str
    descricao: Optional[str] = ""
    preco_venda: float
    custo_producao: float = 0
    receita: List[ReceitaItem] = []


class ProdutoUpdate(BaseModel):
    """Schema para atualizar produto"""
    nome: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    preco_venda: Optional[float] = None
    custo_producao: Optional[float] = None
    receita: Optional[List[ReceitaItem]] = None
    status: Optional[str] = None


class ProdutoResponse(BaseModel):
    """Schema de resposta de produto"""
    id: str
    nome: str
    categoria: str
    descricao: str
    preco_venda: float
    custo_producao: float
    status: str
    data_cadastro: datetime
    data_atualizacao: datetime