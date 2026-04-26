# Serviço de Produtos
from typing import List, Optional
from src.models.produto import Produto, ProdutoCreate, ProdutoUpdate, ProdutoResponse
from src.repositories.arquivo_repo import ArquivoRepositorio
from src.core.config import ARQUIVO_PRODUTOS
from src.utils.logger import logger
from src.utils.helpers import gerar_id


class ProdutoService:
    """Serviço para gerenciar produtos"""
    
    def __init__(self):
        self.repo = ArquivoRepositorio(ARQUIVO_PRODUTOS, dict)
    
    def listar(self) -> List[ProdutoResponse]:
        """Lista todos os produtos ativos"""
        produtos = self.repo.buscar_por_filtro({"status": "ativo"})
        return [self._to_response(p) for p in produtos]
    
    def buscar_por_id(self, id: str) -> Optional[ProdutoResponse]:
        """Busca produto por ID"""
        produto = self.repo.buscar_por_id(id)
        if produto:
            return self._to_response(produto)
        return None
    
    def buscar_por_categoria(self, categoria: str) -> List[ProdutoResponse]:
        """Busca produtos por categoria"""
        produtos = self.repo.buscar_por_filtro({"categoria": categoria, "status": "ativo"})
        return [self._to_response(p) for p in produtos]
    
    def criar(self, dados: ProdutoCreate) -> ProdutoResponse:
        """Cria novo produto"""
        produto_dict = {
            "id": gerar_id("prod"),
            "nome": dados.nome,
            "categoria": dados.categoria,
            "descricao": dados.descricao or "",
            "preco_venda": dados.preco_venda,
            "custo_producao": dados.custo_producao,
            "receita": [r.model_dump() for r in dados.receita],
            "status": "ativo"
        }
        produto = self.repo.criar(produto_dict)
        logger.info(f"Produto criado: {produto.nome}")
        return self._to_response(produto)
    
    def atualizar(self, id: str, dados: ProdutoUpdate) -> Optional[ProdutoResponse]:
        """Atualiza produto"""
        dados_dict = dados.model_dump(exclude_unset=True)
        produto = self.repo.atualizar(id, dados_dict)
        if produto:
            return self._to_response(produto)
        return None
    
    def deletar(self, id: str) -> bool:
        """Deleta produto (soft delete)"""
        return self.repo.atualizar(id, {"status": "inativo"}) is not None
    
    def _to_response(self, produto: dict) -> ProdutoResponse:
        """Converte produto para response"""
        return ProdutoResponse(
            id=produto["id"],
            nome=produto["nome"],
            categoria=produto["categoria"],
            descricao=produto.get("descricao", ""),
            preco_venda=produto["preco_venda"],
            custo_producao=produto.get("custo_producao", 0),
            status=produto["status"],
            data_cadastro=produto.get("data_cadastro"),
            data_atualizacao=produto.get("data_atualizacao")
        )


# Instância global
produto_service = ProdutoService()