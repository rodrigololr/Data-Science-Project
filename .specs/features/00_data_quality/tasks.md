# Tasks — Feature 00 (Data Quality)

## T001: Drop colunas com missing massivo

- [ ] Adicionar cell em NB01 após cell 6 (qualidade de dados)
- [ ] Justificar: "74% e 67% missing = imputação vira invenção"
- [ ] `df_clean = df.drop(columns=['ESCOLARIDADE VITIMA', 'OCUPACAO VITIMA'])`
- [ ] Imprimir `df_clean.shape` antes/depois
- [ ] Atualizar tabela de faltantes

**Done quando:** shape de `df_clean` tem 12 colunas e tabela de faltantes mostra apenas colunas com 0-5% missing.

## T002: Benchmark de fill methods

- [ ] Criar seção nova em NB01 (depois de T001)
- [ ] Para cada coluna restante com NaN, simular NaN artificial em 20% dos dados conhecidos
- [ ] Testar 5 métodos:
  1. **Drop:** remove linhas com NaN
  2. **Moda global:** preenche com valor mais frequente
  3. **Moda condicional:** moda por grupo (ex: sexo × faixa_etaria para COR/RACA)
  4. **KNN-Imputer:** k=5 com features correlacionadas (apenas IDADE)
  5. **RandomForest:** modelo preditivo por coluna
- [ ] Avaliar em test set: acurácia para categóricas, MAE/RMSE para IDADE
- [ ] Gerar tabela comparativa
- [ ] Documentar conclusão em `.notebook/sessions/`

**Done quando:** tabela com scores dos 5 métodos + recomendação explícita por coluna.

## Critérios de Aceitação

- Código executa sem erro em `nb01_clean` (state pós-drop)
- Cada método tem acurácia/MAE documentado
- Recomendação registrada em markdown no notebook + nota em `.notebook/sessions/`
