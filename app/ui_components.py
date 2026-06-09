"""
Reusable UI Components for the CVLI Dashboard.
Keeps the main page files focused on layout and flow.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Final

def render_risk_gauge(taxa: float, media: float, cor: str) -> None:
    """
    Renders a Plotly Gauge chart for risk visualization.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=taxa,
        title={'text': "Taxa Prevista (Crimes/100k hab do perfil)"},
        gauge={
            'axis': {'range': [0, max(taxa * 1.5, media * 5)]},
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

def render_risk_card(label: str, cor: str) -> None:
    """
    Renders the prominent visual card showing the risk category.
    """
    st.markdown(
        f"""
        <div style="background:{cor}; padding:40px; border-radius:15px; text-align:center;">
            <h1 style="color:white; margin:0;">{label}</h1>
            <p style="color:white; margin-top:10px;">risco relativo de CVLI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_technical_info(label: str, modelo_nome: str) -> None:
    """
    Renders the bottom technical interpretation section.
    """
    st.divider()
    st.markdown("### Interpretação")
    st.markdown(
        f"""
        - **Classe atribuída:** **{label}**
        - **Modelo usado:** {modelo_nome}
        - **Base:** Dados cruzados entre SSP/AL (Microdados CVLI) e IBGE (Censo 2022).
        """
    )

def color_for_class(classe: str) -> str:
    """Returns CSS hex color for risk level."""
    return {"baixa": "#2ca02c", "media": "#ff7f0e", "alta": "#d62728"}.get(classe, "#7f7f7f")

def label_for_class(classe: str) -> str:
    """Returns standardized UI label for risk level."""
    return {"baixa": "BAIXA", "media": "MEDIA", "alta": "ALTA"}.get(classe, "N/A")
