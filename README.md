# Projeto Final de Ciência de Dados - Análise de CVLI em Alagoas

**Universidade Federal de Alagoas (UFAL)**  
**Instituto de Computação (IC)**  
**Disciplina:** Ciência de Dados  

---

## 👥 Equipe
* **Antônio Guilherme da Silva**
* **Antônio Rodrigo Lima de Andrade Tenório**
* **Sandro Gomes Paulino**

---

## Sobre o Projeto
Este repositório contém o Projeto Final da disciplina de Ciência de Dados. O objetivo principal é aplicar técnicas de Ciência de Dados em uma base real, com foco na geração de conhecimento útil para apoiar uma tomada de decisão na área de Segurança Pública.

### Tema e Base de Dados
**Tema:** Segurança Pública, Criminologia e Análise de Padrões Sociais.  
**Base:** [CVLI AL - Base de Microdados (2012 a Abril de 2026)](https://dados.al.gov.br/catalogo/dataset/cvli-2012-a-2023-base-microdados) - Crimes Violentos Letais Intencionais no Estado de Alagoas.  
**Fonte:** Portal de Dados Abertos do Estado de Alagoas (Secretaria de Estado da Segurança Pública).  

O conjunto de dados apresenta uma relação nominal (microdados) atualizada das vítimas de CVLI (Homicídios, Latrocínios e Lesões Corporais Seguidas de Morte) no estado de Alagoas. A base abrange o período de 2012 até abril de 2026, possuindo mais de **21.000 registros** e diversas variáveis (categóricas e numéricas) que descrevem cada ocorrência de forma detalhada (data, hora, cidade, bairro, características da vítima, local do fato e instrumento utilizado).

---

## Objetivos e Problemas Analisados

O projeto visa responder a três possíveis problemas centrais:
1. **Perfilamento Dinâmico de Risco:** Existe um padrão claro entre o perfil demográfico da vítima (idade, raça, sexo e escolaridade), a localização geográfica (cidade/bairro) e o horário do crime? Podemos mapear essas "personas de risco" por região?
2. **Preditores do Instrumento do Crime:** As características socioeconômicas da vítima e o local do crime são fatores determinantes para o instrumento utilizado (ex: arma de fogo vs. arma branca/espancamento)?
3. **Análise Espaço-Temporal (Manchas Criminais):** Existem padrões de sazonalidade (dias da semana, meses do ano ou faixas de horário) associados a surtos de violência em microrregiões específicas do estado que precedem aumentos nos índices de CVLI?

### Tomada de Decisão Apoiada
O principal objetivo do projeto será fornecer *insights* acionáveis para gestores de segurança pública, apoiando decisões como:
* **Otimização do Patrulhamento:** Direcionamento dinâmico de policiamento ostensivo e blitzes alocando viaturas para bairros específicos em faixas de horário exatas.
* **Políticas Preventivas:** Direcionamento de campanhas de conscientização e inserção social voltadas para parcelas da população e locais de maior vulnerabilidade estatística.
* **Foco Investigativo:** Auxílio à Polícia Civil no cruzamento de padrões de *Modus Operandi* para otimizar inquéritos sobre conflitos de facções e violência estrutural.

---

## Metodologia e Tecnologias

Para a condução deste trabalho, avaliamos utilizar as seguintes técnicas de Ciência de Dados e Aprendizagem de Máquina:

* **Pré-processamento de Dados:** Limpeza, tratamento de valores faltantes (como registros "Não Informado" - NI), conversão e manipulação de atributos temporais, discretização de idades e codificação de variáveis categóricas (One-Hot Encoding).
* **Análise Exploratória de Dados (EDA):** Estatística descritiva cruzada, matriz de correlação e visualizações ricas (gráficos de distribuição, mapas de calor / heatmaps).
* **Modelagem Não-Supervisionada:** Clusterização (ex: K-Means ou DBSCAN) para descoberta de "perfis de vítimas" subjacentes.
* **Modelagem Supervisionada:** Classificação (ex: Random Forest, Árvores de Decisão ou XGBoost) para prever o tipo de crime/instrumento com base no local e horário e identificar a importância de cada variável (feature importance).
* **Validação e Métricas:** Avaliação dos modelos utilizando técnicas como K-Fold Cross-Validation, Matriz de Confusão, Acurácia, Precisão, Revocação (Recall) e F1-Score.

---

## Estrutura Inicial do Repositório

* `cvli-microdados-alagoas-2012-a-abril-de-2026.csv`: Base de dados selecionada para o projeto.
* `proposta_inicial.md`: Documento contendo a proposta inicial da equipe com a justificativa, problemas e hipóteses iniciais.
* `descricao_projeto.md`: Documento contendo as diretrizes e regras da disciplina para a confecção do Projeto Final.
* `Projeto (2026-1).pdf`: Material de apoio contendo orientações do projeto.
