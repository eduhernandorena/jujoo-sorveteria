# Serviço de Relatórios
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from src.utils.helpers import formatar_data_simples, formatar_mes, mes_extenso
from src.services.venda_service import venda_service
from src.services.compra_service import compra_service
from src.services.caixa_service import caixa_service
from src.services.estoque_service import estoque_service
from src.services.producao_service import producao_service


class RelatorioService:
    """Serviço para gerar relatórios"""
    
    def relatorio_vendas(self, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> Dict[str, Any]:
        """Gera relatório de vendas"""
        vendas = venda_service.listar()
        
        if data_inicio:
            vendas = [v for v in vendas if formatar_data_simples(datetime.fromisoformat(v.data)) >= data_inicio]
        if data_fim:
            vendas = [v for v in vendas if formatar_data_simples(datetime.fromisoformat(v.data)) <= data_fim]
        
        total_vendido = sum(v.total for v in vendas)
        total_desconto = sum(v.desconto_total for v in vendas)
        quantidade_vendas = len(vendas)
        
        # Agrupar por forma de pagamento
        por_forma_pagamento = {}
        for v in vendas:
            forma = v.forma_pagamento
            if forma not in por_forma_pagamento:
                por_forma_pagamento[forma] = {"quantidade": 0, "total": 0}
            por_forma_pagamento[forma]["quantidade"] += 1
            por_forma_pagamento[forma]["total"] += v.total
        
        return {
            "periodo": {"inicio": data_inicio, "fim": data_fim},
            "resumo": {
                "quantidade_vendas": quantidade_vendas,
                "total_vendido": round(total_vendido, 2),
                "total_desconto": round(total_desconto, 2),
                "ticket_medio": round(total_vendido / quantidade_vendas, 2) if quantidade_vendas > 0 else 0
            },
            "por_forma_pagamento": por_forma_pagamento,
            "vendas": [v.model_dump() for v in vendas]
        }
    
    def relatorio_compras(self, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> Dict[str, Any]:
        """Gera relatório de compras"""
        compras = compra_service.listar()
        
        if data_inicio:
            compras = [c for c in compras if formatar_data_simples(datetime.fromisoformat(c.data)) >= data_inicio]
        if data_fim:
            compras = [c for c in compras if formatar_data_simples(datetime.fromisoformat(c.data)) <= data_fim]
        
        total_comprado = sum(c.total for c in compras)
        quantidade_compras = len(compras)
        
        # Agrupar por fornecedor
        por_fornecedor = {}
        for c in compras:
            fornecedor = c.fornecedor
            if fornecedor not in por_fornecedor:
                por_fornecedor[fornecedor] = {"quantidade": 0, "total": 0}
            por_fornecedor[fornecedor]["quantidade"] += 1
            por_fornecedor[fornecedor]["total"] += c.total
        
        return {
            "periodo": {"inicio": data_inicio, "fim": data_fim},
            "resumo": {
                "quantidade_compras": quantidade_compras,
                "total_comprado": round(total_comprado, 2),
                "media_por_compra": round(total_comprado / quantidade_compras, 2) if quantidade_compras > 0 else 0
            },
            "por_fornecedor": por_fornecedor,
            "compras": [c.model_dump() for c in compras]
        }
    
    def relatorio_lucratividade(self, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> Dict[str, Any]:
        """Gera relatório de lucratividade"""
        # Obter dados
        dados_vendas = self.relatorio_vendas(data_inicio, data_fim)
        dados_compras = self.relatorio_compras(data_inicio, data_fim)
        
        total_vendas = dados_vendas["resumo"]["total_vendido"]
        total_compras = dados_compras["resumo"]["total_comprado"]
        
        # Lucro bruto = vendas - custo das mercadorias vendidas
        # Simplificação: usamos compras como custo
        lucro_bruto = total_vendas - total_compras
        
        # Margem de lucro
        margem = (lucro_bruto / total_vendas * 100) if total_vendas > 0 else 0
        
        return {
            "periodo": {"inicio": data_inicio, "fim": data_fim},
            "resumo": {
                "receita_vendas": total_vendas,
                "custo_mercadorias": total_compras,
                "lucro_bruto": round(lucro_bruto, 2),
                "margem_percentual": round(margem, 2)
            },
            "analise": self._analisar_lucratividade(lucro_bruto, margem)
        }
    
    def _analisar_lucratividade(self, lucro: float, margem: float) -> str:
        """Analisa a lucratividade"""
        if margem > 30:
            return "Excelente - Margem muito acima do mercado"
        elif margem > 20:
            return "Boa - Margem acima do esperado"
        elif margem > 10:
            return "Regular - Margem dentro do esperado"
        elif margem > 0:
            return "Baixa - Margem apertada, atenção aos custos"
        else:
            return "Negativa - Prejuízo, revisar custos"
    
    def relatorio_estoque(self) -> Dict[str, Any]:
        """Gera relatório de estoque"""
        estoque = estoque_service.get_resumo_estoque()
        estoque_baixo = estoque_service.buscar_estoque_baixo()
        
        return {
            "resumo": {
                "total_itens": estoque["total_itens"],
                "estoque_baixo": estoque["estoque_baixo"],
                "valor_total": estoque["valor_total"]
            },
            "itens_estoque_baixo": [item.model_dump() for item in estoque_baixo],
            "todos_itens": estoque["itens"]
        }
    
    def relatorio_caixa(self, data: Optional[str] = None, mes: Optional[str] = None) -> Dict[str, Any]:
        """Gera relatório de caixa"""
        if mes:
            fechamento = caixa_service.fazer_fechamento_mensal(mes)
        else:
            fechamento = caixa_service.fazer_fechamento_diario(data)
        
        return {
            "periodo": mes or data or formatar_data_simples(datetime.now()),
            "entradas": {
                "dinheiro": fechamento.entrada_dinheiro,
                "pix": fechamento.entrada_pix,
                "cartao_credito": fechamento.entrada_cartao_credito,
                "cartao_debito": fechamento.entrada_cartao_debito,
                "total": fechamento.total_entradas
            },
            "saidas": {
                "dinheiro": fechamento.saida_dinheiro,
                "pix": fechamento.saida_pix,
                "cartao_credito": fechamento.saida_cartao_credito,
                "cartao_debito": fechamento.saida_cartao_debito,
                "total": fechamento.total_saidas
            },
            "saldo": fechamento.saldo,
            "status": fechamento.status
        }
    
    def relatorio_producao(self, data: Optional[str] = None) -> Dict[str, Any]:
        """Gera relatório de produção"""
        if data:
            producoes = producao_service.listar(data=data)
        else:
            producoes = producao_service.get_producoes_do_dia()
        
        total_produzido = sum(p.total_itens for p in producoes)
        
        # Agrupar por produto
        por_produto = {}
        for p in producoes:
            for item in p.itens:
                if item.produto_nome not in por_produto:
                    por_produto[item.produto_nome] = 0
                por_produto[item.produto_nome] += item.quantidade
        
        return {
            "data": data or formatar_data_simples(datetime.now()),
            "resumo": {
                "quantidade_producoes": len(producoes),
                "total_itens": total_produzido
            },
            "por_produto": por_produto,
            "producoes": [p.model_dump() for p in producoes]
        }
    
    def dashboard(self) -> Dict[str, Any]:
        """Retorna dados para dashboard"""
        return {
            "vendas": {
                "do_dia": venda_service.get_total_vendas_do_dia(),
                "quantidade": len(venda_service.get_vendas_do_dia())
            },
            "compras": {
                "do_dia": compra_service.get_total_compras_do_dia()
            },
            "caixa": {
                "saldo_atual": caixa_service.get_saldo_atual(),
                "saldo_do_dia": caixa_service.get_saldo_do_dia()
            },
            "estoque": {
                "itens": estoque_service.get_resumo_estoque()["total_itens"],
                "estoque_baixo": estoque_service.get_resumo_estoque()["estoque_baixo"]
            },
            "producao": {
                "do_dia": producao_service.get_total_produzido_do_dia()
            }
        }


# Instância global
relatorio_service = RelatorioService()