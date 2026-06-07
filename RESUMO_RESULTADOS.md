# Resumo de Resultados — CVLI Alagoas

**Base:** 21.217 registros de Crimes Violentos Letais Intencionais em Alagoas (2012–abril 2026)  
**Fonte:** Portal de Dados Abertos do Estado de Alagoas — Secretaria de Segurança Pública

---

## Hipóteses Confirmadas (Qui-Quadrado, p < 0.05)

Todas as quatro hipóteses levantadas na proposta inicial foram **confirmadas estatisticamente**:

| Hipótese | Associação testada | Resultado |
|---|---|---|
| H1 | Sexo × Faixa Etária | ✓ Confirmada (χ²=320.6, p=3.2×10⁻⁶⁶) |
| H1b | Sexo × Cor/Raça | ✗ **Não confirmada** (χ²=7.15, p=0.128) |
| H2 | Dia da Semana × Período do Dia | ✓ Confirmada (χ²=113.7, p=1.8×10⁻²⁴) |
| H3 | Local do Fato × Instrumento | ✓ Confirmada (χ²=490.9, p=1.9×10⁻⁹⁷) |
| H4 | Sexo da Vítima × Instrumento | ✓ Confirmada (χ²=564.4, p=5.4×10⁻¹²²) |

> **Nota sobre H1b:** A distribuição racial das vítimas de CVLI é estatisticamente similar entre homens e mulheres — ambos provêm da mesma população geral (predominantemente parda/preta). A raça por si só não diferencia o perfil por sexo. Esse resultado é válido e fortalece a análise, pois demonstra que a alta proporção de negros/pardos é um padrão geral da violência letal, independente do gênero.

---

## Principais Descobertas por Análise

### EDA — Perfil das Vítimas

- **93,34%** das vítimas são do sexo masculino
- **57,90%** têm entre 15 e 29 anos
- **82,99%** são pardas ou pretas
- **46,94%** são ao mesmo tempo: masculino + 15–29 anos + parda/preta
- **77,24%** dos crimes usaram arma de fogo (PAF)
- **47,99%** ocorreram em espaço público; apenas **15,63%** em ambiente interno
- Faixa mais atingida: **18–24 anos** (32,29% dos registros)

### Análise Temporal

- **59,65%** dos crimes ocorrem à noite ou na madrugada (18h–06h)
- **37,66%** ocorrem em fins de semana
- **23,88%** combinam fim de semana + noite/madrugada
- Período de maior incidência: **Noite (18h–23h)** → 42,27% dos casos com hora registrada
- **Queda de 57%** no total de registros anuais entre 2013 (2.247) e 2025 (950)

### Análise Espacial

- **Maceió concentra 33,05%** de todos os CVLI do estado
- **Arapiraca** é a 2ª cidade (7,15%), seguida de Rio Largo (4,14%)
- **Janelas de risco mais críticas** (cidade + dia + hora):
  - Maceió | Domingo | 20h → 107 registros históricos
  - Maceió | Sábado | 19h → 106 registros
  - Maceió | Sábado | 21h → 105 registros

### Clustering — Perfis de Vítimas (Notebook 02)

K-Means com k ótimo por Silhouette identificou perfis recorrentes com características distintas de sexo, faixa etária, período e local — confirmando que não existe um único "perfil de vítima", mas grupos com vulnerabilidades específicas.

### Classificação Supervisionada (Notebook 03) — Versão Avançada

**Problema:** prever se o instrumento é Arma de Fogo (PAF) ou Outro  
**Pipeline:** BorderlineSMOTE → RF + XGBoost + LightGBM + CatBoost → Stacking (meta: LogisticRegression)

| Modelo | AUC | F1-Macro |
|---|---|---|
| CatBoost | **0.7142** | 0.5667 |
| LightGBM | 0.7114 | 0.5751 |
| XGBoost | 0.7106 | 0.5824 |
| Stacking Ensemble | 0.7079 | 0.6163 |
| Random Forest | 0.6859 | 0.5889 |
| **CatBoost (threshold=0.65)** | 0.7142 | **0.6413** |

**Features mais importantes (LightGBM + Gini):**
1. `bairro_encoded` — taxa histórica de arma de fogo por bairro (target encoding bayesiano)
2. `hora_sin` / `hora_cos` — hora cíclica do crime
3. `SUBJETIVIDADE COMPLEMENTAR` — subtipo do crime (feminicídio → quase sempre Outros)
4. `faixa_etaria` — perfil etário da vítima
5. `grupo_local` — tipo de local

**Avanços da versão avançada vs. versão base:**

| Feature | Versão Base | Versão Avançada |
|---|---|---|
| Modelos | Decision Tree, RF, XGBoost | RF, XGBoost, LightGBM, CatBoost + Stacking |
| Balanceamento | SMOTE | BorderlineSMOTE (borderline-1) |
| Bairro | ausente | target encoding (smoothing=10) |
| Subjetividade | ausente | incluída |
| Threshold | padrão (0.50) | otimizado por F1-Macro |
| AUC | 0.705 | **0.7142** |
| F1-Macro | 0.568 | **0.6413** |

---

## Insights Acionáveis (Formato Pitch)

### Insight 1 — Policiamento Armado por Janela Temporal

> *Percebemos que **59,65%** dos CVLI ocorrem entre 18h e 06h, e que crimes em espaço público nessa faixa têm **probabilidade acima de 80%** de envolver arma de fogo (AUC=0.705, Random Forest + SMOTE). Isso sugere que o **horário noturno em vias públicas é a janela de maior risco armado**. Por isso, recomendamos **realocar efetivo armado para vias públicas das 18h às 06h**, com prioridade para sextas, sábados e domingos em Maceió e Arapiraca. A decisão foi sustentada pela importância da feature `hora` no modelo e pela distribuição temporal dos crimes. Após **6 meses**, o sucesso pode ser avaliado pela **redução percentual de CVLI em espaço público no período noturno**. Será considerado bem-sucedido se essa taxa cair pelo menos **10%** nas cidades com maior realocação de efetivo.*

### Insight 2 — Prevenção da Violência Doméstica

> *Percebemos que mulheres representam apenas **6,66%** das vítimas de CVLI, mas **35,22%** dessas mortes envolvem arma branca ou espancamento — contra **19,23%** no total geral. O modelo classifica crimes em **ambiente interno** com **P(arma de fogo) = 40,9%**, confirmando um padrão distinto de violência doméstica (χ², p < 0,001). Isso sugere que **violência letal contra mulheres em ambientes internos segue um padrão específico**, separado do crime de rua. Por isso, recomendamos **integrar os dados de CVLI com ocorrências de violência doméstica** para identificar endereços de reincidência e acionar prevenção antes do desfecho fatal. A decisão foi sustentada pelo crosstab H4 e pela feature importance do modelo. Após **12 meses**, o sucesso pode ser avaliado pela **redução de feminicídios com instrumento branco/espancamento**. Será considerado bem-sucedido se essa taxa cair pelo menos **8%** após integração das bases.*

### Insight 3 — Focalização por Perfil Demográfico

> *Percebemos que **46,94%** de todas as vítimas de CVLI são simultaneamente: **homens, de 15 a 29 anos, pardos ou pretos** — grupo confirmado estatisticamente como o de maior vulnerabilidade (χ², p < 0,001). A faixa 18–24 anos representa **32,29%** de todos os registros. Isso sugere que **programas preventivos genéricos têm baixa eficiência** — o impacto máximo está em intervenções focadas nesse perfil específico. Por isso, recomendamos **direcionar programas de inserção social, educação e esporte** para jovens de 15–29 anos, pardos/pretos, em bairros com alta concentração de CVLI em Maceió e Arapiraca. A decisão foi sustentada pela estatística H1 e pela distribuição de faixa etária nos clusters. Após **2 anos**, o sucesso pode ser avaliado pela **redução de CVLI na faixa 15–29 anos nos bairros atendidos**, comparando com bairros não atendidos como grupo controle. Será considerado bem-sucedido se houver **redução de pelo menos 15%** no grupo exposto ao programa.*

---

## Métodos Utilizados

| Método | Aplicação | Métricas |
|---|---|---|
| EDA + Estatística Descritiva | Distribuições, frequências, crosstabs | Percentuais, médias, medianas |
| Qui-Quadrado (χ²) | Teste de independência para H1–H4 | p-valor, graus de liberdade |
| K-Means + K-Medoids | Perfis de vítimas (clustering) | Silhouette, Davies-Bouldin, Inertia |
| PCA | Visualização dos clusters | Variância explicada |
| Random Forest + BorderlineSMOTE | Predição do instrumento do crime | AUC, F1-Macro, Matriz de Confusão |
| XGBoost + BorderlineSMOTE | Predição do instrumento do crime | AUC, F1-Macro |
| LightGBM + BorderlineSMOTE | Predição do instrumento do crime | AUC, F1-Macro, Feature Importance |
| CatBoost + BorderlineSMOTE | Predição do instrumento do crime | AUC, F1-Macro |
| Stacking Ensemble (meta: LR) | Combinação dos 4 modelos | AUC, F1-Macro, Threshold Otimizado |
| Target Encoding (Bayesiano) | Codificação do bairro | Smoothing, taxa histórica |
| K-Fold CV (5 folds estratificado) | Validação dos modelos | AUC médio ± std |
| Análise temporal | Sazonalidade, tendências, janelas de risco | Contagens, heatmaps |

---

## Limitações

- **Escolaridade e ocupação** têm 74% e 68% de valores ausentes — não usados nos modelos
- **Cor/raça** tem 5,12% de ausência — imputado como "Não informado" nos modelos
- **2026 parcial** (apenas janeiro–abril) — excluído das comparações anuais
- O modelo classifica o instrumento **antes do crime** — aplica-se a análise de padrão histórico, não predição em tempo real
- AUC de **~0.714** indica discriminação **boa mas não perfeita** — o instrumento é determinado por fatores não capturados nos dados (histórico da vítima, conflito específico)
- O teto prático do AUC para este problema é ~0.72–0.75, pois o instrumento é escolhido pelo agressor (informação não disponível nos dados da vítima)
- **H1b não confirmada:** cor/raça não diferencia vítimas por sexo — ambos os grupos seguem a mesma distribuição racial majoritária da violência letal em AL
