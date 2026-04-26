# Serviço de Produção
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.producao import Producao, ProducaoCreate, ProducaoResponse, ItemProducao
from src.repositories.arquivo_repo import ArquivoRepositorio
from src.core.config import ARQUIVO_PRODUCAO
from src.utils.logger import logger
from src.utils.helpers import gerar_id
from src.services.estoque_service import estoque_service
from src.services.produto_service import produto_service


class ProducaoService:
    """Serviço para gerenciar produção diária"""
    
    def __init__(self):
        self.repo = ArquivoRepositorio(ARQUIVO_PRODUCAO, dict)
    
    def _to_response(self, producao: dict) -> ProducaoResponse:
        """Converte produção para response"""
        return ProducaoResponse(
            id=producao["id"],
            data=producao.get("data"),
            itens=[ItemProducao(**i) for i in producao.get("itens", [])],
            total_itens=producao.get("total_itens", 0),
            status=producao["status"],
            observacoes=producao.get("observacoes", "")
        )
    
    def criar(self, dados: ProducaoCreate) -> Dict[str, Any]:
        """Cria nova produção"""
        # Validar e calcular matéria-prima necessária
        materias_utilizadas = []
        erros = []
        
        for item in dados.itens:
            # Buscar receita do produto
            produto = produto_service.buscar_por_id(item.produto_id)
            if not produto:
                erros.append(f"Produto {item.produto_id} não encontrado")
                continue
            
            # Verificar estoque de cada ingrediente
            for receita in produto.get("receita", []):
                mp_id = receita.get("materia_prima_id")
                qtd_necessaria = receita.get("quantidade", 0) * item.quantidade
                
                mp = estoque_service.buscar_por_id(mp_id)
                if not mp:
                    erros.append(f"Matéria-prima {mp_id} não encontrada")
                    continue
                
                if mp.quantidade_estoque < qtd_necessaria:
                    erros.append(f"Estoque insuficiente para {mp.nome}: necessário {qtd_necessaria}, disponível {mp.quantidade_estoque}")
                else:
                    # Baixar do estoque
                    estoque_service.remover_estoque(mp_id, qtd_necessaria)
                    materias_utilizadas.append({
                        "materia_prima": mp.nome,
                        "quantidade": qtd_necessaria,
                        "unidade": mp.unidade
                    })
        
        if erros:
            return {"erro": "Erros na produção", "detalhes": erros}
        
        # Calcular total de itens produzidos
        total_itens = sum(item.quantidade for item in dados.itens)
        
        # Criar registro de produção
        producao_dict = {
            "id": gerar_id("prod"),
            "itens": [item.model_dump() for item in dados.itens],
            "total_itens": total_itens,
            "status": "ativo",
            "observacoes": dados.observacoes or ""
        }
        
        producao = self.repo.criar(producao_dict)
        
        logger.info(f"Produção criada: {producao.id} - {total_itens} itens")
        
        return {
            "producao": self._to_response(self.repo.buscar_por_id(producao.id)),
            "materias_utilizadas": materias_utilizadas
        }
    
    def listar(self, data: Optional[str] = None) -> List[ProducaoResponse]:
        """Lista produções"""
        producoes = self.repo.listar()
        
        if data:
            from src.utils.helpers import formatar_data_simples
            producoes = [p for p in producoes if formatar_data_simples(datetime.fromisoformat(p.get("data", ""))) == data]
        
        return [self._to_response(p) for p in producoes if p.get("status") == "ativo"]
    
    def buscar_por_id(self, id: str) -> Optional[ProducaoResponse]:
        """Busca produção por ID"""
        producao = self.repo.buscar_por_id(id)
        if producao:
            return self._to_response(producao)
        return None
    
    def get_producoes_do_dia(self) -> List[ProducaoResponse]:
        """Retorna produções do dia"""
        from src.utils.helpers import formatar_data_simples
        return self.listar(data=formatar_data_simples(datetime.now()))
    
    def get_total_produzido_do_dia(self) -> int:
        """Retorna total de itens produzidos no dia"""
        producoes = self.get_producoes_do_dia()
        return sum(p.total_itens for p in producoes)


# Instância global
producao_service = ProducaoService()