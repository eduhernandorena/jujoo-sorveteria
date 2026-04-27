# Configurações centrais do sistema Jujoo Sorveteria

import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Garante que diretórios existam
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Configurações da API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
API_TITLE = "Jujoo Sorveteria API"
API_VERSION = "1.0.0"
CORS_ORIGINS = [
    origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()
]

# Configurações de persistência
ARQUIVO_PRODUTOS = DATA_DIR / "produtos.json"
ARQUIVO_MATERIAS_PRIMAS = DATA_DIR / "materias_primas.json"
ARQUIVO_VENDAS = DATA_DIR / "vendas.json"
ARQUIVO_COMPRAS = DATA_DIR / "compras.json"
ARQUIVO_PRODUCAO = DATA_DIR / "producao.json"
ARQUIVO_CAIXA = DATA_DIR / "caixa.json"
ARQUIVO_NFCE = DATA_DIR / "nfce.json"

# Configurações de log
LOG_FILE = LOGS_DIR / "jujoo.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Dados do emitente (para NFCe)
EMITENTE = {
    "nome": "Jujoo Sorveteria",
    "cnpj": "12.345.678/0001-90",
    "endereco": "Rua dos Sorvetes, 123 - Centro",
    "cidade": "São Paulo",
    "estado": "SP",
    "telefone": "(11) 99999-9999",
    "inscricao_estadual": "123456789"
}

# Configurações de estoque
ESTOQUE_MINIMO_PADRAO = 10  # Quantidade mínima padrão

# Formas de pagamento
FORMAS_PAGAMENTO = ["dinheiro", "pix", "cartao_credito", "cartao_debito"]

# Categorias de produtos
CATEGORIAS = ["sorvete", "picole", "acai", "topping", "bebida", "acompanhamento"]
