"""Pagina 2 - Preditor de risco CVLI em Maceio."""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from data_loader import load_model, load_meta, load_clean
from predictor import (
    SEXOS, DIAS, LOCAIS,
    make_input, predict, color_for_class, label_for_class,
)

st.set_page_config(page_title="Preditor CVLI", page_icon="🎯", layout="wide")
st.title("🎯 Preditor de Risco — CVLI em Maceió")
st.markdown(
    "Classifica um perfil em **3 classes** (baixa / média / alta) com base em "
    "14 anos de dados de Maceió. **Inclui bairro** para granularidade geográfica."
)

# === Disclaimer ===
st.warning(
    "**Aviso ético:** esta ferramenta produz um **ranking estatístico** baseado em dados "
    "históricos, NÃO uma predição individual de vitimização. "
    "CVLI é evento raro e a saída reflete concentração relativa do seu perfil no histórico. "
    "Modelo treinado **apenas com dados de Maceió**."
)

model = load_model()
meta = load_meta()

# === Bairros de Maceio (para selectbox) ===
df = load_clean()
maceio = df[df["CIDADE DO FATO"] == "Maceió"]
bairros_opcoes = (
    maceio["BAIRRO DO FATO"]
    .astype(str)
    .str.strip()
    .str.upper()
    .value_counts()
    .head(40)
    .index.sort_values()
    .tolist()
)

# === Form ===
with st.form("preditor"):
    c1, c2, c3 = st.columns(3)
    with c1:
        sexo = st.radio("Sexo", SEXOS, index=0)
        idade = st.slider("Idade", 0, 100, 25)
        bairro = st.selectbox("Bairro do fato", bairros_opcoes, index=0)
    with c2:
        dia_semana = st.selectbox("Dia da semana", DIAS, index=5)
        hora = st.slider("Hora do fato (0-23)", 0, 23, 22)
    with c3:
        grupo_local = st.selectbox("Local do fato", LOCAIS, index=2)
        mes = st.slider("Mês", 1, 12, 6)

    submit = st.form_submit_button("Calcular risco", type="primary", use_container_width=True)

if submit:
    X = make_input(sexo, idade, dia_semana, hora, grupo_local, mes, bairro)
    classe, probs = predict(model, X)
    cor = color_for_class(classe)
    label = label_for_class(classe)

    st.divider()
    st.subheader("Resultado")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(
            f"""
            <div style="background:{cor}; padding:40px; border-radius:15px; text-align:center;">
                <h1 style="color:white; margin:0;">{label}</h1>
                <p style="color:white; margin-top:10px;">chance de CVLI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown("**Probabilidades por classe:**")
        for c in ["baixa", "media", "alta"]:
            p = probs.get(c, 0)
            st.progress(min(p, 1.0), text=f"{c}: {p*100:.1f}%")

    st.divider()
    st.markdown("### Interpretação")
    st.markdown(
        f"""
        - **Classe atribuída:** **{label}**
        - **Modelo usado:** {meta['modelo']}
        - **F1 macro (validação cruzada 5-fold):** {meta['f1_macro_cv']:.3f}
        - **Base de treino:** {meta['n_amostras_treino']:,} registros de Maceió
        - **Design do target:** rank contextual (raro=baixa, comum=alta) dentro do grupo demográfico
        """
    )

    with st.expander("Ver perfil enviado ao modelo"):
        st.dataframe(X, use_container_width=True)

st.divider()
st.caption(
    f"Modelo: {meta['modelo']} · Treinado em {meta['n_amostras_treino']:,} registros · "
    f"Features: {len(meta['features_num']) + len(meta['features_cat'])}"
)
