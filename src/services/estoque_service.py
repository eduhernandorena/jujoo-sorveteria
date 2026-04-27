# Serviço de Matérias-Primas (Estoque)
from typing import List, Optional, Dict, Any
from src.models.materia_prima import MateriaPrima, MateriaPrimaCreate, MateriaPrimaUpdate, MateriaPrimaResponse
from src.repositories.arquivo_repo import ArquivoRepositorio
from src.core.config import ARQUIVO_MATERIAS_PRIMAS
from src.utils.logger import logger
from src.utils.helpers import gerar_id


class EstoqueService:
    """Serviço para gerenciar estoque de matérias-primas"""
    
    def __init__(self):
        self.repo = ArquivoRepositorio(ARQUIVO_MATERIAS_PRIMAS, dict)
    
    def listar(self) -> List[MateriaPrimaResponse]:
        """Lista todas as matérias-primas ativas"""
        materias = self.repo.buscar_por_filtro({"status": "ativo"})
        return [self._to_response(m) for m in materias]
    
    def buscar_por_id(self, id: str) -> Optional[MateriaPrimaResponse]:
        """Busca matéria-prima por ID"""
        materia = self.repo.buscar_por_id(id)
        if materia:
            return self._to_response(materia)
        return None
    
    def buscar_estoque_baixo(self) -> List[MateriaPrimaResponse]:
        """Busca matérias-primas com estoque abaixo do mínimo"""
        materias = self.repo.listar()
        resultado = []
        for m in materias:
            if m.get("status") == "ativo" and m.get("quantidade_estoque", 0) < m.get("quantidade_minima", 10):
                resultado.append(self._to_response(m))
        return resultado
    
    def criar(self, dados: MateriaPrimaCreate) -> MateriaPrimaResponse:
        """Cria nova matéria-prima"""
        materia_dict = {
            "id": gerar_id("mp"),
            "nome": dados.nome,
            "descricao": dados.descricao or "",
            "unidade": dados.unidade,
            "quantidade_estoque": dados.quantidade_estoque,
            "quantidade_minima": dados.quantidade_minima,
            "preco_unitario": dados.preco_unitario,
            "status": "ativo"
        }
        materia = self.repo.criar(materia_dict)
        logger.info(f"Matéria-prima criada: {materia['nome']}")
        return self._to_response(materia)
    
    def atualizar(self, id: str, dados: MateriaPrimaUpdate) -> Optional[MateriaPrimaResponse]:
        """Atualiza matéria-prima"""
        dados_dict = dados.model_dump(exclude_unset=True)
        materia = self.repo.atualizar(id, dados_dict)
        if materia:
            return self._to_response(materia)
        return None
    
    def deletar(self, id: str) -> bool:
        """Deleta matéria-prima (soft delete)"""
        return self.repo.atualizar(id, {"status": "inativo"}) is not None
    
    def adicionar_estoque(self, id: str, quantidade: float) -> Optional[MateriaPrimaResponse]:
        """Adiciona quantidade ao estoque"""
        materia = self.repo.buscar_por_id(id)
        if materia:
            novo_estoque = materia.get("quantidade_estoque", 0) + quantidade
            return self.atualizar(id, MateriaPrimaUpdate(quantidade_estoque=novo_estoque))
        return None
    
    def remover_estoque(self, id: str, quantidade: float) -> Optional[MateriaPrimaResponse]:
        """Remove quantidade do estoque"""
        materia = self.repo.buscar_por_id(id)
        if materia:
            novo_estoque = max(0, materia.get("quantidade_estoque", 0) - quantidade)
            return self.atualizar(id, MateriaPrimaUpdate(quantidade_estoque=novo_estoque))
        return None
    
    def get_resumo_estoque(self) -> Dict[str, Any]:
        """Retorna resumo do estoque"""
        materias = self.listar()
        total_itens = len(materias)
        estoque_baixo = len(self.buscar_estoque_baixo())
        valor_total = sum(m.quantidade_estoque * m.preco_unitario for m in materias)
        
        return {
            "total_itens": total_itens,
            "estoque_baixo": estoque_baixo,
            "valor_total": round(valor_total, 2),
            "itens": [m.model_dump() for m in materias]
        }
    
    def _to_response(self, materia: dict) -> MateriaPrimaResponse:
        """Converte matéria-prima para response"""
        return MateriaPrimaResponse(
            id=materia["id"],
            nome=materia["nome"],
            descricao=materia.get("descricao", ""),
            unidade=materia["unidade"],
            quantidade_estoque=materia.get("quantidade_estoque", 0),
            quantidade_minima=materia.get("quantidade_minima", 10),
            preco_unitario=materia.get("preco_unitario", 0),
            status=materia["status"],
            precisa_repor=materia.get("quantidade_estoque", 0) < materia.get("quantidade_minima", 10)
        )


# Instância global
estoque_service = EstoqueService()
