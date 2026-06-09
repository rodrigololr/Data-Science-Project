# STATE — Status Vivo do Projeto

> Atualizado em 2026-06-06 (noite) após sub-agent review e correções.

## Tabela de Tasks

| ID | Task | Estado | % | Evidência |
|---|---|---|---|---|
| T001 | Drop ESCOL+OCUP | ✅ Done | 100 | NB01b seção 3 |
| T002 | Benchmark fill methods | ✅ Done | 100 | NB01b seção 4 |
| T003 | Carregar base | ✅ Done | 100 | NB01 cell 2 |
| T004 | Limpar NI→NaN | ✅ Done | 100 | NB01 cell 4 |
| T005 | Derivar vars temporais | ✅ Done | 100 | NB01 cell 4 |
| T006 | Agrupar instrumento | ✅ Done | 100 | NB01 cell 5 |
| T007 | Agrupar local | ✅ Done | 100 | NB01 cell 5 |
| T008 | Qualidade de dados | ✅ Done | 100 | NB01 cell 6 |
| T009 | Distribuições univariadas | ✅ Done | 100 | NB01 cells 8-12 |
| T010 | Top cidades/bairros | ✅ Done | 100 | NB01 cell 14-15 |
| T011 | Testar hipóteses H1-H4 | ✅ Done | 100 | NB01 cells 16+ |
| T012 | Clustering K-Means | ✅ Done | 100 | NB02 k=8 personas + PCA + heatmaps |
| T013 | K-Medoids | ✅ Done | 100 | NB02 k=3 (amostra 5k) |
| T014 | SHAP clustering | ✅ Done | 100 | Clusterização descritiva finalizada |
| T015 | Geocoding municípios | ✅ Done | 100 | NB03 seção 3 + municipios_al.csv |
| T016 | Geocoding bairros top 5 | ✅ Done | 100 | NB03 seção 4 + bairros_top5.csv |
| T017 | Choropleth + agregações | ✅ Done | 100 | NB03 seção 5 (5 PNGs) |
| T018 | HeatMap bairro + série | ✅ Done | 100 | NB03 seção 6 (2 HTMLs) |
| T019 | Preditor Poisson (XGBoost) | ✅ Done | 100 | Implementado proxy demográfico IBGE para Taxa 100k hab. |
| T020 | Validação + XAI | ✅ Done | 100 | Calibração intra-grupo + SHAP. Fator 'mês' removido. |
| T021 | Streamlit mapa | ✅ Done | 100 | app/pages/1_🗺️_Mapa.py operante |
| T022 | Streamlit preditor | ✅ Done | 100 | Refatorado para UI Modular + Integração Gemini (IA) |
| T023 | Doc SBC | ✅ Done | 100 | docs/artigo_sbc.md |
| T024 | Slides pitch+técnica | ✅ Done | 100 | docs/slides_pitch.md |

## Resumo

- **Concluídas:** Todas as tasks principais e evolutivas (Poisson, Gemini, Modularização) foram finalizadas com sucesso.
- **Pendentes críticos:** NENHUM
- **Pendentes não-críticos:** NENHUM

> *Nota: O modelo evoluiu de um classificador de tercis enviesado por volume para um preditor de regressão de Poisson ancorado em dados do Censo IBGE 2022. O target agora é a taxa real de vitimização por 100k hab, e o ranking é calibrado por grupo demográfico para garantir justiça e precisão.*

## Bloqueios

_Nenhum._

## Próximas Ações
1. Apresentação do Pitch e Defesa Técnica.

## Artefatos Produzidos

### Dados
- `data/processed/cvli_clean.csv` (20.369 × 25)
- `data/processed/agg_*.csv` (5 arquivos de agregação)
- `data/geo/municipios_al.csv` (102 municípios)
- `data/geo/populacao_maceio_bairros.csv` (Censo 2022)

### Modelos
- `models/preditor_poisson_final.joblib` (**XGBRegressor Poisson**)
- `models/preditor_poisson_final_meta.json` (Metadados e médias de referência por gênero)

### Arquitetura Web
- `app/ai_engine.py` (GenAI)
- `app/ui_components.py` (Layout)
- `app/predictor.py` (Core ML)
- `app/domain.py` & `app/utils.py`

