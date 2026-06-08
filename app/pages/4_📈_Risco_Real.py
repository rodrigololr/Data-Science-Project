"""Pagina 4 - Analise de Risco Real (CVLI + IBGE)."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from data_loader import load_clean, load_populacao_maceio

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip().upper()
    # Remover acentos
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    return text

st.set_page_config(page_title="Risco Real Maceió", page_icon="📈", layout="wide")

st.title("📈 Análise de Risco Real — Maceió")
st.markdown(
    """
    Esta análise cruza os microdados de **CVLI** (o numerador) com a **população residente** 
    por bairro do **Censo IBGE 2022** (o denominador). 
    
    O objetivo é identificar onde a **taxa de criminalidade** (casos por 100 mil habitantes) 
    é maior, mitigando o viés de que bairros populosos são "mais perigosos" apenas pelo seu tamanho.
    """
)

# === Carregar Dados ===
df_full = load_clean()
df_pop = load_populacao_maceio()

# Filtrar apenas Maceió
df_cvli = df_full[df_full["CIDADE DO FATO"] == "Maceió"].copy()

# === Filtros ===
st.sidebar.header("Filtros")
anos_disp = sorted(df_cvli["ano"].unique().tolist())
anos_sel = st.sidebar.multiselect(
    "Selecione os Anos para Análise",
    options=anos_disp,
    default=anos_disp[-5:] if len(anos_disp) > 5 else anos_disp, # Ultimos 5 anos por padrao
    help="A taxa será anualizada com base na quantidade de anos selecionada."
)

if not anos_sel:
    st.error("Por favor, selecione ao menos um ano.")
    st.stop()

# Filtrar por anos
df_cvli_f = df_cvli[df_cvli["ano"].isin(anos_sel)].copy()
n_anos = len(anos_sel)

# === Processamento ===
# 1. Contar crimes por bairro no CVLI
df_cvli_f["bairro_norm"] = df_cvli_f["BAIRRO DO FATO"].apply(normalize_text)
crime_counts = df_cvli_f["bairro_norm"].value_counts().reset_index()
crime_counts.columns = ["bairro_norm", "total_crimes"]

# 2. Normalizar nomes na tabela de populacao
df_pop["bairro_norm"] = df_pop["bairro"].apply(normalize_text)

# 3. Merge
df_final = df_pop.merge(crime_counts, on="bairro_norm", how="left")
df_final["total_crimes"] = df_final["total_crimes"].fillna(0)

# 4. Calcular Taxas
# Taxa Anualizada = (Total Crimes / n_anos) / Populacao * 100.000
# Evitar divisao por zero para bairros desabitados (Mutange)
df_final = df_final[df_final["populacao_2022"] > 0].copy()

df_final["crimes_ano"] = df_final["total_crimes"] / n_anos
df_final["taxa_100k"] = (df_final["crimes_ano"] / df_final["populacao_2022"]) * 100000

# 5. Indice de Risco (em relacao a media da cidade)
media_maceio = df_final["taxa_100k"].mean()
df_final["risco_relativo"] = df_final["taxa_100k"] / media_maceio

# === Visualizacoes ===

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Bairros: Volume Absoluto")
    fig_abs = px.bar(
        df_final.nlargest(10, "total_crimes"),
        x="total_crimes",
        y="bairro",
        orientation="h",
        text_auto=True,
        labels={"total_crimes": "Total de Crimes", "bairro": "Bairro"},
        color="total_crimes",
        color_continuous_scale="Reds"
    )
    fig_abs.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_abs, use_container_width=True)

with col2:
    st.subheader("Top 10 Bairros: Taxa Real (por 100k hab)")
    fig_rate = px.bar(
        df_final.nlargest(10, "taxa_100k"),
        x="taxa_100k",
        y="bairro",
        orientation="h",
        text_auto=".1f",
        labels={"taxa_100k": "Crimes / 100k hab (anual)", "bairro": "Bairro"},
        color="taxa_100k",
        color_continuous_scale="OrRd"
    )
    fig_rate.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_rate, use_container_width=True)

st.divider()

# === Grafico de Dispersao: Populacao vs Crimes ===
st.subheader("Relação População x Crimes")
st.markdown("Bairros acima da linha vermelha possuem risco superior à média da cidade.")

fig_scatter = px.scatter(
    df_final,
    x="populacao_2022",
    y="crimes_ano",
    size="taxa_100k",
    color="taxa_100k",
    hover_name="bairro",
    text="bairro",
    labels={
        "populacao_2022": "População (Censo 2022)",
        "crimes_ano": "Média de Crimes / Ano",
        "taxa_100k": "Taxa por 100k hab"
    },
    color_continuous_scale="Viridis",
    height=600
)
# Adicionar linha de tendencia media
x_range = [0, df_final["populacao_2022"].max()]
y_mean_line = [x * (media_maceio / 100000) for x in x_range]
fig_scatter.add_trace(go.Scatter(
    x=x_range, y=y_mean_line, 
    mode="lines", name="Média Maceió", 
    line=dict(color="red", dash="dash")
))
fig_scatter.update_traces(textposition='top center')
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# === Tabela Detalhada ===
st.subheader("Tabela de Risco por Bairro")
st.markdown("Utilize esta tabela para auditar os valores exatos e o risco relativo.")

# Preparar tabela para exibicao
tab_disp = df_final[[
    "bairro", "populacao_2022", "total_crimes", "crimes_ano", "taxa_100k", "risco_relativo"
]].copy()
tab_disp.columns = [
    "Bairro", "População (2022)", "Total Crimes (Período)", "Média Crimes/Ano", "Taxa/100k hab", "Risco Relativo"
]
tab_disp = tab_disp.sort_values("Taxa/100k hab", ascending=False)

st.dataframe(
    tab_disp.style.format({
        "População (2022)": "{:,}",
        "Total Crimes (Período)": "{:,}",
        "Média Crimes/Ano": "{:.1f}",
        "Taxa/100k hab": "{:.2f}",
        "Risco Relativo": "{:.2f}x"
    }).background_gradient(subset=["Risco Relativo"], cmap="YlOrRd"),
    use_container_width=True,
    height=500
)

# === Conclusao e Metodologia ===
with st.expander("Nota Metodológica e Insights"):
    st.markdown(
        f"""
        **Insights Principais:**
        1. **Inversão de Ranking:** Bairros com menor população mas alta criminalidade (como Centro ou Jaraguá) 
           podem apresentar taxas de risco muito superiores a bairros gigantes como o Benedito Bentes.
        2. **Risco Médio:** A média de Maceió no período selecionado é de **{media_maceio:.2f} crimes por 100k hab/ano**.
        3. **Risco Relativo:** Um valor de 2.00x significa que o bairro é duas vezes mais perigoso que a média da cidade.

        **Metodologia:**
        - **Numerador:** Dados nominais de CVLI da SSP/AL.
        - **Denominador:** População do Censo 2022 (IBGE).
        - **Anualização:** Calculada dividindo o total de crimes pela quantidade de anos selecionada ({n_anos}).
        - **Bairros Excluídos:** O bairro Mutange foi excluído por possuir população zero no censo de 2022.
        """
    )

st.caption("Fontes: SSP/AL (Microdados CVLI) e IBGE (Censo 2022).")
