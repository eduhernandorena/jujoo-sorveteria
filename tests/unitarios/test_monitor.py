# Testes Unitários - Monitor
import pytest
from src.utils.monitor import MonitorRecursos


class TestMonitor:
    """Testes para monitor de recursos"""
    
    def setup_method(self):
        self.monitor = MonitorRecursos()
    
    def test_get_cpu_percent(self):
        """Testa obtenção de uso de CPU"""
        cpu = self.monitor.get_cpu_percent()
        assert cpu >= 0
    
    def test_get_memoria(self):
        """Testa obtenção de informações de memória"""
        mem = self.monitor.get_memoria()
        
        assert "rss_mb" in mem
        assert "vms_mb" in mem
        assert "percent" in mem
        assert mem["rss_mb"] > 0
    
    def test_get_disco(self):
        """Testa obtenção de informações de disco"""
        disco = self.monitor.get_disco()
        
        assert "total_gb" in disco
        assert "usado_gb" in disco
        assert "livre_gb" in disco
        assert "percent" in disco
    
    def test_get_info_sistema(self):
        """Testa obtenção de informações completas"""
        info = self.monitor.get_info_sistema()
        
        assert "timestamp" in info
        assert "cpu" in info
        assert "memoria" in info
        assert "disco" in info
        assert "processo" in info
    
    def test_get_status_simplificado(self):
        """Testa obtenção de status simplificado"""
        status = self.monitor.get_status_simplificado()
        
        assert "cpu_percent" in status
        assert "memoria_mb" in status
        assert "disco_percent" in status