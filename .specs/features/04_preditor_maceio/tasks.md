# Tasks — Feature 04 (Preditor Maceió)

## T019: Pipeline preditor 3-classes

- [ ] Criar `notebooks/04_preditor_maceio.ipynb`
- [ ] Carregar `data/raw/cvli_microdados.csv`
- [ ] Aplicar limpeza padrão (NI→NaN, derivadas)
- [ ] Filtrar `CIDADE DO FATO == 'Maceió'`
- [ ] Definir `segmento` (concatenação de features)
- [ ] Contar CVLI por segmento
- [ ] Cortar em tercis → coluna `classe_risco`
- [ ] Encoding: one-hot para categóricas
- [ ] Split 80/20 estratificado
- [ ] Treinar 3 modelos (RF, XGB, LR)
- [ ] Tabela comparativa de métricas

## T020: Validação + SHAP

- [ ] StratifiedKFold (k=5) para cada modelo
- [ ] Confusion matrix por classe
- [ ] SHAP TreeExplainer no melhor modelo
- [ ] Waterfall plot para 1 exemplo "alta" e 1 "baixa"
- [ ] Serializar modelo final via `joblib` em `models/`
- [ ] Salvar encoder em `models/`

## Critérios de Aceitação

- Acurácia ≥ baseline de classe majoritária
- F1 macro ≥ 0,50
- Pelo menos 1 exemplo SHAP documentado
- Modelo carrega sem erro: `joblib.load('models/preditor.joblib').predict(X_test)`
