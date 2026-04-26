# Modelo de Venda
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.core.constants import STATUS_ATIVO, FORMAS_PAGAMENTO


class ItemVenda(BaseModel):
    """Item de uma venda"""
    produto_id: str
    produto_nome: str
    quantidade: float = Field(..., gt=0)
    preco_unitario: float
    desconto: float = Field(default=0, ge=0)
    total: float


class Venda(BaseModel):
    """Modelo de venda"""
    id: str
    data: datetime = Field(default_factory=datetime.now)
    itens: List[ItemVenda]
    subtotal: float
    desconto_total: float = Field(default=0, ge=0)
    total: float
    forma_pagamento: str = Field(..., pattern="|".join(FORMAS_PAGAMENTO))
    status: str = STATUS_ATIVO
    nfce_id: Optional[str] = None
    observacoes: Optional[str] = ""

    class Config:
        json_schema_extra = {
            "example": {
                "id": "venda_001",
                "data": "2024-01-15T10:30:00",
                "itens": [
                    {
                        "produto_id": "prod_001",
                        "produto_nome": "Sorvete de Chocolate",
                        "quantidade": 2,
                        "preco_unitario": 15.00,
                        "desconto": 0,
                        "total": 30.00
                    }
                ],
                "subtotal": 30.00,
                "desconto_total": 0,
                "total": 30.00,
                "forma_pagamento": "dinheiro",
                "status": "ativo"
            }
        }


class VendaCreate(BaseModel):
    """Schema para criar venda"""
    itens: List[ItemVenda]
    forma_pagamento: str
    desconto_total: float = 0
    observacoes: Optional[str] = ""


class VendaResponse(BaseModel):
    """Schema de resposta de venda"""
    id: str
    data: datetime
    itens: List[ItemVenda]
    subtotal: float
    desconto_total: float
    total: float
    forma_pagamento: str
    status: str
    nfce_id: Optional[str]
    observacoes: str