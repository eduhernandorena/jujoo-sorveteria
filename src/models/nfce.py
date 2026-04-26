# Modelo de NFCe (Nota Fiscal de Consumidor Eletrônica)
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.core.constants import STATUS_ATIVO, ICMS_PADRAO, PIS_PADRAO, COFINS_PADRAO


class ItemNFCe(BaseModel):
    """Item da NFCe"""
    codigo: str
    descricao: str
    quantidade: float
    unidade: str
    preco_unitario: float
    total: float
    aliquota_icms: float = ICMS_PADRAO
    aliquota_pis: float = PIS_PADRAO
    aliquota_cofins: float = COFINS_PADRAO


class NFCe(BaseModel):
    """Modelo de NFCe"""
    id: str
    numero: int
    serie: int = 1
    data_emissao: datetime = Field(default_factory=datetime.now)
    chave_acesso: str
    itens: List[ItemNFCe]
    subtotal: float
    desconto: float = 0
    total: float
    valor_icms: float = 0
    valor_pis: float = 0
    valor_cofins: float = 0
    forma_pagamento: str
    status: str = STATUS_ATIVO
    xml: Optional[str] = None
    danfe: Optional[str] = None  # Representação simplificada do DANFE

    class Config:
        json_schema_extra = {
            "example": {
                "id": "nfce_001",
                "numero": 100,
                "serie": 1,
                "data_emissao": "2024-01-15T10:30:00",
                "chave_acesso": "12345678901234567890123456789012345678901234",
                "itens": [
                    {
                        "codigo": "prod_001",
                        "descricao": "Sorvete de Chocolate",
                        "quantidade": 2,
                        "unidade": "un",
                        "preco_unitario": 15.00,
                        "total": 30.00,
                        "aliquota_icms": 18.0,
                        "aliquota_pis": 1.65,
                        "aliquota_cofins": 7.6
                    }
                ],
                "subtotal": 30.00,
                "desconto": 0,
                "total": 30.00,
                "valor_icms": 5.40,
                "valor_pis": 0.50,
                "valor_cofins": 2.28,
                "forma_pagamento": "dinheiro",
                "status": "ativo"
            }
        }


class NFCeResponse(BaseModel):
    """Schema de resposta de NFCe"""
    id: str
    numero: int
    serie: int
    data_emissao: datetime
    chave_acesso: str
    itens: List[ItemNFCe]
    subtotal: float
    desconto: float
    total: float
    valor_icms: float
    valor_pis: float
    valor_cofins: float
    forma_pagamento: str
    status: str
    danfe: Optional[str]