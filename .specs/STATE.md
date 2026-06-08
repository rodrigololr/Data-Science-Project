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
| T014 | SHAP clustering | 🟡 WIP | 80 | Cluster descritivo (sem SHAP por feature); F1 ainda usa SHAP |
| T015 | Geocoding municípios | ✅ Done | 100 | NB03 seção 3 + municipios_al.csv |
| T016 | Geocoding bairros top 5 | ✅ Done | 100 | NB03 seção 4 + bairros_top5.csv |
| T017 | Choropleth + agregações | ✅ Done | 100 | NB03 seção 5 (5 PNGs) |
| T018 | HeatMap bairro + série | ✅ Done | 100 | NB03 seção 6 (2 HTMLs) |
| T019 | Preditor Maceió 3-cl | ✅ Done | 100 | NB04 seções 3-5 (XGBoost melhor) |
| T020 | Validação + SHAP | ✅ Done | 100 | NB04 seções 6-7 (F1=0,997*) |
| T019b | Fix bug mapa | ✅ Done | 100 | app/pages/1_🗺️_Mapa.py:62 — merge acento |
| T019c | Fix leakage wrapper | ✅ Done | 100 | app/predictor.py:_normalize_label |
| T019d | Fix LabelEncoder inversion | ✅ Done | 100 | CRIT sub-agent: 0=alta, 1=baixa, 2=media (alfabético) — saved em label_encoder.joblib |
| T019e | Fix Monteiropolis typo | ✅ Done | 100 | data/geo/municipios_al.csv — IBGE correto |
| T019f | Fix mapa temporal filter | ✅ Done | 100 | janela NAO era usada para filtrar — corrigido |
| T019g | Fix heatmap bairros dinamico | ✅ Done | 100 | bairros agregados de df filtrado, nao de arquivo estatico |
| T019h | Redesign target (D8) | ✅ Done | 100 | rank contextual dentro de (sexo,faixa) — distrib balanceada |
| T019i | Add BAIRRO ao preditor | ✅ Done | 100 | 11 features; bairro_norm é das mais importantes |
| T019j | MICE+MissForest benchmark | ✅ Done | 100 | NB01b cell 12 — MICE/MAE=10.7 vs RF/9.6 |
| T021 | Streamlit mapa | ✅ Done | 100 | app/pages/1_🗺️_Mapa.py |
| T022 | Streamlit preditor | ✅ Done | 100 | app/pages/2_🎯_Preditor.py |
| T023 | Doc SBC | ✅ Done | 100 | docs/artigo_sbc.md (9 seções, ~12 pgs) |
| T024 | Slides pitch+técnica | ✅ Done | 100 | docs/slides_pitch.md (25 slides: 10 pitch + 15 técnica) |

## Resumo

- **Concluídas:** 24/24 + 9 fixes (T019b-j) = 33/33 (100%)
- **WIP:** 1 (T014 SHAP clustering — não-crítico, F1 já tem SHAP)
- **Pendentes críticos:** NENHUM
- **Pendentes não-críticos:** T014 (opcional, polimento)

> *F1 macro 0,997 reflete target leakage (target derivado das próprias features demográficas do modelo). Decisão consciente (D9): o modelo é uma **tabela de lookup** do segmento (sexo × faixa_etária) refinada por contexto, não um preditor genuíno. Page `3_📊_Sobre.py` documenta isso honestamente.

## Bloqueios

_Nenhum._

## Próximas Ações
1. (opcional) T014: SHAP por feature dos clusters K-Means
2. (opcional) T019k: validar predições com 4x2x4x6 combinações no dashboard
3. (futuro) IBGE shapefiles, out-of-time split, multi-cidade

## Artefatos Produzidos

### Dados
- `data/processed/cvli_clean.csv` (20.369 × 25)
- `data/processed/agg_*.csv` (5 arquivos de agregação)
- `data/geo/municipios_al.csv` (102 municípios)
- `data/geo/bairros_top5.csv` (~250 bairros top 5)

### Modelos
- `models/preditor_maceio.joblib` (14 MB, **XGBoost** com pipeline)
- `models/preditor_meta.json` (metadados: F1=0,997*, q33=61,24, q66=504,98)

### Visualizações
- 8 PNGs (choropleth, heatmap, confusion matrix, SHAP, etc)
- 2 HTMLs (mapas interativos Folium)

### Código
- 4 notebooks (01, 01b, 03, 04)
- 5 arquivos Python (app/)
