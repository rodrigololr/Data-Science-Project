# Feature 04 — Preditor Maceió (NB04)

## Objetivo

Classificar o **perfil de risco** de uma pessoa (segmento demográfico + contexto) em 3 classes:
- **Baixa** chance
- **Média** chance
- **Alta** chance

Restrito a **Maceió** (33% da base; 7.013 registros). Outras cidades não têm massa estatística.

## Saída

**3 classes**, não probabilidade. Decisão D2 (ver DECISIONS.md) — honestidade epistemológica.

## Como derivar o target

```
// Definir segmento = (sexo, faixa_etaria, periodo_dia, grupo_local, dia_semana)
// Para cada registro, contar quantos CVLI existem no mesmo segmento
// Cortar em tercis:
//   count ≤ 33%  → 'baixa'
//   count ≤ 66%  → 'media'
//   count > 66%  → 'alta'
// Atribuir classe a cada registro
```

## Features (X)

| Variável | Tipo | Encoding |
|---|---|---|
| SEXO DA VITIMA | binário | 0/1 |
| faixa_etaria | categórico | one-hot |
| periodo_dia | categórico | one-hot |
| dia_semana | categórico | one-hot |
| grupo_local | categórico | one-hot |
| grupo_instrumento | categórico | one-hot |

## Modelos candidatos

1. **RandomForestClassifier** (baseline, feature importance)
2. **XGBoost** (performance)
3. **LogisticRegression** (interpretabilidade)

## Validação

- Stratified K-Fold (k=5)
- Métricas: accuracy, F1 macro, confusion matrix
- SHAP values (TreeExplainer) — waterfall por exemplo

## Estrutura NB04

```
// 1. Setup
// 2. Carga base limpa
// 3. Filtro Maceió
// 4. Definir segmento + count + tercis → y_classe
// 5. Encoding features
// 6. Split treino/teste (80/20 estratificado)
// 7. Modelo 1: RandomForest
// 8. Modelo 2: XGBoost
// 9. Modelo 3: LogisticRegression
// 10. Comparação de métricas
// 11. SHAP waterfall exemplo end-to-end
// 12. Serialização (joblib) do modelo escolhido
```

## Tasks (T019-T020)

| ID | Task | Estado |
|---|---|---|
| T019 | Pipeline preditor Maceió 3-cl | ⏳ Pending |
| T020 | Validação + SHAP | ⏳ Pending |
