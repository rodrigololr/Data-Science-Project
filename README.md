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
3. **Preditor de Risco Real** para Maceió via **Regressão de Poisson** (NB04)
4. **Dashboard Streamlit Modular** com Mapa + Preditor + Explicação por IA (Gemini)

**Base:** 20.369 registros de CVLI (2012-2026). Fonte: [Secretaria de Estado da Segurança Pública de Alagoas](https://dados.al.gov.br/catalogo/dataset/cvli-2012-a-2023-base-microdados).

## Estrutura do Repositório (Modular)

```
projeto_cd/
├── .specs/                          # Documentação SDD/TLC
├── .notebook/                       # Memória do time e investigações
├── data/
│   ├── raw/cvli_microdados.csv      # Base original
│   ├── processed/cvli_clean.csv     # Base limpa
│   └── geo/                         # População Maceió (IBGE) + Coordenadas
├── notebooks/
│   ├── 01_analise_exploratoria_cvli.ipynb   # EDA original
│   ├── 03_geo_temporal.ipynb               # Mapa + Agregações
│   └── 04_preditor_maceio.ipynb            # Treino Poisson (XGBoost)
├── models/
│   ├── preditor_poisson_final.joblib       # Modelo final (Poisson)
│   └── preditor_poisson_final_meta.json    # Metadados e Calibração
├── app/
│   ├── streamlit_app.py             # Entry point
│   ├── data_loader.py               # Cache de dados e modelos
│   ├── predictor.py                 # Orquestrador de inferência
│   ├── ai_engine.py                 # Integração SHAP + Google Gemini
│   ├── ui_components.py             # Componentes visuais reutilizáveis
│   ├── domain.py                    # Constantes e domínios
│   ├── utils.py                     # Helpers de pré-processamento
│   └── pages/                       # Abas do Dashboard
├── requirements.txt
└── .env                             # Chaves de API (Gemini)
```

## Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar o .env (Necessário para a explicação por IA)
# GEMINI_API_KEY=sua_chave_aqui

# 3. Executar treinamento (Opcional, artefatos já inclusos)
python scripts/train_poisson_risk.py

# 4. Subir dashboard
streamlit run app/streamlit_app.py
```

## Decisões Arquiteturais Evoluídas

| # | Decisão | Razão |
|---|---|---|
| D1 | Preditor restrito a Maceió | Estabilidade estatística e foco demográfico |
| D2 | Regressão de Poisson | Ideal para modelagem de taxas/contagens de eventos raros |
| D3 | Imputação por Proxy Demográfico | Estima população específica (ex: homens de 20 anos) por bairro via proporções IBGE |
| D4 | Recalibração de Média | Compara risco individual contra a média de locais com crime, não contra a cidade toda vazia |
| D5 | Explicação por IA (Gemini) | Traduz pesos matemáticos (SHAP) em linguagem humana direta |
| D6 | Arquitetura Modular | Separação estrita entre UI (ui_components) e Lógica (ai_engine/predictor) |

## Resultados & Calibração

O modelo utiliza o **XGBoost Poisson** para estimar a taxa de crimes por 100 mil habitantes de um perfil específico. A calibração de risco ("Baixa/Média/Alta") é baseada em uma **Média de Referência (3.04)** obtida a partir das predições em locais com crimes reais, garantindo um ranking justo e condizente com a realidade de segurança pública de Maceió.

---
*Projeto acadêmico · UFAL · Ciência de Dados · 2026.1*
