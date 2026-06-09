"""Entry point do Streamlit - redireciona para Mapa."""
import streamlit as st

st.set_page_config(page_title="CVLI Alagoas", page_icon="🚨", layout="wide")

st.title("🚨 CVLI Alagoas — Análise Espaço-Temporal")
st.markdown(
    """
    Bem-vindo ao dashboard interativo do projeto final de Ciência de Dados (UFAL, 2026.1).
    
    Use o menu lateral para navegar entre as abas:
    - 🗺️ **Mapa** — visualização espaço-temporal de CVLI em Alagoas
    - 🎯 **Preditor (Densidade)** — classificador original por prevalência
    - 📊 **Sobre** — metodologia, limitações éticas, reprodutibilidade
    
    **Equipe:** 
    - Antônio Guilherme
    - Antônio Rodrigo
    - Sandro Gomes
    """
)
st.info("👈 Use o menu lateral para começar")
