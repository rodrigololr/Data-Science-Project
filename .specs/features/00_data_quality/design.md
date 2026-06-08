# Feature 00 — Data Quality

## Contexto

Base CVLI original tem 21.217 registros × 14 colunas. Valores ausentes estão codificados como string `"NI"`. Qualidade mapeada em NB01 (cell 6).

## Problema

Duas colunas com missing massivo inviabilizam imputação razoável:

| Coluna | Faltantes | % |
|---|---|---|
| ESCOLARIDADE VITIMA | 15.733 | 74,15% |
| OCUPACAO VITIMA | 14.340 | 67,59% |

Restantes têm 0,4%-5,1% — recuperáveis com métodos de imputação.

## Objetivos

1. **T001** — Decidir destino das 2 colunas com missing massivo
2. **T002** — Comparar 5 métodos de imputação nas colunas restantes e recomendar o melhor

## Decisão Recomendada

**T001:** Drop de `ESCOLARIDADE VITIMA` e `OCUPACAO VITIMA`. Manter 12 colunas restantes.

**T002:** Benchmark comparativo com 5 estratégias, validando em split 80/20. Métrica varia por tipo de coluna:
- Categóricas (COR/RACA, INSTRUMENTO, LOCAL): acurácia
- Numérica (IDADE): MAE e RMSE

## Saída Esperada

- DataFrame limpo com 12 colunas + 8 derivadas
- Tabela de comparação de fill methods
- Recomendação justificada registrada em `.notebook/sessions/`

## Não-Objetivos

- Não criar pipeline de produção (apenas análise exploratória)
- Não aplicar técnicas avançadas (MICE, missForest) — overhead não justifica
