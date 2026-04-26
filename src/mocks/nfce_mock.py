# Mock de NFCe (Nota Fiscal de Consumidor Eletrônica)
from typing import List, Dict, Any
from datetime import datetime
from src.models.nfce import NFCe, ItemNFCe
from src.core.config import EMITENTE
from src.core.constants import ICMS_PADRAO, PIS_PADRAO, COFINS_PADRAO
from src.utils.helpers import gerar_chave_acesso, calcular_icms, calcular_pis, calcular_cofins
from src.utils.logger import logger


class MockNFCe:
    """Mock para emissão de NFCe"""
    
    def __init__(self):
        self.ultimo_numero = 0
        self.serie = 1
        self.nfces_emitidas = []
    
    def _proximo_numero(self) -> int:
        """Gera próximo número de NFCe"""
        self.ultimo_numero += 1
        return self.ultimo_numero
    
    def _gerar_danfe(self, nfce: NFCe) -> str:
        """Gera representação simplificada do DANFE"""
        linhas = []
        linhas.append("=" * 48)
        linhas.append(f"{EMITENTE['nome']:^48}")
        linhas.append(f"CNPJ: {EMITENTE['cnpj']}")
        linhas.append(f"{EMITENTE['endereco']}")
        linhas.append(f"{EMITENTE['cidade']} - {EMITENTE['estado']}")
        linhas.append("=" * 48)
        linhas.append(f"NFC-e N° {nfce.numero:06d}  Série {nfce.serie}")
        linhas.append(f"Data: {nfce.data_emissao.strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("-" * 48)
        linhas.append("ITEM  CÓDIGO       DESCRIÇÃO           QTD X VALOR")
        linhas.append("-" * 48)
        
        for i, item in enumerate(nfce.itens, 1):
            linhas.append(f"{i:3d}  {item.codigo[:10]:10} {item.descricao[:17]:17} {item.quantidade:4.0f} x {item.preco_unitario:6.2f}")
            linhas.append(f"       {item.total:>25.2f}")
        
        linhas.append("-" * 48)
        linhas.append(f"SUBTOTAL:                    R$ {nfce.subtotal:>10.2f}")
        if nfce.desconto > 0:
            linhas.append(f"DESCONTO:                    R$ {nfce.desconto:>10.2f}")
        linhas.append(f"TOTAL:                       R$ {nfce.total:>10.2f}")
        linhas.append("-" * 48)
        linhas.append(f"ICMS: R$ {nfce.valor_icms:>10.2f}  PIS: R$ {nfce.valor_pis:>8.2f}  COFINS: R$ {nfce.valor_cofins:>8.2f}")
        linhas.append("-" * 48)
        linhas.append(f"FORMA PAGTO: {nfce.forma_pagamento.upper()}")
        linhas.append("=" * 48)
        linhas.append(f"Chave: {nfce.chave_acesso[:44]}")
        linhas.append("=" * 48)
        linhas.append("Consulte pela chave de acesso em")
        linhas.append("www.nfe.fazenda.gov.br")
        
        return "\n".join(linhas)
    
    def emitir(self, venda_id: str, itens: List[Dict[str, Any]], 
                forma_pagamento: str, total: float, desconto: float = 0) -> NFCe:
        """Emite NFCe para uma venda"""
        logger.info(f"Emitindo NFCe para venda {venda_id}")
        
        numero = self._proximo_numero()
        chave = gerar_chave_acesso(numero, self.serie)
        
        # Criar itens da NFCe
        itens_nfce = []
        subtotal = 0
        valor_icms = 0
        valor_pis = 0
        valor_cofins = 0
        
        for item in itens:
            total_item = item['quantidade'] * item['preco_unitario']
            subtotal += total_item
            
            icms = calcular_icms(total_item, ICMS_PADRAO)
            pis = calcular_pis(total_item, PIS_PADRAO)
            cofins = calcular_cofins(total_item, COFINS_PADRAO)
            
            valor_icms += icms
            valor_pis += pis
            valor_cofins += cofins
            
            itens_nfce.append(ItemNFCe(
                codigo=item['produto_id'],
                descricao=item['produto_nome'],
                quantidade=item['quantidade'],
                unidade="un",
                preco_unitario=item['preco_unitario'],
                total=total_item,
                aliquota_icms=ICMS_PADRAO,
                aliquota_pis=PIS_PADRAO,
                aliquota_cofins=COFINS_PADRAO
            ))
        
        # Criar NFCe
        nfce = NFCe(
            id=f"nfce_{numero}",
            numero=numero,
            serie=self.serie,
            chave_acesso=chave,
            itens=itens_nfce,
            subtotal=subtotal,
            desconto=desconto,
            total=total - desconto,
            valor_icms=valor_icms,
            valor_pis=valor_pis,
            valor_cofins=valor_cofins,
            forma_pagamento=forma_pagamento
        )
        
        # Gerar DANFE
        nfce.danfe = self._gerar_danfe(nfce)
        
        self.nfces_emitidas.append(nfce)
        logger.info(f"NFCe {numero} emitida com sucesso")
        
        return nfce
    
    def consultar(self, numero: int) -> NFCe:
        """Consulta NFCe por número"""
        for nfce in self.nfces_emitidas:
            if nfce.numero == numero:
                return nfce
        return None
    
    def cancelar(self, numero: int) -> bool:
        """Cancela NFCe"""
        nfce = self.consultar(numero)
        if nfce:
            nfce.status = "cancelado"
            logger.info(f"NFCe {numero} cancelada")
            return True
        return False
    
    def get_emitente(self) -> Dict[str, str]:
        """Retorna dados do emitente"""
        return EMITENTE.copy()


# Instância global
mock_nfce = MockNFCe()