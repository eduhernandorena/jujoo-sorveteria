# Modelo de Compra
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.core.constants import STATUS_ATIVO


class ItemCompra(BaseModel):
    """Item de uma compra"""
    materia_prima_id: str
    materia_prima_nome: str
    quantidade: float = Field(..., gt=0)
    preco_unitario: float
    total: float


class Compra(BaseModel):
    """Modelo de compra"""
    id: str
    data: datetime = Field(default_factory=datetime.now)
    fornecedor: str
    itens: list[ItemCompra]
    subtotal: float
    desconto: float = Field(default=0, ge=0)
    total: float
    forma_pagamento: str = "dinheiro"
    status: str = STATUS_ATIVO
    observacoes: Optional[str] = ""

    class Config:
        json_schema_extra = {
            "example": {
                "id": "compra_001",
                "data": "2024-01-15T08:00:00",
                "fornecedor": "Distribuidora de Laticínios",
                "itens": [
                    {
                        "materia_prima_id": "mp_001",
                        "materia_prima_nome": "Leite Integral",
                        "quantidade": 20,
                        "preco_unitario": 5.00,
                        "total": 100.00
                    }
                ],
                "subtotal": 100.00,
                "desconto": 0,
                "total": 100.00,
                "forma_pagamento": "dinheiro",
                "status": "ativo"
            }
        }


class CompraCreate(BaseModel):
    """Schema para criar compra"""
    fornecedor: str
    itens: list[ItemCompra]
    forma_pagamento: str = "dinheiro"
    desconto: float = 0
    observacoes: Optional[str] = ""


class CompraResponse(BaseModel):
    """Schema de resposta de compra"""
    id: str
    data: datetime
    fornecedor: str
    itens: list[ItemCompra]
    subtotal: float
    desconto: float
    total: float
    forma_pagamento: str
    status: str
    observacoes: str