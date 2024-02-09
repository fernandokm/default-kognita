"""Contém funções utilizadas para o preprocessamento dos dados.

Essas funções são explicadas no notebook 2_treinamento.ipynb e foram desenvolvidas
a partir da análise de dados.
"""

import re

import numpy as np
import pandas as pd

# Colunas utilizadas para o cálculo de qtd_indicadores_zero
# na função count_zeros
zero_cols = [
    "valor_vencido",
    "default_3months",
    "quant_protestos",
    "valor_protestos",
    "quant_acao_judicial",
    "dividas_vencidas_valor",
    "dividas_vencidas_qtd",
    "acao_judicial_valor",
    "falencia_concordata_qtd",
]


def fix_amount(data: pd.DataFrame) -> pd.DataFrame:
    """Corrige erros em colunas de quantidade/valor"""

    pairs = [
        ("quant_protestos", "valor_protestos"),
        ("dividas_vencidas_qtd", "dividas_vencidas_valor"),
        ("quant_acao_judicial", "acao_judicial_valor"),
    ]

    data = data.copy()
    for amount_col, value_col in pairs:
        if amount_col in data.columns and value_col in data.columns:
            invalid = (data[amount_col] == 0) & (data[value_col] != 0)
            data.loc[invalid, amount_col] = np.nan
    return data


def parse_payment(x: float | str) -> dict:
    """Converte a forma de pagamento para uma representação estruturada.

    Retorna um dicionário com as seguintes variáveis:
        primeira_parcela (int): o número de dias até a primeira parcela
        ultima_parcela (int): o número de dias até a última parcela
        qtd_parcelas (int): o número de parcelas
        is_boleto (int): indica se o pagamento será feito em boleto
    """

    if pd.isna(x):
        return {
            "primeira_parcela": np.nan,
            "ultima_parcela": np.nan,
            "qtd_parcelas": np.nan,
            "is_boleto": np.nan,
        }
    assert isinstance(x, str)

    is_boleto = x.startswith("boleto")
    if is_boleto:
        x = x.removeprefix("boleto").strip()

    if x == "sem pagamento":
        payment_dates = []
    elif x == "a vista":
        payment_dates = [0]
    elif m := re.fullmatch(r"(\d+(?:[/,]\d+)*) ?(?:dias|dd)?", x):
        # Identifica formas de pagamento nos seguintes formatos:
        # - 10/20/30
        # - 10,20,30
        # seguido, opcionalmente, de "dias" ou "dd"
        payment_dates = [int(val) for val in re.split(r"[/,]", m.group(1))]
    elif m := re.fullmatch(r"(\d+) ?(?:x|vezes), ?1a[.,] (\d+)dd", x):
        # Identifica formas de pagamento nos seguintes formatos:
        # - 10x, 1a. 30dd
        # - 10 vezes, 1a. 30dd
        num = int(m.group(1))
        period = int(m.group(2))
        payment_dates = [period * (i + 1) for i in range(num)]
    elif m := re.fullmatch(r"(\d+)\+(\d+)x - (\d+)/(\d+)", x):
        # Identifica formas de pagamento nos seguintes formatos:
        # - 90+10x - 30/30
        first = int(m.group(1))
        num = int(m.group(2))
        period = int(m.group(3))
        payment_dates = [first + period * i for i in range(num + 1)]
    elif m := re.fullmatch(r"(\d+)x(?: \(.*\))?", x):
        # Identifica formas de pagamento nos seguintes formatos:
        # - 10x
        payment_dates = None
    else:
        print("Warning: Forma de pagamento não reconhecida:", x)
        return {
            "primeira_parcela": np.nan,
            "ultima_parcela": np.nan,
            "qtd_parcelas": np.nan,
            "is_boleto": np.nan,
        }

    return {
        "primeira_parcela": payment_dates[0] if payment_dates else np.nan,
        "ultima_parcela": payment_dates[-1] if payment_dates else np.nan,
        "qtd_parcelas": len(payment_dates) if payment_dates is not None else np.nan,
        "is_boleto": int(is_boleto),
    }


def convert_payment_column(data: pd.DataFrame) -> pd.DataFrame:
    """Converte a coluna de forma de pagamento para um formato estruturado"""
    # Criar um novo DataFrame manualmente é muito mais rápido do que
    # utilizar pd.Series.apply ou pd.Series.map
    return pd.DataFrame(
        data=map(parse_payment, data["forma_pagamento"]),
        index=data.index,
    )


def drop_column(data: pd.DataFrame) -> pd.DataFrame:
    """Utilizado para remover uma coluna.

    Retorna um dataframe vazio com os mesmos indices do DataFrame de entrada
    """
    return data.iloc[:, []]


def to_category(data: pd.DataFrame) -> pd.DataFrame:
    """Converte os dados de entrada para o tipo categórico do pandas"""
    return data.astype("category")


def count_zeros(data: pd.DataFrame) -> pd.DataFrame:
    # A variável é repetida aqui para garantir que essa o pickle funcione corretamente
    return pd.DataFrame({"qtd_indicadores_zero": data.loc[:, zero_cols].sum(axis=1)})
