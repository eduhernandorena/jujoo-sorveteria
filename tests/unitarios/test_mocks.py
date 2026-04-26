# Testes Unitários - Mocks
import pytest
from src.mocks.pagto_mock import MockPagamento
from src.mocks.nfce_mock import MockNFCe


class TestMockPagamento:
    """Testes para mock de pagamento"""
    
    def setup_method(self):
        self.mock = MockPagamento()
    
    def test_processar_dinheiro(self):
        """Testa processamento de pagamento em dinheiro"""
        resultado = self.mock.processar_dinheiro(100.00, {})
        
        assert resultado["status"] == "aprovado"
        assert resultado["valor"] == 100.00
        assert resultado["forma"] == "dinheiro"
    
    def test_processar_pix(self):
        """Testa processamento de pagamento PIX"""
        resultado = self.mock.processar_pix(100.00, {})
        
        assert resultado["status"] == "aprovado"
        assert resultado["valor"] == 100.00
        assert resultado["forma"] == "pix"
        assert "qr_code" in resultado
    
    def test_processar_cartao_credito(self):
        """Testa processamento de cartão de crédito"""
        resultado = self.mock.processar_cartao_credito(100.00, {"bandeira": "visa"})
        
        assert resultado["status"] == "aprovado"
        assert resultado["forma"] == "cartao_credito"
        assert resultado["bandeira"] == "visa"
    
    def test_processar_cartao_debito(self):
        """Testa processamento de cartão de débito"""
        resultado = self.mock.processar_cartao_debito(100.00, {})
        
        assert resultado["status"] == "aprovado"
        assert resultado["forma"] == "cartao_debito"
    
    def test_processar_forma_invalida(self):
        """Testa forma de pagamento inválida"""
        resultado = self.mock.processar("forma_invalida", 100.00, {})
        
        assert resultado["status"] == "erro"
    
    def test_estornar(self):
        """Testa estorno"""
        resultado = self.mock.estornar("transacao_123")
        
        assert resultado["status"] == "estornado"


class TestMockNFCe:
    """Testes para mock de NFCe"""
    
    def setup_method(self):
        self.mock = MockNFCe()
    
    def test_emitir_nfce(self):
        """Testa emissão de NFCe"""
        itens = [
            {"produto_id": "prod_001", "produto_nome": "Sorvete", 
             "quantidade": 2, "preco_unitario": 15.00}
        ]
        
        nfce = self.mock.emitir("venda_001", itens, "dinheiro", 30.00, 0)
        
        assert nfce.numero == 1
        assert nfce.total == 30.00
        assert len(nfce.itens) == 1
        assert nfce.danfe is not None
    
    def test_consultar_nfce(self):
        """Testa consulta de NFCe"""
        itens = [
            {"produto_id": "prod_001", "produto_nome": "Sorvete",
             "quantidade": 1, "preco_unitario": 10.00}
        ]
        
        nfce = self.mock.emitir("venda_001", itens, "dinheiro", 10.00, 0)
        consultada = self.mock.consultar(nfce.numero)
        
        assert consultada is not None
        assert consultada.numero == nfce.numero
    
    def test_cancelar_nfce(self):
        """Testa cancelamento de NFCe"""
        itens = [{"produto_id": "prod_001", "produto_nome": "Sorvete",
                  "quantidade": 1, "preco_unitario": 10.00}]
        
        nfce = self.mock.emitir("venda_001", itens, "dinheiro", 10.00, 0)
        resultado = self.mock.cancelar(nfce.numero)
        
        assert resultado is True
        assert self.mock.consultar(nfce.numero).status == "cancelado"
    
    def test_get_emitente(self):
        """Testa obtenção de dados do emitente"""
        emitente = self.mock.get_emitente()
        
        assert "nome" in emitente
        assert "cnpj" in emitente
        assert emitente["nome"] == "Jujoo Sorveteria"