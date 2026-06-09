# Feature 04 — Preditor Maceió (NB04)

## Objetivo

Estimar a **Taxa de Risco Real** de uma pessoa (segmento demográfico + contexto) baseada em uma **Regressão de Poisson**, e classificá-la em 3 níveis (Baixa/Média/Alta) comparando a taxa do perfil com a média de risco de seu próprio grupo demográfico.
Restrito a **Maceió** (33% da base; 7.013 registros).

## Saída

**Taxa Contínua (Crimes por 100k hab)** e uma **Classe de Risco (Baixa/Média/Alta)**.
Decisão atualizada — Evoluímos do classificador de tercis enviesado para a estimação do risco real baseada em densidade populacional (IBGE).

## Como derivar o target (Proxy Demográfico)

```
// 1. Obter População Total do Bairro (Censo IBGE 2022)
// 2. Mapear Proporções de Sexo e Faixa Etária de Maceió
// 3. populacao_perfil = populacao_bairro * prop_sexo * prop_faixa
// 4. crimes_anuais = crimes_no_segmento / anos_historico
// 5. target_taxa = (crimes_anuais / populacao_perfil) * 100.000
```

## Features (X)

| Variável | Tipo | Encoding |
|---|---|---|
| SEXO DA VITIMA | binário | one-hot |
| faixa_etaria | categórico | one-hot |
| periodo_dia | categórico | one-hot |
| dia_semana | categórico | one-hot |
| grupo_local | categórico | one-hot |
| bairro | categórico | one-hot |

*(Nota: 'Mês' foi removido por ser ruído sazonal irrelevante; 'grupo_instrumento' foi removido por não ser uma feature preditiva de entrada do usuário).*

## Modelo Escolhido

**XGBRegressor (objective='count:poisson')**
Com parâmetros de regularização (subsample, colsample_bytree) para lidar com imputação heurística.

## Calibração e Ranking

O threshold de classificação utiliza a **Média de Referência Intra-grupo** (calculada apenas sobre os locais com histórico de crimes), garantindo que a régua para Mulheres seja baseada no risco histórico das mulheres, e não distorcida pelo volume de crimes masculinos.

## Integração XAI (Explainable AI)

O modelo final conta com o `TreeExplainer` do **SHAP**, que extrai as top 3 features responsáveis por elevar a taxa daquele perfil. Esses dados são injetados em um LLM (Google Gemini) para gerar uma explicação fluida e baseada em causa raiz.
