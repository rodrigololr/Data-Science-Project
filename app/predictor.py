"""
Core Predictor Module - Orchestrates Poisson model inference.
"""
from __future__ import annotations
from typing import Any, Tuple
import pandas as pd
import streamlit as st

from utils import idade_para_faixa, hora_para_grupo

def make_input(
    sexo: str,
    idade: int,
    dia_semana: str,
    hora: int,
    grupo_local: str,
    bairro: str = "BENEDITO BENTES",
) -> pd.DataFrame:
    """
    Constructs a single-row DataFrame formatted for Poisson Model input.
    """
    return pd.DataFrame([{
        "bairro_input": bairro.strip().upper(),
        "sexo_input": sexo,
        "faixa_input": idade_para_faixa(idade),
        "dia_input": dia_semana,
        "hora_input": hora_para_grupo(hora),
        "local_input": grupo_local,
    }])

def predict(model: Any, X: pd.DataFrame, media_cidade: float) -> Tuple[str, float]:
    """
    Performs inference and classifies risk based on city average.
    """
    try:
        taxa_pred = float(model.predict(X)[0])
        taxa_pred = max(0.0, taxa_pred)
        
        if taxa_pred < media_cidade:
            return "baixa", taxa_pred
        if taxa_pred < media_cidade * 3:
            return "media", taxa_pred
        return "alta", taxa_pred
        
    except Exception as e:
        st.error(f"Inference Failure: {str(e)}")
        return "indeterminado", 0.0
