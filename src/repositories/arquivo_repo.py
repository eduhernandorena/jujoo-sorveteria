# Repositório de Persistência em Arquivo
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar
from datetime import datetime
from src.core.config import DATA_DIR
from src.utils.logger import logger

T = TypeVar('T')


class ArquivoRepositorio:
    """Repositório genérico para persistência em arquivo JSON"""
    
    def __init__(self, arquivo: Path, modelo: Type[T]):
        self.arquivo = arquivo
        self.modelo = modelo
        self._garantir_arquivo()
    
    def _garantir_arquivo(self):
        """Garante que o arquivo existe"""
        if not self.arquivo.exists():
            self.arquivo.parent.mkdir(parents=True, exist_ok=True)
            self._salvar([])
    
    def _carregar(self) -> List[Dict]:
        """Carrega dados do arquivo"""
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Arquivo {self.arquivo} corrompido, criando novo")
            return []
        except FileNotFoundError:
            return []
    
    def _salvar(self, dados: List[Dict]):
        """Salva dados no arquivo"""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    
    def listar(self) -> List[T]:
        """Lista todos os registros"""
        dados = self._carregar()
        if self.modelo is dict:
            return dados
        return [self.modelo(**item) for item in dados]
    
    def buscar_por_id(self, id: str) -> Optional[T]:
        """Busca registro por ID"""
        dados = self._carregar()
        for item in dados:
            if item.get('id') == id:
                if self.modelo is dict:
                    return item
                return self.modelo(**item)
        return None
    
    def buscar_por_campo(self, campo: str, valor: Any) -> List[T]:
        """Busca registros por campo"""
        dados = self._carregar()
        if self.modelo is dict:
            return [item for item in dados if item.get(campo) == valor]
        return [self.modelo(**item) for item in dados if item.get(campo) == valor]
    
    def buscar_por_filtro(self, filtros: Dict[str, Any]) -> List[T]:
        """Busca registros com múltiplos filtros"""
        dados = self._carregar()
        resultados = []
        for item in dados:
            match = True
            for campo, valor in filtros.items():
                if item.get(campo) != valor:
                    match = False
                    break
            if match:
                if self.modelo is dict:
                    resultados.append(item)
                else:
                    resultados.append(self.modelo(**item))
        return resultados
    
    def criar(self, dados: Dict) -> T:
        """Cria novo registro"""
        lista = self._carregar()
        if self.modelo is dict:
            novo = dados.copy()
            agora = datetime.now().isoformat()
            novo.setdefault("data", agora)
            novo.setdefault("data_cadastro", agora)
            novo.setdefault("data_atualizacao", agora)
            lista.append(novo)
        else:
            novo = self.modelo(**dados)
            lista.append(novo.model_dump(mode='json'))
        self._salvar(lista)
        logger.info(f"Criado registro {novo['id'] if self.modelo is dict else novo.id} em {self.arquivo.name}")
        return novo
    
    def atualizar(self, id: str, dados: Dict) -> Optional[T]:
        """Atualiza registro existente"""
        lista = self._carregar()
        for i, item in enumerate(lista):
            if item.get('id') == id:
                dados['data_atualizacao'] = datetime.now().isoformat()
                lista[i].update(dados)
                self._salvar(lista)
                logger.info(f"Atualizado registro {id} em {self.arquivo.name}")
                if self.modelo is dict:
                    return lista[i]
                return self.modelo(**lista[i])
        return None
    
    def deletar(self, id: str) -> bool:
        """Deleta registro"""
        lista = self._carregar()
        nova_lista = [item for item in lista if item.get('id') != id]
        if len(nova_lista) < len(lista):
            self._salvar(nova_lista)
            logger.info(f"Deletado registro {id} de {self.arquivo.name}")
            return True
        return False
    
    def contar(self) -> int:
        """Conta total de registros"""
        return len(self._carregar())
    
    def limpar(self):
        """Limpa todos os registros"""
        self._salvar([])
        logger.info(f"Limpos todos os registros de {self.arquivo.name}")


# Factory para criar repositórios
_repositorios: Dict[str, ArquivoRepositorio] = {}


def get_repositorio(arquivo: Path, modelo: Type[T]) -> ArquivoRepositorio:
    """Factory para obter ou criar repositório"""
    key = str(arquivo)
    if key not in _repositorios:
        _repositorios[key] = ArquivoRepositorio(arquivo, modelo)
    return _repositorios[key]
