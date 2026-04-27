# Serviço de Compras
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.compra import Compra, CompraCreate, CompraResponse, ItemCompra
from src.models.caixa import MovimentoCaixaCreate
from src.repositories.arquivo_repo import ArquivoRepositorio
from src.core.config import ARQUIVO_COMPRAS
from src.utils.logger import logger
from src.utils.helpers import gerar_id
from src.services.caixa_service import caixa_service
from src.services.estoque_service import estoque_service


class CompraService:
    """Serviço para gerenciar compras"""
    
    def __init__(self):
        self.repo = ArquivoRepositorio(ARQUIVO_COMPRAS, dict)
    
    def _to_response(self, compra: dict) -> CompraResponse:
        """Converte compra para response"""
        return CompraResponse(
            id=compra["id"],
            data=compra.get("data"),
            fornecedor=compra["fornecedor"],
            itens=[ItemCompra(**i) for i in compra.get("itens", [])],
            subtotal=compra["subtotal"],
            desconto=compra.get("desconto", 0),
            total=compra["total"],
            forma_pagamento=compra["forma_pagamento"],
            status=compra["status"],
            observacoes=compra.get("observacoes", "")
        )
    
    def criar(self, dados: CompraCreate) -> Dict[str, Any]:
        """Cria nova compra"""
        # Calcular totais
        subtotal = sum(item.quantidade * item.preco_unitario for item in dados.itens)
        total = subtotal - dados.desconto
        
        # Criar compra
        compra_dict = {
            "id": gerar_id("compra"),
            "fornecedor": dados.fornecedor,
            "itens": [item.model_dump() for item in dados.itens],
            "subtotal": subtotal,
            "desconto": dados.desconto,
            "total": total,
            "forma_pagamento": dados.forma_pagamento,
            "status": "ativo",
            "observacoes": dados.observacoes or ""
        }
        
        compra = self.repo.criar(compra_dict)
        
        # Registrar no caixa
        caixa_service.criar_movimento(MovimentoCaixaCreate(
            tipo="saida",
            valor=total,
            origem="compra",
            descricao=f"Compra #{compra['id']} - {dados.fornecedor}",
            referencia_id=compra["id"],
            forma_pagamento=dados.forma_pagamento
        ))
        
        # Atualizar estoque
        for item in dados.itens:
            estoque_service.adicionar_estoque(
                item.materia_prima_id,
                item.quantidade
            )
        
        logger.info(f"Compra criada: {compra['id']} - R$ {total}")

        return {
            "compra": self._to_response(self.repo.buscar_por_id(compra["id"])),
            "estoque_atualizado": True
        }
    
    def listar(self, data: Optional[str] = None) -> List[CompraResponse]:
        """Lista compras"""
        compras = self.repo.listar()
        
        if data:
            from src.utils.helpers import formatar_data_simples
            compras = [c for c in compras if formatar_data_simples(datetime.fromisoformat(c.get("data", ""))) == data]
        
        return [self._to_response(c) for c in compras if c.get("status") == "ativo"]
    
    def buscar_por_id(self, id: str) -> Optional[CompraResponse]:
        """Busca compra por ID"""
        compra = self.repo.buscar_por_id(id)
        if compra:
            return self._to_response(compra)
        return None
    
    def get_compras_do_dia(self) -> List[CompraResponse]:
        """Retorna compras do dia"""
        from src.utils.helpers import formatar_data_simples
        return self.listar(data=formatar_data_simples(datetime.now()))
    
    def get_total_compras_do_dia(self) -> float:
        """Retorna total de compras do dia"""
        compras = self.get_compras_do_dia()
        return sum(c.total for c in compras)


# Instância global
compra_service = CompraService()
