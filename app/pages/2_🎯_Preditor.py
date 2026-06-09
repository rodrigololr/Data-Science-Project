"""
Pagina 2 - Preditor de Risco Real em Maceió.
Production-grade modular version.
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from typing import Final, Any

import pandas as pd
import streamlit as st

# Path adjustment
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from data_loader import load_model, load_meta
from domain import SEXOS, DIAS, LOCAIS
from predictor import make_input, predict
from ai_engine import get_ai_explanation
from ui_components import (
    render_risk_gauge, render_risk_card, render_technical_info,
    color_for_class, label_for_class
)

# --- Configuration ---
AI_COOLDOWN: Final[int] = 1

st.set_page_config(page_title="Preditor Risco Real", page_icon="🎯", layout="wide")

def render_page_header() -> None:
    st.title("🎯 Preditor de Risco Real — Maceió")
    st.markdown(
        "Esta ferramenta utiliza **Regressão de Poisson** para calcular a **Taxa de Risco Real** "
        "(crimes por 100 mil habitantes), cruzando o histórico da polícia com estimativas."
    )
    st.warning("**Aviso:** Este modelo prevê a densidade de crimes para o seu perfil.")

def handle_prediction(model: Any, meta: dict) -> None:
    with st.form("main_preditor_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            sexo = st.radio("Sexo", SEXOS)
            idade = st.slider("Idade", 0, 100, 25)
        with c2:
            dia_semana = st.selectbox("Dia da semana", DIAS, index=5)
            hora = st.slider("Hora do fato (0-23)", 0, 23, 22)
        with c3:
            grupo_local = st.selectbox("Local do fato", LOCAIS, index=2)
            bairro = st.selectbox("Bairro do fato", meta['bairros_disponiveis'])
            
        if st.form_submit_button("Calcular risco", type="primary", use_container_width=True):
            X_input = make_input(sexo, idade, dia_semana, hora, grupo_local, bairro)

            # Recalibração Relativa: Usa a média de referência do sexo selecionado
            medias = meta['media_cidade_taxa']
            if isinstance(medias, dict):
                media_referencia = medias.get(sexo, medias.get('Geral'))
            else:
                media_referencia = medias

            classe, taxa = predict(model, X_input, media_referencia)

            # Save state
            st.session_state.X = X_input
            st.session_state.taxa = taxa
            st.session_state.media_cidade = media_referencia
            st.session_state.classe = classe
            st.session_state.prediction_done = True
            
            profile_json = X_input.to_json()
            if st.session_state.get("last_profile_json") != profile_json:
                st.session_state.current_explanation = None
                st.session_state.last_profile_json = profile_json

def render_ai_section(model: Any, meta: dict) -> None:
    st.divider()
    st.subheader("🤖 Explicação da Inteligência Artificial")
    
    current_time = time.time()
    last_time = st.session_state.get("last_ai_request_time", 0)
    
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("✨ Gerar Explicação por IA", use_container_width=True):
            if (current_time - last_time) < AI_COOLDOWN:
                st.warning(f"Aguarde {int(AI_COOLDOWN - (current_time - last_time))}s.")
            else:
                with st.spinner("Consultando analista de segurança (Gemini)..."):
                    X = st.session_state.X
                    taxa = st.session_state.taxa
                    media_cidade = st.session_state.media_cidade
                    explanation = get_ai_explanation(model, X.to_json(), taxa, media_cidade)
                    st.session_state.current_explanation = explanation
                    st.session_state.last_ai_request_time = current_time
                    st.rerun()

    if st.session_state.get("current_explanation"):
        st.info(st.session_state.current_explanation)
    else:
        st.caption("Clique no botão acima para entender os fatores de risco deste perfil.")

# --- Execution ---
render_page_header()

model = load_model()
meta = load_meta()

handle_prediction(model, meta)

if st.session_state.get("prediction_done"):
    X = st.session_state.X
    taxa = st.session_state.taxa
    classe = st.session_state.classe
    media_cidade = st.session_state.media_cidade
    
    cor = color_for_class(classe)
    label = label_for_class(classe)

    st.divider()
    st.subheader("Resultado do Risco Real")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_risk_card(label, cor)
    with col2:
        render_risk_gauge(taxa, media_cidade, cor)

    st.markdown(f"### Seu Risco Relativo: **{taxa / media_cidade:.2f}x** a média do seu perfil na cidade")
    
    render_ai_section(model, meta)
    render_technical_info(label, meta['modelo'])
    
    with st.expander("Ver perfil enviado ao modelo"):
        st.dataframe(X, use_container_width=True)
