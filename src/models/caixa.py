# Modelo de Caixa
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.core.constants import TIPO_ENTRADA, TIPO_SAIDA, ORIGEM_VENDA, ORIGEM_COMPRA, ORIGEM_DESPESA, ORIGEM_RECEBIMENTO, ORIGEM_PRODUCAO


class MovimentoCaixa(BaseModel):
    """Modelo de movimento de caixa"""
    id: str
    data: datetime = Field(default_factory=datetime.now)
    tipo: str = Field(..., pattern=f"{TIPO_ENTRADA}|{TIPO_SAIDA}")
    valor: float = Field(..., gt=0)
    origem: str = Field(..., pattern=f"{ORIGEM_VENDA}|{ORIGEM_COMPRA}|{ORIGEM_DESPESA}|{ORIGEM_RECEBIMENTO}|{ORIGEM_PRODUCAO}")
    descricao: str
    referencia_id: Optional[str] = None  # ID da venda/compra/etc
    forma_pagamento: str = "dinheiro"

    class Config:
        json_schema_extra = {
            "example": {
                "id": "mov_001",
                "data": "2024-01-15T10:30:00",
                "tipo": "entrada",
                "valor": 30.00,
                "origem": "venda",
                "descricao": "Venda #venda_001",
                "referencia_id": "venda_001",
                "forma_pagamento": "dinheiro"
            }
        }


class FechamentoDiario(BaseModel):
    """Modelo de fechamento diário"""
    id: str
    data: str  # Data no formato YYYY-MM-DD
    entrada_dinheiro: float = 0
    entrada_pix: float = 0
    entrada_cartao_credito: float = 0
    entrada_cartao_debito: float = 0
    saida_dinheiro: float = 0
    saida_pix: float = 0
    saida_cartao_credito: float = 0
    saida_cartao_debito: float = 0
    total_entradas: float = 0
    total_saidas: float = 0
    saldo: float = 0
    status: str = "aberto"
    data_fechamento: Optional[datetime] = None


class FechamentoMensal(BaseModel):
    """Modelo de fechamento mensal"""
    id: str
    mes: str  # Formato YYYY-MM
    entrada_dinheiro: float = 0
    entrada_pix: float = 0
    entrada_cartao_credito: float = 0
    entrada_cartao_debito: float = 0
    saida_dinheiro: float = 0
    saida_pix: float = 0
    saida_cartao_credito: float = 0
    saida_cartao_debito: float = 0
    total_entradas: float = 0
    total_saidas: float = 0
    saldo: float = 0
    status: str = "aberto"
    data_fechamento: Optional[datetime] = None


class MovimentoCaixaCreate(BaseModel):
    """Schema para criar movimento"""
    tipo: str
    valor: float
    origem: str
    descricao: str
    referencia_id: Optional[str] = None
    forma_pagamento: str = "dinheiro"


class MovimentoCaixaResponse(BaseModel):
    """Schema de resposta de movimento"""
    id: str
    data: datetime
    tipo: str
    valor: float
    origem: str
    descricao: str
    referencia_id: Optional[str]
    forma_pagamento: str