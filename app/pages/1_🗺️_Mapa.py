"""Pagina 1 - Mapa espaco-temporal."""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from data_loader import load_municipios, load_bairros_top5, load_clean

st.set_page_config(page_title="Mapa CVLI Alagoas", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa Espaço-Temporal — CVLI em Alagoas")
st.markdown(
    "Visualize a distribuição geográfica de CVLI com filtro de **ano**, "
    "**janela temporal**, **sexo** e **instrumento**."
)

# === Dados brutos (cacheado) ===
df_full = load_clean()

# === Controles ===
col1, col2, col3, col4 = st.columns(4)

# Anos disponiveis (cache)
anos_disponiveis = sorted(df_full["ano"].unique().tolist())
min_ano, max_ano = (anos_disponiveis[0], anos_disponiveis[-1]) if anos_disponiveis else (0, 0)

# Opcoes: "Todo o tempo" + cada ano individual
all_time_label = f"Todo o tempo ({min_ano}-{max_ano})"
ano_options = [all_time_label] + [str(a) for a in anos_disponiveis]

with col1:
    ano_filter_str = st.selectbox(
        "📅 Período",
        options=ano_options,
        index=0,  # default: Todo o tempo
    )

# Flag Todo o tempo
is_all_time = ano_filter_str == all_time_label
ano_filter = None if is_all_time else int(ano_filter_str)

with col2:
    janela = st.radio(
        "Janela" if is_all_time else "Janela dentro do ano",
        ["Ano inteiro", "Semestre", "Trimestre", "Mês"],
        index=0,
        horizontal=True,
        disabled=is_all_time,  # desabilitado em Todo o tempo
    )
    # Forçar "Ano inteiro" em Todo o tempo
    if is_all_time:
        janela = "Ano inteiro"

with col3:
    sexo_filter = st.multiselect(
        "Sexo da vítima",
        ["Masculino", "Feminino"],
        default=["Masculino", "Feminino"],
    )

with col4:
    instrumento_filter = st.multiselect(
        "Instrumento",
        ["Arma de fogo", "Arma branca", "Espancamento", "Outros"],
        default=["Arma de fogo", "Arma branca", "Espancamento", "Outros"],
    )

# === Filtro adicional: cidade (top 5 ativa heatmap de bairro) ===
top5 = ["Maceio", "Arapiraca", "Rio Largo", "Uniao dos Palmares", "Marechal Deodoro"]
zoom_cidade = st.selectbox(
    "🔍 Zoom em cidade (top 5 — ativa heatmap de bairro):",
    ["(Visão geral Alagoas)"] + top5,
    index=0,
)

# === APLICAR FILTROS ===
# Filtro por ano (ou Todo o tempo)
if is_all_time:
    df = df_full.copy()
else:
    df = df_full[df_full["ano"] == ano_filter].copy()

# Filtro de janela dentro do ano (so aplica se NAO for Todo o tempo)
if not is_all_time:
    if janela == "Semestre":
        semestre = st.radio(
            "Semestre",
            [1, 2],
            index=0,
            horizontal=True,
            key="semestre_select",
        )
        df = df[df["mes"] <= 6] if semestre == 1 else df[df["mes"] > 6]
    elif janela == "Trimestre":
        trimestre = st.radio(
            "Trimestre",
            [1, 2, 3, 4],
            index=0,
            horizontal=True,
            key="trimestre_select",
        )
        df = df[df["mes"].between((trimestre - 1) * 3 + 1, trimestre * 3)]
    elif janela == "Mês":
        meses_disp = sorted(df["mes"].unique().tolist())
        if not meses_disp:
            meses_disp = list(range(1, 13))
        mes = st.selectbox(
            "Mês",
            options=meses_disp,
            index=0,
            format_func=lambda m: [
                "", "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"
            ][m],
        )
        df = df[df["mes"] == mes]

# Filtros demograficos
df = df[df["SEXO DA VITIMA"].isin(sexo_filter)]
df = df[df["grupo_instrumento"].isin(instrumento_filter)]

# Normalizar cidade para match com geo
df["cidade_match"] = (
    df["CIDADE DO FATO"]
    .astype(str)
    .str.strip()
    .replace({"Maceió": "Maceio", "União dos Palmares": "Uniao dos Palmares"})
)

mun = load_municipios()

# === Contagem por municipio (do df JÁ filtrado) ===
mun_count = df.groupby("cidade_match").size().reset_index(name="count")
mun_data = mun.merge(
    mun_count, left_on="cidade_norm", right_on="cidade_match", how="left"
)
mun_data["count"] = mun_data["count"].fillna(0)

# === Construir mapa ===
if is_all_time:
    periodo_label = f" — {all_time_label}"
else:
    periodo_label = f" — {ano_filter}"
    if janela == "Semestre":
        periodo_label += f" S{semestre}"
    elif janela == "Trimestre":
        periodo_label += f" T{trimestre}"
    elif janela == "Mês":
        periodo_label += f"/{mes:02d}"

if zoom_cidade == "(Visão geral Alagoas)":
    st.subheader(f"Visão geral de Alagoas{periodo_label} — {len(df):,} casos no total")
    m = folium.Map(location=[-9.5, -36.5], zoom_start=7, tiles="OpenStreetMap")
    max_count = max(mun_data["count"].max(), 1)
    for _, row in mun_data.iterrows():
        if row["count"] == 0:
            continue
        radius = max(3, (row["count"] / max_count) * 25)
        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=radius,
            color="darkred",
            fill=True, fill_color="red", fill_opacity=0.5,
            popup=folium.Popup(
                f"<b>{row['cidade_norm']}</b><br>{int(row['count'])} casos",
                max_width=200,
            ),
        ).add_to(m)
    st_folium(m, width=1200, height=600, returned_objects=[])

else:
    # HeatMap com coords Nominatim (NÃO mais hash)
    df_cidade = df[df["cidade_match"] == zoom_cidade].copy()
    if len(df_cidade) == 0:
        st.warning(f"Sem dados para {zoom_cidade} com os filtros selecionados.")
    else:
        # Agregar por bairro
        bairro_count = (
            df_cidade.groupby("BAIRRO DO FATO")
            .size()
            .reset_index(name="count")
            .rename(columns={"BAIRRO DO FATO": "bairro"})
        )

        # Coords Nominatim (NÃO hash)
        bairros_geo = load_bairros_top5()
        bairros_geo_cidade = bairros_geo[bairros_geo["cidade"] == zoom_cidade].copy()

        # Merge por nome (case-insensitive para matching robusto)
        bairro_count["bairro_norm"] = bairro_count["bairro"].astype(str).str.strip().str.upper()
        bairros_geo_cidade["bairro_norm"] = (
            bairros_geo_cidade["bairro"].astype(str).str.strip().str.upper()
        )

        cidade_data = bairro_count.merge(
            bairros_geo_cidade[["bairro_norm", "lat", "lng"]],
            on="bairro_norm",
            how="left",
        )
        cidade_data = cidade_data.drop(columns=["bairro_norm"])

        # Fallback para bairros sem coords Nominatim:
        # centroide da cidade + offset hash (pequeno, ~1km)
        if cidade_data["lat"].isna().any():
            import hashlib
            mun_row = mun[mun.cidade_norm == zoom_cidade]
            if len(mun_row) > 0:
                lat_c, lng_c = mun_row.iloc[0].lat, mun_row.iloc[0].lng
            else:
                lat_c = cidade_data["lat"].mean()
                lng_c = cidade_data["lng"].mean()

            def offset_hash(bairro):
                h = int(hashlib.md5(str(bairro).encode()).hexdigest()[:4], 16)
                return ((h % 201) - 100) * 0.001, ((h >> 8) % 201 - 100) * 0.001

            for idx, row in cidade_data.iterrows():
                if pd.isna(row["lat"]) or pd.isna(row["lng"]):
                    dlat, dlng = offset_hash(row["bairro"])
                    cidade_data.at[idx, "lat"] = lat_c + dlat
                    cidade_data.at[idx, "lng"] = lng_c + dlng

        cidade_data = cidade_data.dropna(subset=["lat", "lng", "count"])
        cidade_data["count"] = cidade_data["count"].fillna(0).astype(int)

        st.subheader(
            f"HeatMap de bairros — {zoom_cidade}{periodo_label} "
            f"({len(df_cidade):,} casos no recorte)"
        )

        if len(cidade_data) == 0:
            st.warning("Sem dados de bairros para esta cidade.")
        else:
            # Centro do mapa: media das coords dos bairros
            coord = cidade_data[["lat", "lng"]].mean()
            m = folium.Map(
                location=[coord["lat"], coord["lng"]],
                zoom_start=12,
                tiles="OpenStreetMap",
            )
            # HeatMap normalizado
            max_cnt = max(cidade_data["count"].max(), 1)
            pts = [
                [row["lat"], row["lng"], row["count"] / max_cnt]
                for _, row in cidade_data.iterrows()
            ]
            HeatMap(pts, radius=20, blur=15, max_zoom=13).add_to(m)
            for _, row in cidade_data.iterrows():
                folium.CircleMarker(
                    location=[row["lat"], row["lng"]],
                    radius=max(3, (row["count"] / max_cnt) * 10 + 2),
                    color="black",
                    fill=True, fill_color="red", fill_opacity=0.7,
                    popup=f"<b>{row['bairro']}</b><br>{int(row['count'])} casos",
                ).add_to(m)
            st_folium(m, width=1200, height=600, returned_objects=[])

            # Top bairros
            st.markdown("**Top 10 bairros neste recorte:**")
            st.dataframe(
                cidade_data.nlargest(10, "count")[["bairro", "count"]].reset_index(drop=True),
                use_container_width=True,
            )

# === Estatísticas ===
st.divider()

# Dataframe para estatísticas (contextual ao zoom)
if zoom_cidade == "(Visão geral Alagoas)":
    df_stats = df.copy()
    titulo_stats = "Alagoas (Geral)"
else:
    df_stats = df[df["cidade_match"] == zoom_cidade].copy()
    titulo_stats = f"Cidade: {zoom_cidade}"

st.subheader(f"📊 Estatísticas — {titulo_stats}")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Casos no recorte", f"{len(df_stats):,}")

with c2:
    if zoom_cidade == "(Visão geral Alagoas)":
        st.metric("Municípios afetados", df_stats["cidade_match"].nunique())
    else:
        # Se for cidade, mostrar % do total do estado no período
        total_estado = len(df)
        pct = (len(df_stats) / total_estado * 100) if total_estado > 0 else 0
        st.metric("% do total AL", f"{pct:.1f}%")

with c3:
    if zoom_cidade == "(Visão geral Alagoas)":
        val_counts = df_stats["CIDADE DO FATO"].value_counts()
        top_val = val_counts.index[0] if not val_counts.empty else "—"
        st.metric("Cidade mais afetada", top_val)
    else:
        st.metric("Cidade selecionada", zoom_cidade)

with c4:
    # Filtro para evitar categorias genéricas como bairro principal
    ignorar = ["ZONA RURAL", "ZONA URBANA", "NÃO INFORMADO", "ZURONA RURAL", "RURAL"]
    bairros_validos = df_stats[
        ~df_stats["BAIRRO DO FATO"].astype(str).str.upper().isin(ignorar)
    ]["BAIRRO DO FATO"]
    
    val_counts_b = bairros_validos.value_counts()
    top_bairro = val_counts_b.index[0] if not val_counts_b.empty else "—"
    st.metric("Bairro mais afetado", top_bairro)

st.caption(
    f"Fonte: Secretaria de Estado da Segurança Pública de Alagoas (dados abertos). "
    f"Coordenadas de bairro via Nominatim/OpenStreetMap."
)
