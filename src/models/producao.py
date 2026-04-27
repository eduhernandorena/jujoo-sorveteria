# Modelo de Produção
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.core.constants import STATUS_ATIVO


class ItemProducao(BaseModel):
    """Item de produção"""
    produto_id: str
    produto_nome: str
    quantidade: float = Field(..., gt=0)


class ConsumoMateriaPrima(BaseModel):
    """Matéria-prima consumida em uma produção"""
    materia_prima_id: str
    materia_prima_nome: str
    quantidade: float = Field(..., gt=0)
    unidade: str


class ItemProducaoCreate(ItemProducao):
    """Item de produção com consumo informado para o lote"""
    materias_primas: List[ConsumoMateriaPrima] = []


class Producao(BaseModel):
    """Modelo de produção diária"""
    id: str
    data: datetime = Field(default_factory=datetime.now)
    itens: List[ItemProducaoCreate]
    total_itens: int
    status: str = STATUS_ATIVO
    observacoes: Optional[str] = ""

    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_001",
                "data": "2024-01-15T06:00:00",
                "itens": [
                    {
                        "produto_id": "prod_001",
                        "produto_nome": "Sorvete de Chocolate",
                        "quantidade": 10
                    }
                ],
                "total_itens": 10,
                "status": "ativo"
            }
        }


class ProducaoCreate(BaseModel):
    """Schema para criar produção"""
    itens: List[ItemProducaoCreate]
    observacoes: Optional[str] = ""


class ProducaoResponse(BaseModel):
    """Schema de resposta de produção"""
    id: str
    data: datetime
    itens: List[ItemProducaoCreate]
    total_itens: int
    status: str
    observacoes: str
