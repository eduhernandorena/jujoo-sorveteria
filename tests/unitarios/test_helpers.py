# Testes Unitários - Helpers
import pytest
from src.utils.helpers import (
    gerar_id, formatar_moeda, formatar_data, formatar_data_simples,
    calcular_percentual, calcular_icms, calcular_pis, calcular_cofins,
    gerar_chave_acesso
)


class TestHelpers:
    """Testes para funções utilitárias"""
    
    def test_gerar_id(self):
        """Testa geração de ID"""
        id1 = gerar_id("test")
        id2 = gerar_id("test")
        
        assert id1.startswith("test_")
        assert id2.startswith("test_")
        assert id1 != id2  # IDs devem ser únicos
    
    def test_formatar_moeda(self):
        """Testa formatação de moeda"""
        resultado = formatar_moeda(10.50)
        assert "R$" in resultado
        assert "10" in resultado
        assert "50" in resultado
    
    def test_calcular_percentual(self):
        """Testa cálculo de percentual"""
        assert calcular_percentual(25, 100) == 25.0
        assert calcular_percentual(10, 50) == 20.0
        assert calcular_percentual(0, 100) == 0.0
        assert calcular_percentual(50, 0) == 0.0  # Evita divisão por zero
    
    def test_calcular_icms(self):
        """Testa cálculo de ICMS"""
        assert calcular_icms(100, 18) == 18.0
        assert calcular_icms(50, 18) == 9.0
    
    def test_calcular_pis(self):
        """Testa cálculo de PIS"""
        assert calcular_pis(100, 1.65) == 1.65
        assert calcular_pis(50, 1.65) == 0.83
    
    def test_calcular_cofins(self):
        """Testa cálculo de COFINS"""
        assert calcular_cofins(100, 7.6) == 7.6
        assert calcular_cofins(50, 7.6) == 3.8
    
    def test_gerar_chave_acesso(self):
        """Testa geração de chave de acesso"""
        chave = gerar_chave_acesso(100, 1)
        assert len(chave) == 44
        # A chave contém dígitos e espaços, verificamos o tamanho
        assert len(chave.strip()) > 0