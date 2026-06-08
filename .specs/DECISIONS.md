# DECISÕES — Log do Projeto

> Toda decisão arquitetural passa por aqui. Formato: ADR simplificado.

## D1 — Preditor restrito a Maceió

**Data:** 2026-06-06
**Contexto:** Proposta inicial permitia 3 abordagens. Time decidiu focar no preditor pessoal.
**Decisão:** Modelo treinado SÓ em registros de Maceió (~7k de 21k).
**Razão:** Maceió = 33% da base + é a capital com maior viés urbano. Outras cidades têm amostras pequenas que gerariam overfitting e taxas ilusoriamente altas/baixas.
**Consequência:** Preditor só responde para Maceió no MVP. Outras cidades = "Modelo não treinado para esta cidade".
**Reversibilidade:** Média — pode-se treinar modelos por cidade individualmente (custo: +1 dia).

## D2 — Saída em 3 classes (baixa/média/alta)

**Data:** 2026-06-06
**Contexto:** Proposta original previa "probabilidade de assalto" — framing arriscado (CVLI ≠ assalto, e probabilidade individual é antiética).
**Decisão:** Saída do preditor é classe discreta: `{baixa, média, alta}`.
**Razão:** Honestidade epistemológica. CVLI é evento raro, modelo não pode prever "você vai ser vítima". Pode classificar perfil em tercis de risco histórico.
**Consequência:** Mais simples, sem denominador populacional obrigatório.
**Reversibilidade:** Alta — basta mudar limiares.

## D3 — Sem IBGE no MVP

**Data:** 2026-06-06
**Contexto:** Risco pessoal real precisaria de população por (cidade, idade, sexo) para taxa por 100k.
**Decisão:** NÃO integrar censo IBGE no MVP.
**Razão:** Com saída em 3 classes via tercis de contagem observada, IBGE não é estritamente necessário. Economiza 1 dia. Documenta como "trabalho futuro".
**Consequência:** Preditor mede **concentração relativa**, não risco absoluto. Aceitável para o pitch.
**Reversibilidade:** Alta — adicionar IBGE é mudança local em NB04.

## D4 — Storage em CSV

**Data:** 2026-06-06
**Contexto:** Parquet é mais eficiente, mas time não conhece.
**Decisão:** Manter CSV.
**Razão:** Familiaridade, debug trivial, ferramentas nativas pandas.
**Consequência:** Leitura um pouco mais lenta (21k linhas = irrelevante).
**Reversibilidade:** Trivial.

## D5 — Top 5 cidades por volume

**Data:** 2026-06-06
**Contexto:** HeatMap por bairro só faz sentido em cidades com volume estatístico.
**Decisão:** Maceió, Arapiraca, Rio Largo, União dos Palmares, Marechal Deodoro.
**Razão:** Top 5 concentram 48,7% dos CVLI. Abaixo disso, bairros têm <10 registros.
**Consequência:** Bairros de outras 97 cidades = agregado municipal apenas.
**Reversibilidade:** Baixa.

## D6 — Stack Streamlit

**Data:** 2026-06-06
**Contexto:** Dashboard precisa de mapa interativo + form de preditor.
**Decisão:** Streamlit + streamlit-folium.
**Razão:** Python-only, 1-2 dias para entregar, comunidade ativa.
**Alternativas descartadas:** Plotly Dash (curva maior), Flask+React (overhead).
**Reversibilidade:** Média.

## D8 — Segmentação coarsened para (sexo, faixa_etaria)

**Data:** 2026-06-06 (noite)
**Contexto:** Segmento original era (sexo, idade, bairro) — 50+ bairros em Maceió = segmentation extrema e leakage total.
**Decisão:** Usar apenas (sexo, faixa_etaria) como dimensões do segmento de lookup.
**Razão:** Faixa etária (7 níveis) preserva informação demográfica útil. Bairro removido do target por ser geográfico demais (territorializa o modelo).
**Consequência:** Tercis agora são por (sexo × faixa_etaria) com q33=61,24, q66=504,98 (agregado, não por perfil individual).
**Reversibilidade:** Alta.

## D9 — Honestidade metodológica sobre leakage

**Data:** 2026-06-06 (noite)
**Contexto:** Sub-agent @scientist review identificou target leakage estrutural — target é função direta das features demográficas do modelo. F1=0,997 reflete lookup, não generalização.
**Decisão:** Assumir honestamente que o modelo é uma **tabela de lookup do segmento (sexo, faixa_etaria)** com refinamento por contexto (período, dia, local, mês, hora). NÃO é um preditor genuíno.
**Razão:** Ético. Para um preditor genuíno seria preciso: (a) splits temporais (treino 2012-2022, teste 2023-2026), (b) target não derivado das features, (c) validação out-of-segment.
**Consequência:** Página `3_📊_Sobre.py` documenta explicitamente. README, STATE.md e `.notebook/sessions/2026-06-06_execucao_sdd.md` atualizados.
**Reversibilidade:** Trivial.

## D10 — Persistir LabelEncoder junto do modelo

**Data:** 2026-06-07 (sub-agent review 2)
**Contexto:** Sub-agent @scientist review 2 identificou que `LabelEncoder.fit(['baixa','media','alta'])` ordena ALFABETICAMENTE = `['alta','baixa','media']` → 0=alta, 1=baixa, 2=media. O wrapper antigo tinha `LABEL_DECODER = {0:'baixa', 1:'media', 2:'alta}'` hardcoded ERRADO, **invertendo silenciosamente todas as predições exibidas ao usuário**.
**Decisão:** Salvar `label_encoder.joblib` junto do modelo. Wrapper usa `le.inverse_transform()` em vez de decoder hardcoded.
**Razão:** Bug de segurança/UX — toda predição estava rotulada com classe trocada. Ético, dado D9 (compromisso de honestidade).
**Consequência:** `models/label_encoder.joblib` (~1KB). `meta['label_encoder_mapping']` documenta o mapping real. Predições do dashboard agora correspondem ao que o modelo realmente aprendeu.
**Reversibilidade:** Trivial.

## D7 — Sem commits git

**Data:** 2026-06-06
**Contexto:** Time quer revisar antes de qualquer versionamento.
**Decisão:** Tudo no working tree. ZERO commits, ZERO branches, ZERO push.
**Razão:** Decisão explícita do time. Nada em `.git/` é tocado.
**Consequência:** Estado do projeto = working tree. Backup é responsabilidade do usuário.
**Reversibilidade:** Trivial — time pode commitar quando quiser.
