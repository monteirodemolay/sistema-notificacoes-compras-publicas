import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "OF_id",
    "fornecedor",
    "data_emissao",
    "prazo_entrega",
    "data_entrega_real",
    "valor",
    "categoria",
]


def load_data(path: str) -> pd.DataFrame:
    """Carrega a base de Ordens de Fornecimento."""
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes na base: {missing}")
    return df


def preprocess_data(df: pd.DataFrame, training: bool = True) -> pd.DataFrame:
    """Padroniza datas, cria variáveis de prazo, atraso e prioridade operacional."""
    data = df.copy()

    for col in ["data_emissao", "prazo_entrega", "data_entrega_real"]:
        data[col] = pd.to_datetime(data[col], errors="coerce")

    data["valor"] = pd.to_numeric(data["valor"], errors="coerce")
    data["fornecedor"] = data["fornecedor"].fillna("Fornecedor_nao_informado")
    data["categoria"] = data["categoria"].fillna("Categoria_nao_informada")

    data["dias_prazo"] = (data["prazo_entrega"] - data["data_emissao"]).dt.days
    data["dias_para_vencer"] = (data["prazo_entrega"] - pd.Timestamp.today().normalize()).dt.days
    data["dias_entrega_real"] = (data["data_entrega_real"] - data["data_emissao"]).dt.days
    data["valor_log"] = np.log1p(data["valor"].clip(lower=0))

    if training:
        data = data.dropna(subset=["data_emissao", "prazo_entrega", "data_entrega_real", "valor"])
        data["atraso"] = (data["data_entrega_real"] > data["prazo_entrega"]).astype(int)
    else:
        data = data.dropna(subset=["data_emissao", "prazo_entrega", "valor"])

    data["dias_prazo"] = data["dias_prazo"].fillna(data["dias_prazo"].median())
    data["dias_para_vencer"] = data["dias_para_vencer"].fillna(data["dias_para_vencer"].median())
    data["dias_entrega_real"] = data["dias_entrega_real"].fillna(data["dias_prazo"])

    return data


def build_supplier_history(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula histórico de atraso por fornecedor sem expor dados pessoais."""
    hist = (
        df.groupby("fornecedor", as_index=False)
        .agg(
            taxa_atraso_fornecedor=("atraso", "mean"),
            total_of_fornecedor=("OF_id", "count"),
            valor_medio_fornecedor=("valor", "mean"),
        )
    )
    return hist


def add_supplier_history(df: pd.DataFrame, hist: pd.DataFrame) -> pd.DataFrame:
    data = df.merge(hist, on="fornecedor", how="left")
    data["taxa_atraso_fornecedor"] = data["taxa_atraso_fornecedor"].fillna(data["taxa_atraso_fornecedor"].mean())
    data["total_of_fornecedor"] = data["total_of_fornecedor"].fillna(1)
    data["valor_medio_fornecedor"] = data["valor_medio_fornecedor"].fillna(data["valor"].mean())
    return data


def prepare_dataset(path: str) -> pd.DataFrame:
    df = load_data(path)
    df = preprocess_data(df, training=True)
    hist = build_supplier_history(df)
    df = add_supplier_history(df, hist)
    return df
