# Testes Integrados - API
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestAPIProdutos:
    """Testes integrados para API de Produtos"""
    
    def test_listar_produtos(self):
        """Testa listagem de produtos"""
        response = client.get("/api/produtos/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_criar_produto(self):
        """Testa criação de produto"""
        dados = {
            "nome": "Sorvete de Morango",
            "categoria": "sorvete",
            "descricao": "Sorvete artesanal de morango",
            "preco_venda": 15.00,
            "custo_producao": 5.00,
            "receita": []
        }
        response = client.post("/api/produtos/", json=dados)
        assert response.status_code == 200
    
    def test_buscar_produto_inexistente(self):
        """Testa busca de produto inexistente"""
        response = client.get("/api/produtos/prod_inexistente")
        assert response.status_code == 404


class TestAPIEstoque:
    """Testes integrados para API de Estoque"""
    
    def test_listar_estoque(self):
        """Testa listagem de estoque"""
        response = client.get("/api/estoque/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_criar_materia_prima(self):
        """Testa criação de matéria-prima"""
        dados = {
            "nome": "Leite Integral",
            "descricao": "Leite fresco",
            "unidade": "l",
            "quantidade_estoque": 50,
            "quantidade_minima": 20,
            "preco_unitario": 5.00
        }
        response = client.post("/api/estoque/", json=dados)
        assert response.status_code == 200
    
    def test_resumo_estoque(self):
        """Testa obtenção de resumo"""
        response = client.get("/api/estoque/resumo")
        assert response.status_code == 200
        data = response.json()
        assert "total_itens" in data


class TestAPICaixa:
    """Testes integrados para API de Caixa"""
    
    def test_get_saldo(self):
        """Testa obtenção de saldo"""
        response = client.get("/api/caixa/saldo")
        assert response.status_code == 200
        data = response.json()
        assert "saldo_atual" in data
    
    def test_listar_movimentos(self):
        """Testa listagem de movimentos"""
        response = client.get("/api/caixa/movimentos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_criar_movimento(self):
        """Testa criação de movimento"""
        dados = {
            "tipo": "entrada",
            "valor": 100.00,
            "origem": "venda",
            "descricao": "Teste de entrada",
            "forma_pagamento": "dinheiro"
        }
        response = client.post("/api/caixa/movimento", json=dados)
        assert response.status_code == 200


class TestAPIVendas:
    """Testes integrados para API de Vendas"""
    
    def test_listar_vendas(self):
        """Testa listagem de vendas"""
        response = client.get("/api/vendas/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_listar_vendas_do_dia(self):
        """Testa listagem de vendas do dia"""
        response = client.get("/api/vendas/do-dia")
        assert response.status_code == 200


class TestAPICompras:
    """Testes integrados para API de Compras"""
    
    def test_listar_compras(self):
        """Testa listagem de compras"""
        response = client.get("/api/compras/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAPIProducao:
    """Testes integrados para API de Produção"""
    
    def test_listar_producoes(self):
        """Testa listagem de produções"""
        response = client.get("/api/producao/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_listar_producoes_do_dia(self):
        """Testa listagem de produções do dia"""
        response = client.get("/api/producao/do-dia")
        assert response.status_code == 200


class TestAPIRelatorios:
    """Testes integrados para API de Relatórios"""
    
    def test_dashboard(self):
        """Testa dashboard"""
        response = client.get("/api/relatorios/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "vendas" in data
        assert "caixa" in data
    
    def test_relatorio_vendas(self):
        """Testa relatório de vendas"""
        response = client.get("/api/relatorios/vendas")
        assert response.status_code == 200
    
    def test_relatorio_estoque(self):
        """Testa relatório de estoque"""
        response = client.get("/api/relatorios/estoque")
        assert response.status_code == 200
    
    def test_relatorio_caixa(self):
        """Testa relatório de caixa"""
        response = client.get("/api/relatorios/caixa")
        assert response.status_code == 200


class TestAPIMonitor:
    """Testes integrados para API de Monitor"""
    
    def test_status_recursos(self):
        """Testa status de recursos"""
        response = client.get("/api/monitor/status")
        assert response.status_code == 200
        data = response.json()
        assert "cpu_percent" in data
    
    def test_info_recursos(self):
        """Testa informações de recursos"""
        response = client.get("/api/monitor/info")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data


class TestAPIRaiz:
    """Testes para rotas raiz"""
    
    def test_root(self):
        """Testa rota raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "nome" in data
        assert "versao" in data
    
    def test_health_check(self):
        """Testa health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"