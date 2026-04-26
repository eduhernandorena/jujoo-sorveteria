# Monitor de Recursos do Sistema
import psutil
import os
from datetime import datetime
from typing import Dict, Any
from src.utils.logger import logger


class MonitorRecursos:
    """Monitor de recursos do sistema"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
    
    def get_cpu_percent(self) -> float:
        """Retorna uso de CPU em percentual"""
        return self.process.cpu_percent(interval=0.1)
    
    def get_memoria(self) -> Dict[str, Any]:
        """Retorna informações de memória"""
        mem = self.process.memory_info()
        return {
            "rss_mb": round(mem.rss / 1024 / 1024, 2),
            "vms_mb": round(mem.vms / 1024 / 1024, 2),
            "percent": self.process.memory_percent()
        }
    
    def get_disco(self) -> Dict[str, Any]:
        """Retorna informações de disco"""
        try:
            disk = psutil.disk_usage('/')
            return {
                "total_gb": round(disk.total / (1024**3), 2),
                "usado_gb": round(disk.used / (1024**3), 2),
                "livre_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            }
        except Exception as e:
            logger.warning(f"Erro ao obter info disco: {e}")
            return {"error": "Não foi possível obter informações de disco"}
    
    def get_info_sistema(self) -> Dict[str, Any]:
        """Retorna informações completas do sistema"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": self.get_cpu_percent(),
                "count": psutil.cpu_count(),
                "count_logico": psutil.cpu_count(logical=True)
            },
            "memoria": self.get_memoria(),
            "disco": self.get_disco(),
            "processo": {
                "pid": self.process.pid,
                "threads": self.process.num_threads(),
                "arquivos_abertos": len(self.process.open_files())
            }
        }
    
    def get_status_simplificado(self) -> Dict[str, Any]:
        """Retorna status simplificado"""
        return {
            "cpu_percent": self.get_cpu_percent(),
            "memoria_mb": self.get_memoria()["rss_mb"],
            "disco_percent": self.get_disco().get("percent", 0)
        }


# Instância global do monitor
monitor = MonitorRecursos()


def get_status_recursos() -> Dict[str, Any]:
    """Função de conveniência para obter status"""
    return monitor.get_status_simplificado()


def get_info_completa() -> Dict[str, Any]:
    """Função de conveniência para obter info completa"""
    return monitor.get_info_sistema()