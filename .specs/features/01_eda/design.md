# Feature 01 — EDA (Retroativo)

> Esta feature já está implementada em `notebooks/01_analise_exploratoria_cvli.ipynb`. Este doc serve como memorial descritivo.

## O que foi feito

| Etapa | Local no NB01 | Resultado |
|---|---|---|
| Carga do CSV | cell 2 | 21.217 × 14 |
| Tipagem | cell 3 | 13 str + 1 int |
| Limpeza NI→NaN + derivadas | cell 4 | +8 cols (data, hora, idade, ano, mes, dia_semana, periodo_dia, faixa_etaria) |
| Agrupamentos | cell 5 | +2 cols (grupo_instrumento, grupo_local) |
| Tabela de faltantes | cell 6 | Tabela ordenada por % |
| Distribuições univariadas | cells 8-12 | Tabelas por coluna |
| Top cidades/bairros | cells 14-15 | Top 15 cada |
| Testes de hipótese H1-H4 | cells 16+ | H1 confirmada: 46,94% match |

## Principais Achados

- 95,10% Homicídio; 2,70% Roubo c/ morte; 1,48% Feminicídio
- 93,34% vítimas Masculino
- 75,48% Pardas, 11,53% Brancas
- 77,24% Arma de fogo, 13,71% Arma branca
- **Maceió = 33,05%** da base (não 45% como mencionado inicialmente)

## Tarefas (T003-T011)

Todas ✅ Done. Ver `STATE.md`.

## Atualizações Pendentes

- [ ] T001-T002 (data quality) — vão ser adicionadas no NB01 como novas seções
- [ ] Refactor: introduzir `df_clean` pós-drop no início do pipeline
