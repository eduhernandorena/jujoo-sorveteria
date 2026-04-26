# Serviço de Caixa
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from src.models.caixa import MovimentoCaixa, MovimentoCaixaCreate, MovimentoCaixaResponse, FechamentoDiario, FechamentoMensal
from src.repositories.arquivo_repo import ArquivoRepositorio
from src.core.config import ARQUIVO_CAIXA
from src.core.constants import TIPO_ENTRADA, TIPO_SAIDA
from src.utils.logger import logger
from src.utils.helpers import gerar_id, formatar_data_simples, formatar_mes


class CaixaService:
    """Serviço para gerenciar caixa"""
    
    def __init__(self):
        self.repo = ArquivoRepositorio(ARQUIVO_CAIXA, dict)
    
    def _to_response(self, movimento: dict) -> MovimentoCaixaResponse:
        """Converte movimento para response"""
        return MovimentoCaixaResponse(
            id=movimento["id"],
            data=movimento.get("data"),
            tipo=movimento["tipo"],
            valor=movimento["valor"],
            origem=movimento["origem"],
            descricao=movimento["descricao"],
            referencia_id=movimento.get("referencia_id"),
            forma_pagamento=movimento.get("forma_pagamento", "dinheiro")
        )
    
    def criar_movimento(self, dados: MovimentoCaixaCreate) -> MovimentoCaixaResponse:
        """Cria novo movimento de caixa"""
        movimento_dict = {
            "id": gerar_id("mov"),
            "tipo": dados.tipo,
            "valor": dados.valor,
            "origem": dados.origem,
            "descricao": dados.descricao,
            "referencia_id": dados.referencia_id,
            "forma_pagamento": dados.forma_pagamento
        }
        movimento = self.repo.criar(movimento_dict)
        logger.info(f"Movimento criado: {dados.tipo} - R$ {dados.valor}")
        return self._to_response(movimento)
    
    def listar_movimentos(self, data: Optional[str] = None, tipo: Optional[str] = None) -> List[MovimentoCaixaResponse]:
        """Lista movimentos de caixa"""
        movimentos = self.repo.listar()
        
        if data:
            movimentos = [m for m in movimentos if formatar_data_simples(datetime.fromisoformat(m.get("data", ""))) == data]
        if tipo:
            movimentos = [m for m in movimentos if m.get("tipo") == tipo]
        
        return [self._to_response(m) for m in movimentos]
    
    def get_saldo_atual(self) -> float:
        """Retorna saldo atual do caixa"""
        movimentos = self.repo.listar()
        saldo = 0
        for m in movimentos:
            if m.get("tipo") == TIPO_ENTRADA:
                saldo += m.get("valor", 0)
            else:
                saldo -= m.get("valor", 0)
        return round(saldo, 2)
    
    def get_saldo_do_dia(self) -> float:
        """Retorna saldo do dia"""
        data_atual = formatar_data_simples(datetime.now())
        movimentos = self.repo.listar()
        saldo = 0
        for m in movimentos:
            data_mov = formatar_data_simples(datetime.fromisoformat(m.get("data", "")))
            if data_mov == data_atual:
                if m.get("tipo") == TIPO_ENTRADA:
                    saldo += m.get("valor", 0)
                else:
                    saldo -= m.get("valor", 0)
        return round(saldo, 2)
    
    def fazer_fechamento_diario(self, data: Optional[str] = None) -> FechamentoDiario:
        """Faz fechamento diário"""
        data_ref = data or formatar_data_simples(datetime.now())
        movimentos = [m for m in self.repo.listar() 
                     if formatar_data_simples(datetime.fromisoformat(m.get("data", ""))) == data_ref]
        
        entrada_dinheiro = 0
        entrada_pix = 0
        entrada_cartao_credito = 0
        entrada_cartao_debito = 0
        saida_dinheiro = 0
        saida_pix = 0
        saida_cartao_credito = 0
        saida_cartao_debito = 0
        
        for m in movimentos:
            valor = m.get("valor", 0)
            forma = m.get("forma_pagamento", "dinheiro")
            tipo = m.get("tipo")
            
            if tipo == TIPO_ENTRADA:
                if forma == "dinheiro":
                    entrada_dinheiro += valor
                elif forma == "pix":
                    entrada_pix += valor
                elif forma == "cartao_credito":
                    entrada_cartao_credito += valor
                elif forma == "cartao_debito":
                    entrada_cartao_debito += valor
            else:
                if forma == "dinheiro":
                    saida_dinheiro += valor
                elif forma == "pix":
                    saida_pix += valor
                elif forma == "cartao_credito":
                    saida_cartao_credito += valor
                elif forma == "cartao_debito":
                    saida_cartao_debito += valor
        
        total_entradas = entrada_dinheiro + entrada_pix + entrada_cartao_credito + entrada_cartao_debito
        total_saidas = saida_dinheiro + saida_pix + saida_cartao_credito + saida_cartao_debito
        
        fechamento = FechamentoDiario(
            id=gerar_id("fd"),
            data=data_ref,
            entrada_dinheiro=round(entrada_dinheiro, 2),
            entrada_pix=round(entrada_pix, 2),
            entrada_cartao_credito=round(entrada_cartao_credito, 2),
            entrada_cartao_debito=round(entrada_cartao_debito, 2),
            saida_dinheiro=round(saida_dinheiro, 2),
            saida_pix=round(saida_pix, 2),
            saida_cartao_credito=round(saida_cartao_credito, 2),
            saida_cartao_debito=round(saida_cartao_debito, 2),
            total_entradas=round(total_entradas, 2),
            total_saidas=round(total_saidas, 2),
            saldo=round(total_entradas - total_saidas, 2),
            status="fechado",
            data_fechamento=datetime.now()
        )
        
        logger.info(f"Fechamento diário {data_ref}: R$ {fechamento.saldo}")
        return fechamento
    
    def fazer_fechamento_mensal(self, mes: Optional[str] = None) -> FechamentoMensal:
        """Faz fechamento mensal"""
        mes_ref = mes or formatar_mes(datetime.now())
        movimentos = self.repo.listar()
        
        entrada_dinheiro = 0
        entrada_pix = 0
        entrada_cartao_credito = 0
        entrada_cartao_debito = 0
        saida_dinheiro = 0
        saida_pix = 0
        saida_cartao_credito = 0
        saida_cartao_debito = 0
        
        for m in movimentos:
            data_mov = datetime.fromisoformat(m.get("data", ""))
            if formatar_mes(data_mov) == mes_ref:
                valor = m.get("valor", 0)
                forma = m.get("forma_pagamento", "dinheiro")
                tipo = m.get("tipo")
                
                if tipo == TIPO_ENTRADA:
                    if forma == "dinheiro":
                        entrada_dinheiro += valor
                    elif forma == "pix":
                        entrada_pix += valor
                    elif forma == "cartao_credito":
                        entrada_cartao_credito += valor
                    elif forma == "cartao_debito":
                        entrada_cartao_debito += valor
                else:
                    if forma == "dinheiro":
                        saida_dinheiro += valor
                    elif forma == "pix":
                        saida_pix += valor
                    elif forma == "cartao_credito":
                        saida_cartao_credito += valor
                    elif forma == "cartao_debito":
                        saida_cartao_debito += valor
        
        total_entradas = entrada_dinheiro + entrada_pix + entrada_cartao_credito + entrada_cartao_debito
        total_saidas = saida_dinheiro + saida_pix + saida_cartao_credito + saida_cartao_debito
        
        fechamento = FechamentoMensal(
            id=gerar_id("fm"),
            mes=mes_ref,
            entrada_dinheiro=round(entrada_dinheiro, 2),
            entrada_pix=round(entrada_pix, 2),
            entrada_cartao_credito=round(entrada_cartao_credito, 2),
            entrada_cartao_debito=round(entrada_cartao_debito, 2),
            saida_dinheiro=round(saida_dinheiro, 2),
            saida_pix=round(saida_pix, 2),
            saida_cartao_credito=round(saida_cartao_credito, 2),
            saida_cartao_debito=round(saida_cartao_debito, 2),
            total_entradas=round(total_entradas, 2),
            total_saidas=round(total_saidas, 2),
            saldo=round(total_entradas - total_saidas, 2),
            status="fechado",
            data_fechamento=datetime.now()
        )
        
        logger.info(f"Fechamento mensal {mes_ref}: R$ {fechamento.saldo}")
        return fechamento


# Instância global
caixa_service = CaixaService()