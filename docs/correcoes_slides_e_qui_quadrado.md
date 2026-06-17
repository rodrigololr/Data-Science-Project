# Correções: slides 8–9 e testes de hipótese (qui-quadrado)

## 1. Código do teste qui-quadrado (rodar no NB03 ou NB01)

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

df = pd.read_csv('data/processed/cvli_clean.csv')  # N = 20.369

def cramers_v(ct):
    chi2 = chi2_contingency(ct)[0]
    n = ct.values.sum()
    r, k = ct.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))

# H4 — instrumento depende do sexo da vítima
ct = pd.crosstab(df['SEXO DA VITIMA'], df['grupo_instrumento'])
chi2, p, dof, _ = chi2_contingency(ct)
print(ct.div(ct.sum(axis=1), axis=0).mul(100).round(1))
print(f"chi2={chi2:.1f}  dof={dof}  p={p:.2e}  V de Cramér={cramers_v(ct):.3f}")

# Concentração temporal — período do dia x dia da semana
ct2 = pd.crosstab(df['periodo_dia'], df['dia_semana'])
chi2, p, dof, _ = chi2_contingency(ct2)
print(f"chi2={chi2:.1f}  dof={dof}  p={p:.2e}  V={cramers_v(ct2):.3f}")
```

### Resultados obtidos (base limpa, N = 20.369)

| Teste | χ² | gl | p | V de Cramér |
|---|---|---|---|---|
| Sexo × grupo_instrumento (H4) | 551,2 | 3 | <10⁻¹¹⁸ | **0,165** |
| Período do dia × dia da semana | 350,1 | 18 | <10⁻⁶² | 0,076 |
| Fim de semana × período do dia | 107,0 | 3 | <10⁻²² | 0,072 |

Distribuição do instrumento por sexo (%):

| Sexo | Arma de fogo | Arma branca | Espancamento | Outros |
|---|---|---|---|---|
| Masculino | 80,6 | 13,0 | 5,1 | 1,3 |
| Feminino | 56,9 | 25,2 | 10,8 | 7,0 |

## 2. Parágrafo para o artigo (inserir no fim da Seção 3.4)

> Para verificar se os padrões descritos são estatisticamente significativos e não
> artefatos de amostragem, aplicou-se o teste qui-quadrado de independência. A
> associação entre o sexo da vítima e o instrumento utilizado é altamente
> significativa (χ²(3) = 551,2; p < 0,001; V de Cramér = 0,165): entre vítimas do
> sexo feminino, arma branca (25,2%) e espancamento (10,8%) são proporcionalmente
> mais frequentes do que entre as masculinas (13,0% e 5,1%), ao passo que a arma de
> fogo predomina entre homens (80,6% contra 56,9%). Esse resultado sustenta
> estatisticamente a hipótese de um perfil distinto de violência associado a vítimas
> femininas (Seção 1). As concentrações temporais também rejeitam a hipótese de
> independência — período do dia × dia da semana (χ²(18) = 350,1; p < 0,001) e fim de
> semana × período do dia (χ²(3) = 107,0; p < 0,001) — embora com tamanho de efeito
> fraco (V ≈ 0,07), indicando que o padrão é consistente, porém de magnitude modesta.

> Na Seção 6 (limitações), substituir/remover a frase
> "não foram aplicados testes de significância estatística", pois agora há testes.

## 3. Slide 8 — CORRIGIDO

**Antes:** título "92% DE PRECISÃO" / "XGBoost classifica riscos com alta acurácia".

**Depois:**

- **Título:** Modelo de Triagem de Risco por Perfil
- **Subtítulo (kicker):** PADRÃO ESTATÍSTICO, NÃO ADIVINHAÇÃO
- **Corpo:**
  - Um XGBoost Poisson estima a **taxa de risco relativo** por perfil
    (bairro × sexo × faixa etária × horário), normalizada pela população do Censo IBGE 2022.
  - Serve para **priorizar** onde olhar primeiro — é uma ferramenta de triagem,
    não uma bola de cristal.
  - As associações que embasam o risco são **estatisticamente significativas**
    (qui-quadrado, p < 0,001).

> Remover o "92%" como headline. Aquele número vem de um experimento de
> classificação com vazamento de alvo e o próprio artigo o desqualifica — exibi-lo
> como conquista contradiz o documento.

## 4. Slide 9 — CORRIGIDO (insight acionável)

- **Percebemos que** 60,36% dos CVLI ocorrem entre 18h e 5h, concentrados em
  manchas identificáveis em Maceió e outras 4 cidades (49,12% do estado).
- **Isso sugere que** o patrulhamento uniforme aloca recursos em zonas e horários de
  baixo risco — a magnitude exata desse desperdício permanece como hipótese a testar.
- **Por isso, recomendamos** um protocolo de patrulhamento preditivo dinâmico, por
  faixa de horário e microrregião.
- **Sustentado por:** concentração espaço-temporal evidenciada no heatmap e nos
  mapas, com associações confirmadas por teste qui-quadrado (p < 0,001) — **não**
  pelas métricas do classificador, otimistas por vazamento de alvo.
- **Após 6 meses,** avaliar pela redução de CVLI nos hotspots, acompanhando a taxa em
  áreas adjacentes (efeito de deslocamento). Bem-sucedido se houver queda de ≥10%,
  alinhado à literatura de *hot spots policing* (Sherman 1989; Weisburd 2016).

### Mudanças-chave no slide 9
- Número noturno: **59,65% → 60,36%** (base limpa, igual ao artigo).
- Removido "desperdiça ~40% dos recursos" como fato → vira hipótese.
- Removido "decisão sustentada pela acurácia de 92,42%" → substituído pela evidência
  espaço-temporal + qui-quadrado (consistente com o artigo).
