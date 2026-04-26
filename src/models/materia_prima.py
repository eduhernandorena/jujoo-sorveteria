# Modelo de Matéria-Prima
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.core.constants import STATUS_ATIVO, UNIDADES


class MateriaPrima(BaseModel):
    """Modelo de matéria-prima"""
    id: str
    nome: str
    descricao: Optional[str] = ""
    unidade: str = Field(..., pattern="|".join(UNIDADES.keys()))
    quantidade_estoque: float = Field(default=0, ge=0)
    quantidade_minima: float = Field(default=10, ge=0)
    preco_unitario: float = Field(default=0, ge=0)
    status: str = STATUS_ATIVO
    data_cadastro: datetime = Field(default_factory=datetime.now)
    data_atualizacao: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "mp_001",
                "nome": "Leite Integral",
                "descricao": "Leite fresco tipo A",
                "unidade": "l",
                "quantidade_estoque": 50,
                "quantidade_minima": 20,
                "preco_unitario": 5.00,
                "status": "ativo"
            }
        }


class MateriaPrimaCreate(BaseModel):
    """Schema para criar matéria-prima"""
    nome: str
    descricao: Optional[str] = ""
    unidade: str
    quantidade_estoque: float = 0
    quantidade_minima: float = 10
    preco_unitario: float = 0


class MateriaPrimaUpdate(BaseModel):
    """Schema para atualizar matéria-prima"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    unidade: Optional[str] = None
    quantidade_estoque: Optional[float] = None
    quantidade_minima: Optional[float] = None
    preco_unitario: Optional[float] = None
    status: Optional[str] = None


class MateriaPrimaResponse(BaseModel):
    """Schema de resposta de matéria-prima"""
    id: str
    nome: str
    descricao: str
    unidade: str
    quantidade_estoque: float
    quantidade_minima: float
    preco_unitario: float
    status: str
    precisa_repor: bool