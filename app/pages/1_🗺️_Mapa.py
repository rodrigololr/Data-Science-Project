"""Pagina 1 - Mapa espaco-temporal."""
from __future__ import annotations
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import folium
from branca.element import MacroElement, Template
from folium.elements import JSCSSMixin
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

modo_mapa = st.radio(
    "Modo de visualização",
    ["Mapa atual", "Mapa temporal"],
    horizontal=True,
)
is_temporal = modo_mapa == "Mapa temporal"


class AnimatedHeatMap(JSCSSMixin, MacroElement):
    """Animated Leaflet heat layer without the TimeDimension plugin."""

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        (function() {
            const map = {{ this._parent.get_name() }};
            const frames = {{ this.frames_json }};
            const labels = {{ this.labels_json }};
            const heatLayer = L.heatLayer(frames[0] || [], {
                radius: {{ this.radius }},
                blur: {{ this.blur }},
                minOpacity: {{ this.min_opacity }},
                gradient: {{ this.gradient_json }}
            }).addTo(map);

            let current = 0;
            let timer = null;
            const control = L.control({position: "bottomleft"});
            control.onAdd = function() {
                const div = L.DomUtil.create("div", "leaflet-bar temporal-control");
                div.style.background = "white";
                div.style.padding = "8px";
                div.style.minWidth = "260px";
                div.style.boxShadow = "0 1px 5px rgba(0,0,0,0.35)";
                div.innerHTML = `
                    <div style="font-weight:700;margin-bottom:6px;color:#111">CVLI acumulado</div>
                    <div data-role="label" style="margin-bottom:6px;color:#111">${labels[0] || ""}</div>
                    <input data-role="range" type="range" min="0" max="${frames.length - 1}" value="0" step="1" style="width:100%" />
                    <button data-role="play" type="button" style="margin-top:6px;color:#111">Pausar</button>
                `;
                L.DomEvent.disableClickPropagation(div);
                L.DomEvent.disableScrollPropagation(div);
                return div;
            };
            control.addTo(map);

            const container = control.getContainer();
            const label = container.querySelector('[data-role="label"]');
            const range = container.querySelector('[data-role="range"]');
            const play = container.querySelector('[data-role="play"]');

            function showFrame(index) {
                current = Number(index);
                heatLayer.setLatLngs(frames[current] || []);
                label.textContent = labels[current] || "";
                range.value = current;
            }

            function start() {
                if (timer) return;
                play.textContent = "Pausar";
                timer = window.setInterval(function() {
                    showFrame((current + 1) % frames.length);
                }, 900);
            }

            function stop() {
                window.clearInterval(timer);
                timer = null;
                play.textContent = "Play";
            }

            range.addEventListener("input", function(event) {
                stop();
                showFrame(event.target.value);
            });
            play.addEventListener("click", function() {
                timer ? stop() : start();
            });
            start();
        })();
        {% endmacro %}
        """
    )

    default_js = [
        (
            "leaflet_heat",
            "https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet_heat.min.js",
        )
    ]

    def __init__(self, frames, labels, radius=22, blur=15, min_opacity=0.25):
        super().__init__()
        self._name = "AnimatedHeatMap"
        self.frames_json = json.dumps(frames)
        self.labels_json = json.dumps(labels)
        self.radius = radius
        self.blur = blur
        self.min_opacity = min_opacity
        self.gradient_json = json.dumps(
            {0.2: "blue", 0.4: "lime", 0.6: "yellow", 0.8: "orange", 1.0: "red"}
        )


def with_event_datetime(data: pd.DataFrame) -> pd.DataFrame:
    """Adiciona timestamp do evento a partir da data e hora registradas."""
    result = data.copy()
    result["evento_dt"] = pd.to_datetime(result["data_fato"], errors="coerce") + pd.to_timedelta(
        result["hora"].fillna(0).astype(int), unit="h"
    )
    return result


def offset_hash(value: str) -> tuple[float, float]:
    import hashlib

    h = int(hashlib.md5(str(value).encode()).hexdigest()[:4], 16)
    return ((h % 201) - 100) * 0.001, ((h >> 8) % 201 - 100) * 0.001


def add_missing_bairro_coords(cidade_data: pd.DataFrame, cidade: str, mun: pd.DataFrame) -> pd.DataFrame:
    if not cidade_data["lat"].isna().any():
        return cidade_data

    mun_row = mun[mun.cidade_norm == cidade]
    if len(mun_row) > 0:
        lat_c, lng_c = mun_row.iloc[0].lat, mun_row.iloc[0].lng
    else:
        lat_c = cidade_data["lat"].mean()
        lng_c = cidade_data["lng"].mean()

    for idx, row in cidade_data.iterrows():
        if pd.isna(row["lat"]) or pd.isna(row["lng"]):
            dlat, dlng = offset_hash(row["bairro"])
            cidade_data.at[idx, "lat"] = lat_c + dlat
            cidade_data.at[idx, "lng"] = lng_c + dlng

    return cidade_data


def render_temporal_heatmap(
    df_window: pd.DataFrame,
    zoom_cidade: str,
    mun: pd.DataFrame,
    frames_tempo: pd.DatetimeIndex,
    acumulacao: pd.Timedelta,
) -> None:
    labels = [
        f"{(fim - acumulacao):%d/%m %Hh} -> {fim:%d/%m %Hh}"
        for fim in frames_tempo
    ]
    geo_frames = []
    all_geo_data = []

    if zoom_cidade == "(Visão geral Alagoas)":
        centro = [-9.5, -36.5]
        zoom_start = 7
        radius = 22

        for fim in frames_tempo:
            inicio = fim - acumulacao
            frame_df = df_window[df_window["evento_dt"].between(inicio, fim)]
            grouped = frame_df.groupby("cidade_match").size().reset_index(name="count")
            geo_data = grouped.merge(
                mun[["cidade_norm", "lat", "lng"]],
                left_on="cidade_match",
                right_on="cidade_norm",
                how="left",
            ).dropna(subset=["lat", "lng"])
            geo_frames.append(geo_data)
            all_geo_data.append(geo_data)
    else:
        bairros_geo = load_bairros_top5()
        bairros_geo_cidade = bairros_geo[bairros_geo["cidade"] == zoom_cidade].copy()
        bairros_geo_cidade["bairro_norm"] = (
            bairros_geo_cidade["bairro"].astype(str).str.strip().str.upper()
        )

        for fim in frames_tempo:
            inicio = fim - acumulacao
            df_cidade = df_window[
                (df_window["cidade_match"] == zoom_cidade)
                & df_window["evento_dt"].between(inicio, fim)
            ].copy()
            grouped = (
                df_cidade.groupby("BAIRRO DO FATO")
                .size()
                .reset_index(name="count")
                .rename(columns={"BAIRRO DO FATO": "bairro"})
            )
            grouped["bairro_norm"] = grouped["bairro"].astype(str).str.strip().str.upper()
            geo_data = grouped.merge(
                bairros_geo_cidade[["bairro_norm", "lat", "lng"]],
                on="bairro_norm",
                how="left",
            ).drop(columns=["bairro_norm"])
            geo_data = add_missing_bairro_coords(geo_data, zoom_cidade, mun).dropna(
                subset=["lat", "lng"]
            )
            geo_frames.append(geo_data)
            all_geo_data.append(geo_data)

        geo_data_all = pd.concat(all_geo_data, ignore_index=True) if all_geo_data else pd.DataFrame()

        if len(geo_data_all) > 0:
            coord = geo_data_all[["lat", "lng"]].mean()
            centro = [coord["lat"], coord["lng"]]
        else:
            mun_row = mun[mun.cidade_norm == zoom_cidade]
            centro = [mun_row.iloc[0].lat, mun_row.iloc[0].lng] if len(mun_row) else [-9.5, -36.5]
        zoom_start = 12
        radius = 18

    geo_data_all = pd.concat(all_geo_data, ignore_index=True) if all_geo_data else pd.DataFrame()
    if len(geo_data_all) == 0:
        st.warning("Sem coordenadas para os eventos na janela selecionada.")
        return

    max_count = max(geo_data_all["count"].max(), 1)
    frames = []
    for frame in geo_frames:
        points = [
            [row["lat"], row["lng"], max(row["count"] / max_count, 0.05)]
            for _, row in frame.iterrows()
        ]
        frames.append(points)

    m = folium.Map(location=centro, zoom_start=zoom_start, tiles="OpenStreetMap")
    AnimatedHeatMap(frames, labels, radius=radius).add_to(m)
    st_folium(m, width=1200, height=600, returned_objects=[])


def render_empty_map(zoom_cidade: str, mun: pd.DataFrame) -> None:
    if zoom_cidade == "(Visão geral Alagoas)":
        centro = [-9.5, -36.5]
        zoom_start = 7
    else:
        mun_row = mun[mun.cidade_norm == zoom_cidade]
        centro = [mun_row.iloc[0].lat, mun_row.iloc[0].lng] if len(mun_row) else [-9.5, -36.5]
        zoom_start = 12

    m = folium.Map(location=centro, zoom_start=zoom_start, tiles="OpenStreetMap")
    st_folium(m, width=1200, height=600, returned_objects=[])


def show_nearest_event_hint(
    df_base: pd.DataFrame,
    center_dt: pd.Timestamp,
    zoom_cidade: str,
) -> None:
    nearby = df_base.copy()
    if zoom_cidade != "(Visão geral Alagoas)":
        nearby = nearby[nearby["cidade_match"] == zoom_cidade]

    if len(nearby) == 0:
        return

    distances = (nearby["evento_dt"] - center_dt).abs()
    nearest = nearby.loc[distances.idxmin()]
    delta_hours = distances.min() / pd.Timedelta(hours=1)
    st.info(
        f"Evento mais próximo para este recorte: "
        f"{nearest['evento_dt']:%d/%m/%Y %H:00} ({delta_hours:.0f}h de distância)."
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
        disabled=is_temporal,
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
        disabled=is_all_time or is_temporal,  # desabilitado em Todo o tempo/temporal
    )
    # Forçar "Ano inteiro" quando o controle temporal principal esta desativado.
    if is_all_time or is_temporal:
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

sexo_filter_eff = sexo_filter or ["Masculino", "Feminino"]
instrumento_filter_eff = instrumento_filter or [
    "Arma de fogo", "Arma branca", "Espancamento", "Outros"
]

# === Filtro adicional: cidade (top 5 ativa heatmap de bairro) ===
top5 = ["Maceio", "Arapiraca", "Rio Largo", "Uniao dos Palmares", "Marechal Deodoro"]
zoom_cidade = st.selectbox(
    "🔍 Zoom em cidade (top 5 — ativa heatmap de bairro):",
    ["(Visão geral Alagoas)"] + top5,
    index=0,
)

center_dt = None
inicio_temporal = None
fim_temporal = None
frames_tempo = None
acumulacao = None
if is_temporal:
    df_temporal_base = with_event_datetime(df_full).dropna(subset=["evento_dt"])
    df_temporal_base["cidade_match"] = (
        df_temporal_base["CIDADE DO FATO"]
        .astype(str)
        .str.strip()
        .replace({"Maceió": "Maceio", "União dos Palmares": "Uniao dos Palmares"})
    )
    min_date = df_temporal_base["evento_dt"].min().date()
    max_date = df_temporal_base["evento_dt"].max().date()
    tcol1, tcol2, tcol3, tcol4 = st.columns([2, 1, 1, 1])
    with tcol1:
        data_centro = st.date_input(
            "Data central da animação",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
        )
    with tcol2:
        hora_centro = st.slider("Hora central", 0, 23, 12)
    with tcol3:
        alcance_label = st.selectbox(
            "Alcance",
            ["7 dias", "15 dias", "30 dias"],
            index=2,
        )
    with tcol4:
        acumulacao_label = st.selectbox(
            "Acumular por quadro",
            ["24 horas", "3 dias", "7 dias"],
            index=2,
        )

    passo_label = st.radio(
        "Intervalo entre quadros",
        ["6 horas", "12 horas", "1 dia"],
        index=2,
        horizontal=True,
    )

    center_dt = pd.Timestamp(dt.datetime.combine(data_centro, dt.time(hour=hora_centro)))
    alcance = pd.Timedelta(days=int(alcance_label.split()[0]))
    acumulacao = pd.Timedelta(hours=24) if acumulacao_label == "24 horas" else pd.Timedelta(
        days=int(acumulacao_label.split()[0])
    )
    passo = {"6 horas": "6h", "12 horas": "12h", "1 dia": "24h"}[passo_label]
    inicio_temporal = center_dt - alcance
    fim_temporal = center_dt + alcance
    frames_tempo = pd.date_range(inicio_temporal, fim_temporal, freq=passo)
    st.caption(
        "No modo temporal, os filtros de período e janela ficam desativados. "
        "Cada quadro acumula eventos no período anterior, reduzindo quadros vazios."
    )

# === APLICAR FILTROS ===
# Filtro por ano (ou Todo o tempo)
if is_temporal:
    df = with_event_datetime(df_full)
    df = df[df["evento_dt"].between(inicio_temporal - acumulacao, fim_temporal)].copy()
elif is_all_time:
    df = df_full.copy()
else:
    df = df_full[df_full["ano"] == ano_filter].copy()

# Filtro de janela dentro do ano (so aplica no mapa atual com ano especifico)
if not is_all_time and not is_temporal:
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
df = df[df["SEXO DA VITIMA"].isin(sexo_filter_eff)]
df = df[df["grupo_instrumento"].isin(instrumento_filter_eff)]

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
if is_temporal:
    periodo_label = (
        f" — {inicio_temporal:%d/%m/%Y %H:00} a {fim_temporal:%d/%m/%Y %H:00}"
    )
elif is_all_time:
    periodo_label = f" — {all_time_label}"
else:
    periodo_label = f" — {ano_filter}"
    if janela == "Semestre":
        periodo_label += f" S{semestre}"
    elif janela == "Trimestre":
        periodo_label += f" T{trimestre}"
    elif janela == "Mês":
        periodo_label += f"/{mes:02d}"

if is_temporal:
    titulo_area = "Alagoas" if zoom_cidade == "(Visão geral Alagoas)" else zoom_cidade
    df_window_title = df[df["evento_dt"].between(inicio_temporal, fim_temporal)]
    if zoom_cidade != "(Visão geral Alagoas)":
        df_window_title = df_window_title[df_window_title["cidade_match"] == zoom_cidade]
    st.subheader(
        f"Mapa temporal — {titulo_area}{periodo_label} — {len(df_window_title):,} casos"
    )
    if len(df) == 0:
        st.warning("Sem eventos na janela temporal com os filtros selecionados.")
        render_empty_map(zoom_cidade, mun)
        hint_base = df_temporal_base[
            df_temporal_base["SEXO DA VITIMA"].isin(sexo_filter_eff)
            & df_temporal_base["grupo_instrumento"].isin(instrumento_filter_eff)
        ]
        show_nearest_event_hint(hint_base, center_dt, zoom_cidade)
    else:
        render_temporal_heatmap(df, zoom_cidade, mun, frames_tempo, acumulacao)

elif zoom_cidade == "(Visão geral Alagoas)":
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

        # Fallback para bairros sem coords Nominatim: centroide + offset hash pequeno.
        cidade_data = add_missing_bairro_coords(cidade_data, zoom_cidade, mun)

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
