"""Data loader centralizado para o dashboard Streamlit."""
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


@lru_cache(maxsize=1)
def load_clean():
    return pd.read_csv(DATA_DIR / "processed" / "cvli_clean.csv", low_memory=False)


@lru_cache(maxsize=1)
def load_municipios():
    return pd.read_csv(DATA_DIR / "geo" / "municipios_al.csv")


@lru_cache(maxsize=1)
def load_bairros_top5():
    return pd.read_csv(DATA_DIR / "geo" / "bairros_top5.csv")


@lru_cache(maxsize=1)
def load_agg_anual():
    return pd.read_csv(DATA_DIR / "processed" / "agg_anual_municipio.csv")


@lru_cache(maxsize=1)
def load_agg_mensal():
    df = pd.read_csv(DATA_DIR / "processed" / "agg_mensal_municipio.csv")
    df["ano_mes"] = pd.to_datetime(df["ano_mes"])
    return df


@lru_cache(maxsize=1)
def load_agg_trimestral():
    return pd.read_csv(DATA_DIR / "processed" / "agg_trimestral_municipio.csv")


@lru_cache(maxsize=1)
def load_agg_semestral():
    return pd.read_csv(DATA_DIR / "processed" / "agg_semestral_municipio.csv")


@lru_cache(maxsize=1)
def load_agg_bairro():
    return pd.read_csv(DATA_DIR / "processed" / "agg_bairro_top5.csv")


@lru_cache(maxsize=1)
def load_populacao_maceio():
    return pd.read_csv(DATA_DIR / "geo" / "populacao_maceio_bairros.csv")


@lru_cache(maxsize=1)
def load_model():
    import joblib
    return joblib.load(MODELS_DIR / "preditor_maceio.joblib")


@lru_cache(maxsize=1)
def load_meta():
    with open(MODELS_DIR / "preditor_meta.json") as f:
        return json.load(f)


def get_agg_for_window(janela: str):
    """Retorna agregacao adequada para a janela temporal escolhida."""
    if janela == "Mes":
        return load_agg_mensal(), "ano_mes"
    elif janela == "Trimestre":
        return load_agg_trimestral(), "trimestre"
    elif janela == "Semestre":
        return load_agg_semestral(), ["ano", "semestre"]
    else:  # Ano
        return load_agg_anual(), "ano"
