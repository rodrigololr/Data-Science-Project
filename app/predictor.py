"""Preditor wrapper - aplica modelo + calcula SHAP local."""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


# Faixas etarias (mesma discretizacao do NB01/NB04)
FAIXAS = ["0-11", "12-17", "18-24", "25-29", "30-39", "40-59", "60+"]
PERIODOS = ["Madrugada (0-5)", "Manha (6-11)", "Tarde (12-17)", "Noite (18-23)"]
DIAS = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
SEXOS = ["Masculino", "Feminino"]
LOCAIS = [
    "Ambiente interno", "Entorno de casa", "Espaco publico",
    "Area externa/isolada", "Outros",
]

# Classes canonicas (sempre nessa ordem em toda a doc/apresentacao)
CLASSES_CANONICAS = ["baixa", "media", "alta"]


@lru_cache(maxsize=1)
def _load_label_encoder():
    """Carrega o LabelEncoder usado no treino (com mapping correto)."""
    import joblib
    return joblib.load(MODELS_DIR / "label_encoder.joblib")


def _int_to_class(int_label: int) -> str:
    """Converte int (0/1/2) do modelo para nome canonico (baixa/media/alta).

    CRITICO: usa o LabelEncoder salvo, NAO um decoder hardcoded,
    porque sklearn LabelEncoder ordena ALFABETICAMENTE.
    Para ['alta','baixa','media'] -> 0=alta, 1=baixa, 2=media.
    """
    le = _load_label_encoder()
    return le.inverse_transform([int(int_label)])[0]


def _class_to_int(class_name: str) -> int:
    """Converte nome canonico para int usado pelo modelo."""
    le = _load_label_encoder()
    return int(le.transform([class_name])[0])


def idade_para_faixa(idade: int) -> str:
    if idade < 12:
        return "0-11"
    if idade < 18:
        return "12-17"
    if idade < 25:
        return "18-24"
    if idade < 30:
        return "25-29"
    if idade < 40:
        return "30-39"
    if idade < 60:
        return "40-59"
    return "60+"


def hora_para_periodo(hora: int) -> str:
    if hora < 6:
        return "Madrugada (0-5)"
    if hora < 12:
        return "Manha (6-11)"
    if hora < 18:
        return "Tarde (12-17)"
    return "Noite (18-23)"


def hora_para_grupo(hora: int) -> str:
    """Grupo de hora (Madrugada/Manha/Tarde/Noite)."""
    if hora < 6:
        return "Madrugada"
    if hora < 12:
        return "Manha"
    if hora < 18:
        return "Tarde"
    return "Noite"


def mes_para_grupo(mes: int) -> str:
    """Grupo de mes (T1/T2/T3/T4)."""
    if mes <= 3:
        return "T1"
    if mes <= 6:
        return "T2"
    if mes <= 9:
        return "T3"
    return "T4"


def make_input(
    sexo: str,
    idade: int,
    dia_semana: str,
    hora: int,
    grupo_local: str,
    mes: int = 6,
    bairro: str = "Benebdito Bentes",
) -> pd.DataFrame:
    """Constroi o DataFrame de 1 linha para predicao.

    Args:
        sexo: Masculino/Feminino
        idade: 0-100
        dia_semana: Segunda/Domingo
        hora: 0-23
        grupo_local: Espaco publico/Ambiente interno/etc
        mes: 1-12
        bairro: BAIRRO DO FATO em maiuscula (para match com modelo)
    """
    return pd.DataFrame([{
        "idade": idade,
        "hora": hora,
        "mes": mes,
        "SEXO DA VITIMA": sexo,
        "faixa_etaria": idade_para_faixa(idade),
        "periodo_dia": hora_para_periodo(hora),
        "dia_semana": dia_semana,
        "grupo_local": grupo_local,
        "hora_grupo": hora_para_grupo(hora),
        "mes_grupo": mes_para_grupo(mes),
        "bairro_norm": bairro.strip().upper(),
    }])


def predict(model, X: pd.DataFrame) -> tuple[str, dict]:
    """Retorna (classe_str, dict com probabilidades).

    IMPORTANTE: usa o LabelEncoder salvo para decodificar,
    garantindo que 0->'alta', 1->'baixa', 2->'media' (ordem alfabetica).
    """
    pred = model.predict(X)[0]
    classe = str(_int_to_class(pred))
    probs = model.predict_proba(X)[0]
    classes_int = model.classes_
    prob_dict = {_int_to_class(int(c)): float(p) for c, p in zip(classes_int, probs)}
    # Garantir chaves como str (nao np.str_)
    prob_dict = {str(k): v for k, v in prob_dict.items()}
    return classe, prob_dict


def color_for_class(classe: str) -> str:
    return {"baixa": "#2ca02c", "media": "#ff7f0e", "alta": "#d62728"}[classe]


def label_for_class(classe: str) -> str:
    return {"baixa": "BAIXA", "media": "MEDIA", "alta": "ALTA"}[classe]
