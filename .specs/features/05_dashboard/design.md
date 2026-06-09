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

## Tab 2 — Preditor (Risco Real)

### Form
- Sexo (radio: Masculino / Feminino)
- Idade (slider 0-100)
- Bairro do fato (selectbox)
- Dia da semana (selectbox 7 opções)
- Hora do fato (slider 0-23)
- Local do fato (selectbox)

### Output Visual
- **Card Categórico:** Classe (`baixa` verde, `média` amarelo, `alta` vermelho) baseada na Média de Referência do Sexo.
- **Gráfico (Gauge):** Medidor contínuo mostrando a Taxa de Crimes Prevista por 100k habitantes, com a linha de threshold na média de Maceió.
- **Risco Relativo:** Multiplicador "Xx a média do seu perfil na cidade".

### Inteligência Artificial (Explainable AI)
- Botão "✨ Gerar Explicação por IA" (com cooldown de 60s anti-abuso).
- Extrai os top 3 fatores via SHAP.
- Cruza com a base de dados em tempo real (data-driven prompt).
- Chama o Google Gemini (1.5 Flash) para gerar 1 parágrafo analítico de causa raiz citando os números reais daquele bairro.

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
