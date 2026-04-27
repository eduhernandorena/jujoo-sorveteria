# Serviço de Vendas
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.venda import Venda, VendaCreate, VendaResponse, ItemVenda
from src.models.caixa import MovimentoCaixaCreate
from src.repositories.arquivo_repo import ArquivoRepositorio
from src.core.config import ARQUIVO_VENDAS
from src.utils.logger import logger
from src.utils.helpers import gerar_id
from src.services.caixa_service import caixa_service
from src.services.estoque_service import estoque_service
from src.services.produto_service import produto_service
from src.mocks.pagto_mock import mock_pagamento
from src.mocks.nfce_mock import mock_nfce


class VendaService:
    """Serviço para gerenciar vendas"""
    
    def __init__(self):
        self.repo = ArquivoRepositorio(ARQUIVO_VENDAS, dict)
    
    def _to_response(self, venda: dict) -> VendaResponse:
        """Converte venda para response"""
        return VendaResponse(
            id=venda["id"],
            data=venda.get("data"),
            itens=[ItemVenda(**i) for i in venda.get("itens", [])],
            subtotal=venda["subtotal"],
            desconto_total=venda.get("desconto_total", 0),
            total=venda["total"],
            forma_pagamento=venda["forma_pagamento"],
            status=venda["status"],
            nfce_id=venda.get("nfce_id"),
            observacoes=venda.get("observacoes", "")
        )
    
    def criar(self, dados: VendaCreate) -> Dict[str, Any]:
        """Cria nova venda"""
        # Calcular totais
        subtotal = sum(item.quantidade * item.preco_unitario - item.desconto for item in dados.itens)
        total = subtotal - dados.desconto_total
        
        # Processar pagamento
        resultado_pagamento = mock_pagamento.processar(
            dados.forma_pagamento, 
            total, 
            {}
        )
        
        if resultado_pagamento.get("status") != "aprovado":
            return {"erro": "Pagamento não aprovado", "detalhes": resultado_pagamento}
        
        # Criar venda
        venda_dict = {
            "id": gerar_id("venda"),
            "itens": [item.model_dump() for item in dados.itens],
            "subtotal": subtotal,
            "desconto_total": dados.desconto_total,
            "total": total,
            "forma_pagamento": dados.forma_pagamento,
            "status": "ativo",
            "observacoes": dados.observacoes or ""
        }
        
        venda = self.repo.criar(venda_dict)
        
        # Registrar no caixa
        caixa_service.criar_movimento(MovimentoCaixaCreate(
            tipo="entrada",
            valor=total,
            origem="venda",
            descricao=f"Venda #{venda['id']}",
            referencia_id=venda["id"],
            forma_pagamento=dados.forma_pagamento
        ))
        
        # Emitir NFCe
        nfce = mock_nfce.emitir(
            venda_id=venda["id"],
            itens=[item.model_dump() for item in dados.itens],
            forma_pagamento=dados.forma_pagamento,
            total=subtotal,
            desconto=dados.desconto_total
        )

        # Atualizar venda com ID da NFCe
        self.repo.atualizar(venda["id"], {"nfce_id": nfce.id})

        logger.info(f"Venda criada: {venda['id']} - R$ {total}")

        return {
            "venda": self._to_response(self.repo.buscar_por_id(venda["id"])),
            "pagamento": resultado_pagamento,
            "nfce": nfce.model_dump()
        }
    
    def listar(self, data: Optional[str] = None) -> List[VendaResponse]:
        """Lista vendas"""
        vendas = self.repo.listar()
        
        if data:
            from src.utils.helpers import formatar_data_simples
            vendas = [v for v in vendas if formatar_data_simples(datetime.fromisoformat(v.get("data", ""))) == data]
        
        return [self._to_response(v) for v in vendas if v.get("status") == "ativo"]
    
    def buscar_por_id(self, id: str) -> Optional[VendaResponse]:
        """Busca venda por ID"""
        venda = self.repo.buscar_por_id(id)
        if venda:
            return self._to_response(venda)
        return None
    
    def get_vendas_do_dia(self) -> List[VendaResponse]:
        """Retorna vendas do dia"""
        from src.utils.helpers import formatar_data_simples
        return self.listar(data=formatar_data_simples(datetime.now()))
    
    def get_total_vendas_do_dia(self) -> float:
        """Retorna total de vendas do dia"""
        vendas = self.get_vendas_do_dia()
        return sum(v.total for v in vendas)


# Instância global
venda_service = VendaService()
