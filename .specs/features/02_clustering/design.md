# Feature 02 — Clustering de Perfis

## Status

🟡 Parcialmente implementado em `notebooks/02_perfilamento_dinamico_risco.ipynb`.

## Contexto

Decisão da equipe (registrada no próprio NB02): **restringir clustering a variáveis de perfil + horário**, excluindo ESCOLARIDADE, OCUPACAO, CIDADE, BAIRRO (risco de overfitting por alta cardinalidade).

## Restrições aplicadas

| Variável | Status no clustering |
|---|---|
| SEXO DA VITIMA | ✅ Usada |
| COR/RACA DA VITIMA | ✅ Usada |
| IDADE DA VITIMA / faixa_etaria | ✅ Usada |
| INSTRUMENTO UTILIZADO / grupo_instrumento | ✅ Usada |
| LOCAL DO FATO / grupo_local | ✅ Usada |
| HORA / periodo_dia | ✅ Usada |
| dia_semana | ✅ Usada |
| ESCOLARIDADE VITIMA | ❌ Excluída |
| OCUPACAO VITIMA | ❌ Excluída |
| CIDADE DO FATO | ❌ Excluída |
| BAIRRO DO FATO | ❌ Excluída |

## Tarefas (T012-T014)

| ID | Task | Estado |
|---|---|---|
| T012 | K-Means | 🟡 WIP (cells 1-3 do NB02) |
| T013 | K-Medoids | ⏳ Pending |
| T014 | SHAP clustering | ⏳ Pending |
