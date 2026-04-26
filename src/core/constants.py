# Constantes do sistema Jujoo Sorveteria

# Status de operações
STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"
STATUS_CANCELADO = "cancelado"

# Tipos de movimento de caixa
TIPO_ENTRADA = "entrada"
TIPO_SAIDA = "saida"

# Origens de movimento
ORIGEM_VENDA = "venda"
ORIGEM_COMPRA = "compra"
ORIGEM_DESPESA = "despesa"
ORIGEM_RECEBIMENTO = "recebimento"
ORIGEM_PRODUCAO = "producao"

# Categorias de despesa
CATEGORIAS_DESPESA = [
    "fornecedor",
    "luz",
    "agua",
    "internet",
    "aluguel",
    "salario",
    "manutencao",
    "marketing",
    "outros"
]

# Categorias de produtos
CATEGORIAS = ["sorvete", "picole", "acai", "topping", "bebida", "acompanhamento"]

# Formas de pagamento
FORMAS_PAGAMENTO = ["dinheiro", "pix", "cartao_credito", "cartao_debito"]

# Unidades de medida
UNIDADES = {
    "kg": "Quilograma",
    "g": "Grama",
    "l": "Litro",
    "ml": "Mililitro",
    "un": "Unidade",
    "cx": "Caixa",
    "pc": "Peça"
}

# Impostos NFCe (percentuais)
ICMS_PADRAO = 18.0
PIS_PADRAO = 1.65
COFINS_PADRAO = 7.6