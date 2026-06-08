# Feature 05 — Dashboard Streamlit

## Objetivo

App local com 3 abas:
1. **🗺️ Mapa** — visualização espaço-temporal interativa
2. **🎯 Preditor** — formulário de risco
3. **📊 Sobre** — metodologia + limitações éticas

## Arquitetura

```
app/
├── streamlit_app.py           # entry point + roteamento de abas
├── pages/
│   ├── 1_🗺️_Mapa.py
│   ├── 2_🎯_Preditor.py
│   └── 3_📊_Sobre.py
├── data_loader.py             # cache de CSV + geo
├── predictor.py               # wrapper do modelo joblib
└── requirements.txt
```

## Tab 1 — Mapa

### Controles
- **Slider:** ano (2012-2026)
- **Radio:** janela temporal (`Mês` | `Trimestre` | `Semestre` | `Ano`)
- **Multiselect:** sexo, faixa_etária, instrumento (filtros)

### Visualização
- **Default (zoom AL):** choropleth dos 102 municípios por contagem
- **Auto-switch:** se filtro de cidade incluir top 5 + zoom_in flag → heatmap de bairro
- **Hover:** nº casos, % do total, ranking

## Tab 2 — Preditor

### Form
- Sexo (radio: Masculino / Feminino)
- Idade (slider 0-100)
- Cidade (selectbox — default Maceió, outras = "fora do escopo")
- Dia da semana (radio 7 opções)
- Período do dia (radio 4 opções)
- Local do fato (selectbox)

### Output
- Card grande com classe (`baixa` verde, `média` amarelo, `alta` vermelho)
- Comparação: "X% acima/abaixo da média Maceió"
- SHAP waterfall (top 5 contribuidoras)
- Texto disclaimer: "ferramenta estatística, não predição individual"

## Tab 3 — Sobre

- Texto curto explicando metodologia
- Lista de limitações éticas
- Fonte dos dados + créditos

## Tasks (T021-T022)

| ID | Task | Estado |
|---|---|---|
| T021 | Streamlit mapa | ⏳ Pending |
| T022 | Streamlit preditor | ⏳ Pending |

## Como Rodar

```bash
.venv/bin/streamlit run app/streamlit_app.py
```

Abre em `http://localhost:8501`.
