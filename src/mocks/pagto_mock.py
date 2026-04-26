# Mock de Pagamentos
from typing import Dict, Any
from datetime import datetime
from src.utils.logger import logger


class MockPagamento:
    """Mock para processar pagamentos"""
    
    def __init__(self):
        self.transacoes = []
    
    def processar_dinheiro(self, valor: float, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento em dinheiro"""
        logger.info(f"Processando pagamento em dinheiro: R$ {valor}")
        return {
            "status": "aprovado",
            "transacao_id": f"din_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "valor": valor,
            "forma": "dinheiro",
            "data": datetime.now().isoformat(),
            "mensagem": "Pagamento em dinheiro recebido"
        }
    
    def processar_pix(self, valor: float, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento via PIX"""
        logger.info(f"Processando pagamento PIX: R$ {valor}")
        # Simula processamento
        return {
            "status": "aprovado",
            "transacao_id": f"pix_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "valor": valor,
            "forma": "pix",
            "chave_pix": dados.get("chave_pix", "jujoo@sorveteria.com"),
            "data": datetime.now().isoformat(),
            "mensagem": "Pagamento PIX aprovado",
            "qr_code": f"00020101021226360014br.gov.bcb.pix0014jujoo@sorveteria.com5204000053039865802BR5925JUJOO SORVETERIA LTDA6009SAO PAULO610701234-622405041234"
        }
    
    def processar_cartao_credito(self, valor: float, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento com cartão de crédito"""
        logger.info(f"Processando cartão de crédito: R$ {valor}")
        return {
            "status": "aprovado",
            "transacao_id": f"cc_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "valor": valor,
            "forma": "cartao_credito",
            "bandeira": dados.get("bandeira", "visa"),
            "parcelas": dados.get("parcelas", 1),
            "data": datetime.now().isoformat(),
            "mensagem": "Transação de crédito aprovada",
            "nsu": f"NSU{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
    
    def processar_cartao_debito(self, valor: float, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento com cartão de débito"""
        logger.info(f"Processando cartão de débito: R$ {valor}")
        return {
            "status": "aprovado",
            "transacao_id": f"cd_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "valor": valor,
            "forma": "cartao_debito",
            "bandeira": dados.get("bandeira", "visa"),
            "data": datetime.now().isoformat(),
            "mensagem": "Transação de débito aprovada",
            "nsu": f"NSU{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
    
    def processar(self, forma_pagamento: str, valor: float, dados: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa pagamento conforme forma"""
        dados = dados or {}
        
        processadores = {
            "dinheiro": self.processar_dinheiro,
            "pix": self.processar_pix,
            "cartao_credito": self.processar_cartao_credito,
            "cartao_debito": self.processar_cartao_debito
        }
        
        processador = processadores.get(forma_pagamento)
        if not processador:
            return {
                "status": "erro",
                "mensagem": f"Forma de pagamento inválida: {forma_pagamento}"
            }
        
        return processador(valor, dados)
    
    def estornar(self, transacao_id: str) -> Dict[str, Any]:
        """Estorna uma transação"""
        logger.info(f"Estornando transação: {transacao_id}")
        return {
            "status": "estornado",
            "transacao_id": transacao_id,
            "data": datetime.now().isoformat(),
            "mensagem": "Estorno realizado com sucesso"
        }


# Instância global
mock_pagamento = MockPagamento()