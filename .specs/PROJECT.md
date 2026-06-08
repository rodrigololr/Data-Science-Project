# CVLI Alagoas — Projeto Final de Ciência de Dados

**Universidade Federal de Alagoas (UFAL)** · Instituto de Computação
**Disciplina:** Ciência de Dados · 2026.1
**Equipe:** Antônio Guilherme · Antônio Rodrigo Tenório · Sandro Gomes Paulino

---

## 1. Visão

Transformar 14 anos de microdados de Crimes Violentos Letais Intencionais (CVLI) em Alagoas (21.217 registros, 2012→2026) em inteligência acionável para segurança pública, através de uma análise espaço-temporal e um preditor de risco relativo.

## 2. Problema de Negócio

Segurança pública em Alagoas é estruturalmente crítica. O estado carece de ferramentas que transformem dados brutos de ocorrências em **insights operacionais**: onde alocar viaturas, quando reforçar patrulha, qual perfil populacional está mais exposto.

## 3. Escopo da Entrega Final

| Item | Status | Valor |
|---|---|---|
| EDA documentada (NB01) | ✅ Done | Visão geral + qualidade de dados |
| Clustering de perfis (NB02) | 🟡 WIP | Personas de vítimas |
| Mapa espaço-temporal (NB03) | ⏳ Pending | Choropleth AL + HeatMap top 5 cidades |
| Preditor Maceió (NB04) | ⏳ Pending | Risco em 3 classes (baixa/média/alta) |
| Dashboard Streamlit | ⏳ Pending | 2 abas: mapa + preditor |
| Documento SBC | ⏳ Pending | ≤12 pgs, formato conferência |
| Pitch + técnica | ⏳ Pending | 5 min + 15 min |

## 4. Decisões Arquiteturais (TLC)

| # | Decisão | Data | Razão |
|---|---|---|---|
| D1 | Apenas Maceió no preditor | 2026-06-06 | 33% da base + viés populacional em outras cidades |
| D2 | Saída em 3 classes (baixa/média/alta) | 2026-06-06 | Honestidade epistemológica (não promete probabilidade) |
| D3 | Sem IBGE no MVP | 2026-06-06 | Tercis de contagem bastam para ranking; +1 dia economizado |
| D4 | Storage em CSV (não Parquet) | 2026-06-06 | Familiaridade do time; debug mais fácil |
| D5 | Top 5 cidades por volume CVLI | 2026-06-06 | Representam 48,7% dos registros |
| D6 | Stack Streamlit | 2026-06-06 | Python-only, curva rápida, 1-2 dias |
| D7 | Nada commitado em git | 2026-06-06 | Decisão do time: working tree only |

## 5. Critérios de Sucesso

- **Acadêmico:** doc SBC ≤12 pgs com 9 seções completas; 3 insights acionáveis; testes estatísticos sustentando H1-H4.
- **Técnico:** pipeline reproduzível (rodar `jupyter execute` do zero); ≥1 modelo com F1 macro ≥0.5; dashboard local funcional.
- **Pitch:** banca entende o problema em ≤30s; reconhece o valor da decisão proposta.

## 6. Riscos & Mitigações

| Risco | Mitigação |
|---|---|
| Geocoding impreciso para bairros | Usar centroides oficiais IBGE + flag de confiança |
| Preditor 3-classes com acurácia baixa | Ter fallback de "baixa confiança" no dashboard |
| Tempo de execução do Streamlit | Cache de agregados + agregação pré-processada |
| Dados faltantes em NI | Drop 2 cols críticas + benchmark de fill em NB01 |
