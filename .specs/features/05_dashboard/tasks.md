# Tasks — Feature 05 (Dashboard)

## T021: Streamlit mapa

- [ ] `app/streamlit_app.py` com roteamento de páginas
- [ ] `app/data_loader.py` com cache `@st.cache_data` para CSV/geo
- [ ] `app/pages/1_🗺️_Mapa.py`:
  - Slider ano (2012-2026)
  - Radio janela temporal
  - Multiselect filtros
  - Choropleth (Folium + st-folium)
  - Auto-switch para heatmap bairro se cidade in top 5
- [ ] Hover com tooltip custom
- [ ] Testar com `streamlit run`

## T022: Streamlit preditor

- [ ] `app/pages/2_🎯_Preditor.py`:
  - Form com 6 inputs
  - Botão "Calcular risco"
  - Carrega modelo joblib
  - Predição + probabilidade por classe
  - SHAP waterfall
  - Card visual com classe + comparação Maceió média
- [ ] `app/pages/3_📊_Sobre.py`:
  - Texto metodológico
  - Limitações
  - Créditos
- [ ] Testar end-to-end

## Critérios de Aceitação

- App abre sem erro
- Mapa renderiza <5s
- Preditor retorna classe + SHAP em <3s
- 3 abas navegáveis
