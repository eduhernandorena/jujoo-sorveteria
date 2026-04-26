# Funções utilitárias helpers
import uuid
import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional
from pathlib import Path


def gerar_id(prefixo: str = "") -> str:
    """Gera um ID único"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = str(uuid.uuid4())[:8]
    if prefixo:
        return f"{prefixo}_{timestamp}_{unique}"
    return f"{timestamp}_{unique}"


def formatar_moeda(valor: float) -> str:
    """Formata valor para padrão brasileiro"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data(data: datetime) -> str:
    """Formata data para padrão brasileiro"""
    return data.strftime("%d/%m/%Y %H:%M:%S")


def formatar_data_simples(data: datetime) -> str:
    """Formata data simples"""
    return data.strftime("%Y-%m-%d")


def formatar_mes(data: datetime) -> str:
    """Formata mês"""
    return data.strftime("%Y-%m")


def calcular_percentual(valor: float, total: float) -> float:
    """Calcula percentual"""
    if total == 0:
        return 0
    return round((valor / total) * 100, 2)


def validar_cnpj(cnpj: str) -> bool:
    """Valida CNPJ (simplificado)"""
    cnpj = cnpj.replace(".", "").replace("-", "").replace("/", "")
    return len(cnpj) == 14 and cnpj.isdigit()


def validar_cpf(cpf: str) -> bool:
    """Valida CPF (simplificado)"""
    cpf = cpf.replace(".", "").replace("-", "")
    return len(cpf) == 11 and cpf.isdigit()


def mes_extenso(mes: int) -> str:
    """Retorna nome do mês"""
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return meses[mes - 1] if 1 <= mes <= 12 else ""


def dias_mes(ano: int, mes: int) -> int:
    """Retorna número de dias de um mês"""
    if mes == 12:
        return 31
    next_month = date(ano, mes + 1, 1)
    return (next_month - date(ano, mes, 1)).days


def calcular_icms(valor: float, aliquota: float = 18.0) -> float:
    """Calcula valor do ICMS"""
    return round(valor * (aliquota / 100), 2)


def calcular_pis(valor: float, aliquota: float = 1.65) -> float:
    """Calcula valor do PIS"""
    return round(valor * (aliquota / 100), 2)


def calcular_cofins(valor: float, aliquota: float = 7.6) -> float:
    """Calcula valor do COFINS"""
    return round(valor * (aliquota / 100), 2)


def gerar_chave_acesso(numero: int, serie: int) -> str:
    """Gera chave de acesso para NFCe"""
    now = datetime.now()
    data_hora = now.strftime("%Y%m%d%H%M%S")
    codigo = f"{now.year}{now.month:02d}{now.day:02d}{numero:9d}{serie:3d}{data_hora}"
    return codigo.ljust(44, "0")[:44]