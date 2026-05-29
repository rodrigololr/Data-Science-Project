# Proposta Inicial de Projeto Final - Ciência de Dados

## 1. Nome e Tema da Base
**Base:** CVLI AL - BASE DE MICRODADOS 🚨 (Crimes Violentos Letais Intencionais no Estado de Alagoas).
**Tema:** Segurança Pública, Criminologia e Análise de Padrões Sociais.

## 2. Origem dos Dados
**Fonte:** Portal de Dados Abertos do Estado de Alagoas (Secretaria de Estado da Segurança Pública).
**Link:** [https://dados.al.gov.br/catalogo/dataset/cvli-2012-a-2023-base-microdados](https://dados.al.gov.br/catalogo/dataset/cvli-2012-a-2023-base-microdados)

## 3. Descrição Geral da Base
O conjunto de dados apresenta uma relação nominal (microdados) atualizada das vítimas de CVLI (Homicídios, Latrocínios e Lesões Corporais Seguidas de Morte) no estado de Alagoas. A base utilizada abrange o período de 2012 até abril de 2026. Ela possui mais de **21.000 registros** e diversas variáveis (categóricas e numéricas) que descrevem cada ocorrência de forma detalhada, incluindo: data, hora, cidade, bairro, características da vítima (sexo, cor/raça, idade, escolaridade, ocupação), local do fato e instrumento utilizado. É uma base robusta que espelha dados reais da criminalidade estadual.

## 4. Justificativa da Escolha
A segurança pública é um dos problemas estruturais de maior impacto social e econômico no Brasil, em especial no estado de Alagoas. Escolhemos esta base pela sua **relevância inquestionável e pelo impacto potencial dos resultados**. Analisar os microdados de mortalidade violenta vai muito além de um exercício puramente acadêmico; trata-se de buscar padrões ocultos que podem literalmente salvar vidas ao direcionar políticas públicas mais eficientes.
Do ponto de vista técnico de Ciência de Dados, o dataset é rico e desafiador. Ele possui tamanho substancial (mais de 21 mil linhas), uma ótima diversidade de variáveis (categóricas, temporais e geográficas) e exigirá um forte trabalho de limpeza e pré-processamento, especialmente para tratar valores nulos e inconsistentes (registros marcados como "Não Informado" - NI), o que se alinha perfeitamente com as exigências da disciplina.

## 5. Problema que será analisado
Como ainda estamos na fase de ideação, levantamos três possíveis problemas centrais que podem ser respondidos (ou combinados) com essa base de dados:

*   **Abordagem 1 - Perfilamento Dinâmico de Risco:** Existe um padrão claro entre o perfil demográfico da vítima (idade, raça, sexo e escolaridade), a localização geográfica (cidade/bairro) e o horário do crime? Podemos mapear essas "personas de risco" por região?
*   **Abordagem 2 - Preditores do Instrumento do Crime:** As características socioeconômicas da vítima e o local do crime são fatores determinantes para o instrumento utilizado (ex: arma de fogo vs. arma branca/espancamento)? 
*   **Abordagem 3 - Análise Espaço-Temporal (Manchas Criminais):** Existem padrões de sazonalidade (dias da semana, meses do ano ou faixas de horário) associados a surtos de violência em microrregiões específicas do estado que precedem aumentos nos índices de CVLI?

## 6. Tipo de tomada de decisão que se pretende apoiar
O principal objetivo do projeto será fornecer *insights* acionáveis para gestores de segurança pública (como o comando da Polícia Militar e a Secretaria de Segurança). As decisões a serem apoiadas incluem:
*   **Otimização do Patrulhamento:** Direcionar o policiamento ostensivo e as blitzes de forma dinâmica, alocando viaturas para bairros específicos em faixas de horário exatas onde as predições indicam maior risco para o perfil populacional local.
*   **Políticas Preventivas:** Apoiar o Estado no direcionamento de campanhas de conscientização e inserção social especificamente voltadas para a parcela da população (idade/escolaridade/raça) e locais de maior vulnerabilidade estatística.
*   **Foco Investigativo:** Auxiliar a Polícia Civil a cruzar padrões de *Modus Operandi* (instrumento utilizado + local + horário) para otimizar inquéritos sobre conflitos de facções e violência estrutural.

## 7. Hipóteses iniciais levantadas pela equipe
*   **H1:** A esmagadora maioria das vítimas de CVLI é formada por homens jovens (15 a 29 anos), de cor/raça parda ou preta e com baixa escolaridade.
*   **H2:** Existe um pico significativo de ocorrências durante os finais de semana e no período noturno (madrugada).
*   **H3:** O uso de Projetil de Arma de Fogo (PAF) representa mais de 75% dos instrumentos de morte, sendo desproporcionalmente maior em vias públicas e em vítimas jovens do sexo masculino.
*   **H4:** Crimes envolvendo armas brancas ou espancamento têm maior correlação com ambientes internos (dentro de residências) e vítimas do sexo feminino, possivelmente indicando casos de feminicídio/violência doméstica.

## 8. Possíveis métodos que poderão ser utilizados
Para conduzir este trabalho, a equipe avalia utilizar as seguintes técnicas de Ciência de Dados e Aprendizagem de Máquina:

*   **Pré-processamento de Dados:** 
    * Tratamento de valores faltantes (substituição ou descarte de dados `NI`);
    * Conversão e manipulação de atributos temporais (criação de colunas como `Dia da Semana`, `Mês`, `Faixa de Horário`);
    * Discretização de idades (transformação de idade contínua em faixas etárias);
    * Codificação (One-Hot Encoding) de variáveis categóricas.
*   **Análise Exploratória (EDA):** Estatística descritiva cruzada, matriz de correlação (para variáveis codificadas) e visualizações ricas (gráficos de distribuição, mapas de calor / *heatmaps* para horários vs. dias da semana).
*   **Modelagem Não-Supervisionada (Clusterização):** Aplicação de algoritmos como **K-Means** ou **DBSCAN** para descobrir grupos (clusters) subjacentes de "perfis de vítimas" que não são óbvios em uma análise manual.
*   **Modelagem Supervisionada (Classificação):** Treinamento de algoritmos de Machine Learning (como **Random Forest**, **Árvores de Decisão** ou **XGBoost**) para:
    1. Tentar prever o tipo de crime/instrumento com base no local e horário;
    2. Identificar a importância (feature importance) de cada variável (idade, sexo, região) no desfecho letal em horários de pico.
*   **Validação e Métricas:** Avaliação dos modelos utilizando técnicas como *K-Fold Cross-Validation*, Matriz de Confusão, Acurácia, Precisão, Revocação (Recall) e *F1-Score*.
