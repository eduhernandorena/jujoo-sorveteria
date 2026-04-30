# Testes de integração da API (Rodada 3) - endpoints principais com mocks
from fastapi.testclient import TestClient
from src.api.main import app
import json

client = TestClient(app)


class FakeProdutoService:
    def listar(self):
        return [
            {
                "id": "p1",
                "nome": "Sorvete A",
                "categoria": "sorvete",
                "descricao": "",
                "preco_venda": 9.99,
                "custo_producao": 0,
                "receita": [],
                "status": "ativo",
                "data_cadastro": "2026-01-01T00:00:00",
                "data_atualizacao": "2026-01-01T00:00:00",
            }
        ]

    def buscar_por_id(self, produto_id):
        if produto_id == "p1":
            return {
                "id": "p1",
                "nome": "Sorvete A",
                "categoria": "sorvete",
                "descricao": "",
                "preco_venda": 9.99,
                "custo_producao": 0,
                "receita": [],
                "status": "ativo",
                "data_cadastro": "2026-01-01T00:00:00",
                "data_atualizacao": "2026-01-01T00:00:00",
            }
        return None

    def criar(self, dados):
        return {"id": "p2", "nome": dados.nome, "categoria": dados.categoria}

    def atualizar(self, produto_id, dados):
        if produto_id == "p1":
            return {"id": produto_id, "nome": dados.nome or "Sorvete A"}
        return None

    def deletar(self, produto_id):
        return produto_id == "p1"


class FakeEstoqueService:
    def listar(self):
        return [
            {
                "id": "mp1",
                "nome": "Leite",
                "descricao": "",
                "unidade": "l",
                "quantidade_estoque": 20,
                "quantidade_minima": 10,
                "preco_unitario": 5.0,
                "status": "ativo",
                "precisa_repor": False,
                "data_cadastro": "2026-01-01T00:00:00",
                "data_atualizacao": "2026-01-01T00:00:00",
            }
        ]

    def buscar_por_id(self, materia_id):
        if materia_id == "mp1":
            return {
                "id": "mp1",
                "nome": "Leite",
                "descricao": "",
                "unidade": "l",
                "quantidade_estoque": 20,
                "quantidade_minima": 10,
                "preco_unitario": 5.0,
                "status": "ativo",
                "data_cadastro": "2026-01-01T00:00:00",
                "data_atualizacao": "2026-01-01T00:00:00",
            }
        return None

    def criar(self, dados):
        return {"id": "mp2", "nome": dados.nome}

    def atualizar(self, materia_id, dados):
        if materia_id == "mp1":
            return {"id": materia_id, "nome": dados.nome or "Leite"}
        return None

    def adicionar_estoque(self, materia_id, quantidade):
        if materia_id != "mp1":
            return None
        return {"id": materia_id, "quantidade_estoque": 20 + quantidade}

    def remover_estoque(self, materia_id, quantidade):
        if materia_id != "mp1":
            return None
        return {"id": materia_id, "quantidade_estoque": max(0, 20 - quantidade)}

    def deletar(self, materia_id):
        return materia_id == "mp1"


import types
def test_produtos_endpoints_monkeypatched(monkeypatch):
    # Patcha serviços para retornar dados simulados
    import src.api.routes.produtos as rotas_produtos
    monkeypatch.setattr(rotas_produtos, "produto_service", FakeProdutoService())

    resp = client.get("/api/produtos/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["id"] == "p1"

    resp_id = client.get("/api/produtos/p1")
    assert resp_id.status_code == 200
    assert resp_id.json()["id"] == "p1" or resp_id.json()["id"] == "p1"

def test_produto_nao_encontrado(monkeypatch):
    import src.api.routes.produtos as rotas_produtos
    class _Svc(FakeProdutoService):
        def buscar_por_id(self, produto_id):
            return None
    monkeypatch.setattr(rotas_produtos, "produto_service", _Svc())
    resp = client.get("/api/produtos/nao-existe")
    assert resp.status_code == 404

def test_estoque_endpoints_monkeypatched(monkeypatch):
    import src.api.routes.estoque as rotas_estoque
    monkeypatch.setattr(rotas_estoque, "estoque_service", FakeEstoqueService())

    resp = client.get("/api/estoque/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["id"] == "mp1"

    # Adicionar via payload (valor positivo)
    resp_add = client.post("/api/estoque/mp1/adicionar", json={"quantidade": 5})
    assert resp_add.status_code == 200
    assert "Estoque atualizado" in resp_add.json()["mensagem"]

    # Adicionar via payload (valor negativo deve falhar)
    resp_bad = client.post("/api/estoque/mp1/adicionar", json={"quantidade": -3})
    assert resp_bad.status_code == 400

    # Remover via payload
    resp_rem = client.post("/api/estoque/mp1/remover", json={"quantidade": 2})
    assert resp_rem.status_code == 200

def test_health_and_root():
    resp = client.get("/")
    assert resp.status_code == 200
    resp_h = client.get("/health")
    assert resp_h.status_code == 200
