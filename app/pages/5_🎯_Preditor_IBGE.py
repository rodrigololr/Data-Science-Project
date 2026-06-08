"""Pagina 5 - Preditor de Risco Real (Poisson + IBGE)."""
import sys
from pathlib import Path
import joblib
import json

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from predictor import (
    SEXOS, DIAS, LOCAIS,
    idade_para_faixa, hora_para_grupo, mes_para_grupo,
    color_for_class, label_for_class
)

# === Funções de Carga ===
@st.cache_resource
def load_poisson_model():
    return joblib.load("models/preditor_poisson_final.joblib")

@st.cache_resource
def load_poisson_meta():
    with open("models/preditor_poisson_final_meta.json") as f:
        return json.load(f)

# === Configuração da Página ===
st.set_page_config(page_title="Preditor Risco Real", page_icon="🎯", layout="wide")

st.title("🎯 Preditor de Risco Real — Maceió (IBGE)")
st.markdown(
    """
    Esta é uma versão aprimorada do preditor original. Ela utiliza **Regressão de Poisson** 
    para calcular a **Taxa de Risco Real** (crimes por 100 mil habitantes), cruzando o 
    histórico da polícia com a população do bairro (**Censo IBGE 2022**).
    """
)

# === Disclaimer ===
st.warning(
    "**Aviso:** Este modelo prevê a **densidade de crimes** para o seu perfil. "
    "Diferente da versão original, aqui o tamanho da população do bairro é levado em conta, "
    "revelando o risco relativo real de vitimização."
)

model = load_poisson_model()
meta = load_poisson_meta()

# === Formulário (Idêntico ao Original) ===
with st.form("preditor_ibge"):
    c1, c2, c3 = st.columns(3)
    with c1:
        sexo = st.radio("Sexo", SEXOS, index=0)
        idade = st.slider("Idade", 0, 100, 25)
        bairro = st.selectbox("Bairro do fato", meta['bairros_disponiveis'], index=0)
    with c2:
        dia_semana = st.selectbox("Dia da semana", DIAS, index=5)
        hora = st.slider("Hora do fato (0-23)", 0, 23, 22)
    with c3:
        grupo_local = st.selectbox("Local do fato", LOCAIS, index=2)
        mes = st.slider("Mês", 1, 12, 6)

    submit = st.form_submit_button("Calcular Risco Real", type="primary", use_container_width=True)

if submit:
    # Preparar entrada para o modelo Poisson
    input_df = pd.DataFrame([{
        'sexo_input': sexo,
        'faixa_input': idade_para_faixa(idade),
        'bairro_input': bairro.strip().upper(),
        'dia_input': dia_semana,
        'local_input': grupo_local,
        'hora_input': hora_para_grupo(hora),
        'mes_input': mes_para_grupo(mes)
    }])
    
    # Predição da Taxa
    taxa_pred = float(model.predict(input_df)[0])
    taxa_pred = max(0, taxa_pred)
    
    # Classificação baseada na média da cidade
    media = meta['media_cidade_taxa']
    if taxa_pred < media:
        classe = "baixa"
    elif taxa_pred < media * 3:
        classe = "media"
    else:
        classe = "alta"
        
    cor = color_for_class(classe)
    label = label_for_class(classe)

    st.divider()
    st.subheader("Resultado do Risco Real")
    
    col_res1, col_res2 = st.columns([1, 2])
    
    with col_res1:
        st.markdown(
            f"""
            <div style="background:{cor}; padding:40px; border-radius:15px; text-align:center;">
                <h1 style="color:white; margin:0;">{label}</h1>
                <p style="color:white; margin-top:10px;">risco relativo de CVLI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_res2:
        # Gauge de Taxa
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = taxa_pred,
            title = {'text': "Taxa Prevista (Crimes/100k hab)"},
            gauge = {
                'axis': {'range': [0, max(taxa_pred * 1.5, media * 5)]},
                'bar': {'color': cor},
                'steps': [
                    {'range': [0, media], 'color': "#e8f5e9"},
                    {'range': [media, media * 3], 'color': "#fff3e0"},
                    {'range': [media * 3, 1000], 'color': "#ffebee"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': media
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"### Seu Risco Relativo: **{taxa_pred / media:.2f}x** a média de Maceió")
    st.write(f"- **Média de Maceió:** {media:.2f} crimes / 100k hab por ano.")
    st.write(f"- **Sua Taxa Estimada:** {taxa_pred:.2f} crimes / 100k hab por ano.")

    st.divider()
    
    # Comparação entre Bairros para o MESMO perfil
    st.subheader("Comparativo Geográfico")
    st.markdown("Como o risco para o seu perfil demográfico/temporal muda em outros bairros?")
    
    bairros_comp = meta['bairros_disponiveis']
    df_comp = pd.DataFrame([
        {
            'sexo_input': sexo,
            'faixa_input': idade_para_faixa(idade),
            'bairro_input': b.strip().upper(),
            'dia_input': dia_semana,
            'local_input': grupo_local,
            'hora_input': hora_para_grupo(hora),
            'mes_input': mes_para_grupo(mes)
        } for b in bairros_comp
    ])
    df_comp['taxa'] = model.predict(df_comp)
    df_comp['bairro_display'] = bairros_comp
    
    top_bairros = df_comp.sort_values('taxa', ascending=False).head(15)
    
    fig_bar = go.Figure(go.Bar(
        x=top_bairros['bairro_display'],
        y=top_bairros['taxa'],
        marker_color='indianred',
        text=top_bairros['taxa'].round(1),
        textposition='auto',
    ))
    fig_bar.update_layout(title="Top 15 Bairros com maior taxa para este Perfil", xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.caption(
    f"Modelo: Poisson Regression (XGBoost) · Denominador: População IBGE 2022 · "
    f"Features: Sexo, Faixa Etária, Bairro, Dia da Semana, Turno, Local, Trimestre."
)
