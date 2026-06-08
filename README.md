# CVLI Alagoas — Análise Espaço-Temporal de Criminalidade

**Universidade Federal de Alagoas (UFAL)** · Instituto de Computação
**Disciplina:** Ciência de Dados · 2026.1
**Equipe:** 
- Antônio Guilherme 
- Antônio Rodrigo Tenório 
- Sandro Gomes Paulino

---

## Sobre o Projeto

Análise de 14 anos de microdados de Crimes Violentos Letais Intencionais (CVLI) em Alagoas, com entrega de:

1. **EDA documentada** (NB01 + NB01b)
2. **Mapa espaço-temporal interativo** (NB03)
3. **Preditor de risco em 3 classes** para Maceió (NB04)
4. **Dashboard Streamlit** com mapa + preditor

**Base:** 20.369 registros de CVLI (2012-2026), 13 colunas originais. Fonte: [Secretaria de Estado da Segurança Pública de Alagoas](https://dados.al.gov.br/catalogo/dataset/cvli-2012-a-2023-base-microdados).

## Estrutura do Repositório

```
projeto_cd/
├── .specs/                          # Documentação SDD/TLC
│   ├── PROJECT.md                   # visão, equipe, escopo
│   ├── STATE.md                     # status tasks
│   ├── DECISIONS.md                 # ADRs
│   ├── ROADMAP.md                   # timeline
│   └── features/                    # 6 features com design.md + tasks.md
├── .notebook/                       # memória do time
│   ├── README.md
│   ├── sessions/                    # o que foi feito
│   └── investigations/              # análises profundas
├── data/
│   ├── raw/cvli_microdados.csv      # base original
│   ├── processed/                   # derivados dos notebooks
│   │   ├── cvli_clean.csv           # base limpa (20.369 rows)
│   │   ├── agg_*.csv                # agregacoes para o mapa
│   │   └── *.png                    # figuras estaticas
│   └── geo/                         # centroides municipios + bairros
├── notebooks/
│   ├── 01_analise_exploratoria_cvli.ipynb   # EDA original
│   ├── 01b_data_quality.ipynb              # T001-T002: drop + fill benchmark
│   ├── 02_perfilamento_dinamico_risco.ipynb # clustering (WIP)
│   ├── 03_geo_temporal.ipynb               # T015-T018: mapa + agregacoes
│   └── 04_preditor_maceio.ipynb            # T019-T020: 3 classes
├── models/
│   ├── preditor_maceio.joblib       # modelo final
│   └── preditor_meta.json           # metadados
├── app/
│   ├── streamlit_app.py             # entry point
│   ├── data_loader.py               # cache de CSVs + modelo
│   ├── predictor.py                 # wrapper preditor
│   └── pages/
│       ├── 1_🗺️_Mapa.py
│       ├── 2_🎯_Preditor.py
│       └── 3_📊_Sobre.py
├── docs/                            # PDFs do projeto (manter existentes)
├── README.md
├── requirements.txt
└── .venv/                           # ambiente local
```

## Como Rodar

```bash
# 1. Ativar ambiente
source .venv/bin/activate

# 2. Instalar deps
pip install -r requirements.txt

# 3. Executar pipeline (em ordem, NB01b -> NB03 -> NB04)
jupyter nbconvert --to notebook --execute notebooks/01b_data_quality.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_geo_temporal.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_preditor_maceio.ipynb

# 4. Subir dashboard
streamlit run app/streamlit_app.py
```

Abre em `http://localhost:8501`.

## Decisões Arquiteturais

| # | Decisão | Razão |
|---|---|---|
| D1 | Preditor restrito a Maceió | 33% da base, evita viés populacional em cidades pequenas |
| D2 | Saída em 3 classes (baixa/média/alta) | Honestidade — não prometemos probabilidade individual |
| D3 | Sem IBGE no MVP | Tercis de contagem bastam para ranking |
| D4 | Top 5 cidades para HeatMap bairro | Concentram 48,7% dos CVLI |
| D5 | Streamlit (não Dash/Flask) | 1-2 dias de entrega, Python-only |
| D6 | Segmento coarsened (sexo, faixa_etaria) | Bairro removido do target (territorializava) |
| D7 | Assumir leakage na doc | Ético — modelo é lookup, não preditor genuíno |

Ver `.specs/DECISIONS.md` para detalhes.

## Resultados Preliminares

| Item | Valor |
|---|---|
| Registros | 20.369 (após drop de NI) |
| Maceió (% da base) | 33,3% |
| Melhor modelo preditor | XGBoost |
| F1 macro (5-fold CV) | **0,997*** |
| Acurácia teste | ~99%* |
| Visualizações geradas | 7 PNG + 2 HTML |
| Artefatos do modelo | `models/preditor_maceio.joblib` (14 MB) |

> **\* Aviso metodológico importante:** o F1 macro de 0,997 reflete que o
> target (`classe_risco`) é derivado das próprias features demográficas do modelo
> (segmento = sexo × faixa_etária). O modelo funciona essencialmente como uma
> **tabela de lookup** do segmento, com refinamento por contexto. **NÃO é um
> preditor genuíno de vitimização.** Para generalização, seria preciso splits
> temporais, target não derivado das features e validação out-of-segment. Ver
> `.specs/DECISIONS.md` (D9) e a aba **Sobre** do dashboard.

## Limitações & Aspectos Éticos

- **Preditor é lookup table** — classifica perfil em tercis, não prediz evento futuro
- **Só funciona para Maceió** (decisão metodológica — D1)
- **Coordenadas de bairro são aproximadas** (centroide + offset determinístico)
- **2026 é ano parcial** (janeiro a abril) — séries temporais têm viés
- **Nenhuma predição individual**: o modelo é descritivo, não prescritivo
- **Acurácia inflada** pelo leakage (D9) — não usar como referência de qualidade

## Documentação Completa

- `.specs/PROJECT.md` — visão geral
- `.specs/STATE.md` — status de cada task
- `.specs/DECISIONS.md` — 9 ADRs
- `.notebook/sessions/` — log diário do time
- `.notebook/investigations/` — análises profundas (IBGE, preditor)

## Stack

**Core:** Python 3.12 · Pandas · NumPy · Scikit-learn · XGBoost · SHAP
**Geo:** GeoPandas · Folium · Branca
**Dashboard:** Streamlit · Streamlit-Folium · Plotly
**Documentação:** Jupyter · SDD/TLC

---

*Projeto acadêmico · UFAL · Ciência de Dados · 2026.1*
