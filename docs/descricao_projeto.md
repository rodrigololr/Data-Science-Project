```
Universidade Federal de Alagoas
Instituto de Computação
Ciência de Dados
```
# Projeto Final

## Proposta

O projeto tem como objetivo aplicar técnicas de Ciência de Dados em uma
base escolhida pela equipe, com foco na geração de conhecimento útil para
apoiar uma tomada de decisão real ou simulada.

Além da parte técnica, o projeto deverá ser estruturado como um pitch, ou seja,
a equipe deve apresentar sua análise de forma clara, objetiva e convincente,
mostrando o valor dos dados para resolver um problema, identificar
oportunidades ou propor melhorias.

A equipe deverá selecionar uma base de dados, realizar sua análise
exploratória, aplicar técnicas estatísticas, métodos de mineração de dados e/ou
aprendizagem de máquina, e apresentar conclusões que possam ser utilizadas
para propor estratégias ou decisões fundamentadas nos dados.

O trabalho deverá contemplar três aspectos principais:

1. **Conteúdo técnico,** demonstrando domínio das etapas de análise,
    tratamento, modelagem e avaliação dos dados;
2. **Aplicação prática,** mostrando como os resultados encontrados podem
    apoiar uma tomada de decisão em um contexto real;
3. **Comunicação em formato de pitch,** apresentando o problema, os
    resultados e as recomendações de forma convincente, como se a
    equipe estivesse defendendo sua solução para um gestor, empresa,
    cliente ou banca avaliadora.

### Conjunto de Dados

A escolha da base de dados será livre, desde que esteja relacionada a um
problema que permita análise, extração de padrões e geração de insights
relevantes.

Não será permitido utilizar as bases de dados já utilizadas para as listas 1 e 2,
bem como não será permitido o uso da base “Hotel Booking", que vinha sendo


utilizada na disciplina. É permitido utilizar mais de uma base de dados, desde
que o conjunto atenda aos requisitos listados abaixo e produza um conjunto de
informações que permita a condução do trabalho. Espera-se que as bases de
dados não se repitam entre diferentes grupos, mas casos pontuais podem ser
discutidos.

A base poderá ser obtida em repositórios públicos, bases governamentais,
plataformas como Kaggle, UCI Machine Learning Repository, dados abertos ou
outras fontes confiáveis, desde que a origem seja clara e devidamente
referenciada no trabalho.

A base escolhida deve atender aos seguintes critérios:

1. **Tamanho mínimo**
    ○ Preferencialmente mais de **5.000 linhas** ;
    ○ Pelo menos **10 colunas úteis** para análise, desconsiderando IDs
       irrelevantes.
2. **Variedade de variáveis**
    ○ Deve conter variáveis numéricas e categóricas;
    ○ Deve ter pelo menos uma variável que possa ser usada como
       **resultado principal** da análise;
    ○ Deve conter variáveis que possibilitem exploração estatística e
       visual.
3. **Problema de negócio claro**
    ○ A base deve estar relacionada a um problema com potencial de
       tomada de decisão e permitir responder uma pergunta prática, por
       exemplo:
          ■ Como aumentar reservas?
          ■ Como reduzir cancelamentos?
          ■ Como prever vendas?
          ■ Como identificar clientes com maior chance de churn?
          ■ Como melhorar o desempenho de alunos, campanhas,
             produtos ou serviços?
4. **Potencial para modelagem**
    ○ A base deve permitir a aplicação de técnicas de Ciência de
       Dados, Mineração de Dados ou Aprendizagem de Máquina.
5. **Necessidade de preparação**
    ○ A base não deve estar “perfeita”;
    ○ Deve exigir pelo menos algumas etapas como tratamento de
       nulos, transformação de variáveis, criação de novas colunas,
       remoção de inconsistências ou análise de outliers.
6. **Potencial de insights**
    ○ A base precisa permitir gerar pelo menos **3 insights acionáveis** ,
       ou seja, recomendações que poderiam orientar uma decisão real.

A equipe deverá justificar a escolha da base, explicando o contexto do
problema, a origem dos dados e o tipo de decisão que pretende apoiar a partir
das análises.

**_Observação:_** Para alunos de mestrado, recomenda-se que a base utilizada
esteja relacionada ao seu tema de pesquisa.


### Objetivos

O objetivo principal do projeto é gerar conhecimento a partir dos dados e
utilizá-lo para apoiar uma tomada de decisão.

A equipe deverá apresentar uma proposta de aplicação prática dos resultados
encontrados, explicando como os insights obtidos podem auxiliar uma
organização, gestor, pesquisador ou usuário final.

O projeto deve responder a perguntas como:

```
● Qual problema está sendo analisado?
● Por que esse problema é relevante?
● Que padrões ou relações podem ser identificados nos dados?
● Que decisões podem ser tomadas com base nas análises?
● Como os resultados podem gerar impacto prático?
```
### Tipo de Insight Esperado

Espera-se que os alunos produzam insights acionáveis e que ultrapassem a
simples descrição dos dados. O projeto deve apresentar interpretações
capazes de apoiar decisões, identificar oportunidades, apontar riscos ou sugerir
melhorias.

Um bom insight deve ser claro, justificável e conectado ao problema analisado.
Ele deve surgir a partir da combinação entre análise estatística, visualização de
dados, modelagem e interpretação dos resultados. Além disso, deve sugerir
ações e definir indicadores de desempenho.

Exemplos de insights acionáveis com proposta de valor:

**Exemplo 1 — Hotel (números mais explícitos e diretos)**

_“Percebemos que reservas feitas com_ **_menos de 7 dias_** _de
antecedência apresentam_ **_taxa de cancelamento de 38%_** _, enquanto reservas
feitas com_ **_mais de 30 dias_** _de antecedência apresentam_ **_taxa de
cancelamento de 17%_**_. Isso sugere que reservas de última hora são mais
instáveis e aumentam o risco de ocupação não realizada. Por isso,
recomendamos criar uma_ **_campanha de incentivo à reserva antecipada_** _,
oferecendo benefício progressivo para clientes que reservarem com_ **_pelo
menos 30 dias de antecedência_**_. A decisão foi sustentada pela taxa de
cancelamento por antecedência da reserva e pelo ticket médio por grupo de
clientes._ **_Após 3 meses_** _, o sucesso da ação pode ser avaliado pela_ **_redução
da taxa de cancelamento_** _e acompanhado pela v_ **_ariação na taxa de
ocupação e no ticket médio_**_. A ação será considerada bem-sucedida se a_
**_taxa de cancelamento cair pelo menos 10%_** _no grupo impactado, sem
redução relevante no ticket médio.”_


**Exemplo 2 — Varejo/e-commerce (tom mais executivo)**

_“Percebemos que clientes que abandonam o carrinho_ **_após visualizar o
frete_** _representam uma_ **_parcela relevante das perdas de conversão_**_. Isso
sugere que_ **_o custo ou a percepção de custo da entrega está atuando
como barreira na etapa final da compra_**_. Por isso, recomendamos testar uma_
**_política de frete subsidiado_** _para compras acima de um valor mínimo,
priorizando categorias com maior margem. A decisão foi sustentada pela_ **_taxa
de abandono de carrinho na etapa de frete, pelo valor médio do pedido e
pela margem estimada por categoria_**_. Após 60 dias, o sucesso da ação pode
ser avaliado pelo_ **_aumento da taxa de conversão e acompanhado pela
margem líquida por pedido_**_. A ação será considerada bem-sucedida_ **_se
houver aumento de conversão sem deterioração da margem total da
operação_** _.”_

**Exemplo 3 — Educação, com foco analítico e social**

_“Percebemos que alunos com_ **_frequência inferior a 75%_** _têm
desempenho médio_ **_significativamente* menor_** _nas avaliações finais em
comparação aos alunos com frequência regular. Isso sugere que a_ **_baixa
presença é um indicador antecipado de risco acadêmico_** _e pode ser usada
para intervenção antes do fechamento do período letivo. Por isso,
recomendamos_ **_criar um acompanhamento preventivo_** _para alunos com
queda de frequência ao longo do bimestre, com contato ativo, reforço
direcionado e acompanhamento pedagógico. A decisão foi sustentada pela_
**_comparação entre frequência, nota final e taxa de aprovação_**_. Após um
bimestre, o sucesso da ação pode ser avaliado pela_ **_recuperação da
frequência_** _e acompanhado pela_ **_evolução das notas e da taxa de
aprovação_**_. Consideraremos a ação bem-sucedida se_ **_os alunos
acompanhados apresentarem aumento de frequência e melhora média de
desempenho_** _em relação ao período anterior ou a um grupo semelhante não
acompanhado.”_

***Cuidado com afirmações como esta, deve ser sustentado por teste estatístico**

De forma geral, um bom insight tem um formato semelhante a:

Percebemos que **[padrão nos dados]**. Isso sugere que **[interpretação do
problema ou oportunidade]**. Por isso, recomendamos **[ação prática]**. A
decisão foi sustentada por **[métrica/evidência usada na análise]**. Após
**[período]** , o sucesso da ação pode ser avaliado por **[métrica principal]** e
acompanhado por **[métrica auxiliar]**. A ação será considerada bem-sucedida
se **[critério objetivo de sucesso]**.


## Conteúdo Técnico

O documento do projeto deve apresentar, pelo menos, as seguintes seções:

### 1. Aplicação

Detalhamento da proposta do trabalho, incluindo o problema escolhido, a
justificativa da escolha, os objetivos a serem alcançados e a relação da análise
com uma possível tomada de decisão.

### 2. Base de Dados

Descrição da origem dos dados, contexto da base, quantidade de registros,
variáveis existentes e principais características.

Também devem ser descritas as técnicas de pré-processamento utilizadas,
como:

```
● limpeza dos dados;
● tratamento de valores ausentes;
● remoção ou tratamento de dados inconsistentes;
● integração de dados, se houver;
● transformação de variáveis;
● redução ou seleção de atributos, se necessário.
```
### 3. Estatística Descritiva e Inferência

Uso de estatísticas, tabelas, gráficos e visualizações para compreender melhor
os dados.

Esta seção deve apresentar análises como distribuição das variáveis, medidas
de tendência central, dispersão, correlações, comparações entre grupos e
demais informações relevantes para o problema estudado.

Quando adequado, a equipe deve utilizar testes de hipótese para apoiar
afirmações feitas a partir dos dados.

### 4. Métodos Avaliados

Descrição dos métodos utilizados no projeto, podendo incluir técnicas de:

```
● classificação;
● regressão;
● agrupamento;
● regras de associação;
● análise de séries temporais;
● redução de dimensionalidade;
● outros métodos relacionados à Ciência de Dados.
```

A equipe deve justificar a escolha dos métodos, relacionando-os ao objetivo do
projeto.

### 5. Métricas de Avaliação

Descrição das métricas utilizadas para avaliar os métodos aplicados.

Exemplos de métricas incluem:

```
● acurácia;
● precisão;
● revocação;
● F-measure;
● AUC;
● erro médio absoluto;
● erro quadrático médio;
● R²;
● matriz de confusão;
● outras métricas adequadas ao problema.
```
### 6. Métodos de Avaliação

Descrição da estratégia utilizada para avaliação dos modelos, como:

```
● divisão treino/teste;
● k-fold cross-validation;
● leave-one-out;
● bootstrap;
● validação temporal, quando aplicável.
```
A equipe deve explicar por que a estratégia escolhida é adequada para o
problema.

### 7. Resultados e Discussão

Apresentação dos principais resultados obtidos.

Esta seção deve demonstrar como os resultados justificam a proposta da
equipe, indicando se a solução é válida, funcional e eficiente.

Também devem ser discutidas as limitações da análise, possíveis problemas
encontrados e interpretações importantes.

Sempre que possível, os resultados devem ser conectados à tomada de
decisão proposta no projeto.
Além de apresentar os resultados técnicos, a equipe deverá explicitar qual
tomada de decisão está sendo recomendada a partir da análise realizada. Essa
decisão deve estar associada a uma métrica ou evidência quantitativa que


demonstre seu impacto. Por exemplo, a equipe pode recomendar uma ação
porque os dados indicam que ela reduz em X% a taxa de cancelamento de
reservas, aumenta em Y% a previsão de vendas, melhora em Z pontos a
acurácia do modelo ou reduz determinado risco identificado na base.

### 8. Conclusão

Resumo do que foi realizado no projeto, principais descobertas, limitações e
possibilidades de trabalhos futuros.

### 9. Bibliografia

Apresentação das obras, artigos, bases de dados, documentações e demais
referências consultadas ou citadas no trabalho.

### Estilo do Documento

O documento deve seguir o modelo de confecção de artigos para conferências
segundo a Sociedade Brasileira de Computação (SBC). O link [1] possui
modelos em doc e latex do site da SBC. O link [2] possui o modelo em latex da
Overleaf.

Modelos disponíveis:

#### [1]

https://www.sbc.org.br/documentos-da-sbc/summary/169-templates-para-artigo
s-e-capitulos-de-livros/878-modelosparapublicaodeartigos

#### [2]

https://pt.overleaf.com/latex/templates/sbc-conferences-template/blbxwjwzdngr

O documento final deve ter, no máximo, 12 páginas.


## Apresentação

A apresentação do trabalho terá tempo total de até **20 minutos** , organizados e
ordenados da seguinte maneira:
● **5 minutos** para o Pitch: apresentação em formato mais comercial,
voltada para cliente, gestor ou banca avaliadora.
● **15 minutos** para a apresentação técnica: explicação mais aprofundada
da base, metodologia, modelos, métricas, resultados e limitações..

A equipe deverá apresentar o trabalho mostrando de forma clara o problema
escolhido, a base utilizada, a metodologia aplicada, os principais resultados
encontrados e a decisão recomendada a partir da análise dos dados, em uma
linguagem compatível com cada tipo de apresentação.

Cada apresentação deve seguir uma linha lógica, por exemplo:

**Pitch:** problema identificado → oportunidade → principais evidências →
decisão proposta → impacto esperado.

**Apresentação técnica:** base utilizada → preparação dos dados →
métodos/modelos aplicados → métricas utilizadas → resultados obtidos →
limitações → justificativa da decisão final.

A equipe deve demonstrar que a decisão sugerida não surgiu apenas de uma
opinião, mas de evidências encontradas nos dados ou referências
consolidadas.

Durante o **pitch** , a equipe deverá apresentar sua solução como se estivesse
defendendo a proposta para um gestor, empresa, cliente ou banca avaliadora,
destacando o valor prático dos resultados obtidos. Já na **apresentação
técnica** , a equipe deverá aprofundar os aspectos metodológicos, explicando as
escolhas realizadas e sustentando tecnicamente os resultados apresentados.

Não é obrigatório que todos os integrantes falem durante a apresentação, mas
todos devem participar efetivamente da construção do trabalho. A equipe
poderá dividir as falas da forma que considerar mais adequada, incluindo
concentrar em um membro, desde que **todos** os integrantes estejam
**presentes** e **aptos a responder perguntas** sobre a base, a metodologia, os
resultados e a decisão proposta.


## Submissão

A entrega deverá ser realizada em duas partes, a saber:

### Parte 1 — Definição da Base e Proposta Inicial

Nesta etapa, a equipe deverá entregar um arquivo **PDF de até 2 páginas** com
a descrição inicial da base escolhida e da proposta de análise do projeto.

A entrega deve conter:

```
● nome ou tema da base (ou bases);
● origem dos dados (link);
● descrição geral da base;
● justificativa da escolha;
● problema que será analisado;
● tipo de tomada de decisão que se pretende apoiar;
● hipóteses iniciais levantadas pela equipe;
● possíveis métodos que poderão ser utilizados (não representa
compromisso para a entrega, apenas uma avaliação inicial).
```
Esta etapa valerá **2,0 pontos** e a entrega deverá ocorrer via **atividade da
turma virtual** após uma semana da proposta do projeto pelo docente da
disciplina.

### Parte 2 — Entrega Final

A entrega final será composta por um arquivo .zip ou .rar, entregue via
**atividade da turma virtual** , conforme cronograma da disciplina, contendo:

```
● documento final em PDF;
● código utilizado nos experimentos;
● apresentação;
● arquivos adicionais, caso existam.
```
As apresentações ocorrerão nas datas propostas pelo cronograma da
disciplina, em ordem a ser definida.

Esta etapa valerá **8,0 pontos** , distribuídos da seguinte forma:

```
● 5,0 pontos para a apresentação (pitch + técnica);
● 3,0 pontos para o documento final.
```

## Critérios de Avaliação

A avaliação será composta pelos seguintes critérios:

### Parte 1 — Definição da Base e Proposta Inicial

**2,0 pontos**

Serão avaliados:

```
● clareza na escolha da base;
● justificativa da escolha;
● relevância do problema e das hipóteses levantadas;
● potencial de geração de insights;
● relação inicial com tomada de decisão.
```
### Parte 2 — Apresentação

**5,0 pontos**

Serão avaliados:

```
● clareza na explicação do problema;
● domínio da base de dados;
● apresentação da metodologia;
● qualidade das análises e visualizações;
● interpretação dos resultados;
● relação entre os insights, as métricas obtidas e a tomada de decisão
proposta;
● clareza na justificativa da decisão recomendada, indicando qual ação
deve ser tomada e qual métrica evidencia sua melhoria ou impacto;
● organização e qualidade da comunicação.
```
### Parte 3 — Documento Final

**3,0 pontos**

Serão avaliados:

```
● estrutura do documento;
● descrição adequada da base;
● uso de estatística, visualização de dados, mineração de dados e/ou
aprendizagem de máquina;
● descrição dos métodos e métricas;
● apresentação dos resultados;
● discussão crítica;
● conclusão;
● referências.
```

### Pontuação Extra

A equipe poderá receber de **1,0 a 2,0 pontos** extras pela inclusão de recursos
adicionais que enriqueçam o projeto.

Exemplos de recursos extras:

```
● construção de dashboard interativo;
● aplicação web simples para visualização dos resultados;
● deploy de modelo;
● relatório automatizado;
● uso de técnicas avançadas de modelagem;
● integração com APIs;
● visualizações interativas;
● comparação aprofundada entre diferentes abordagens.
● integração e uso de LLMs
```
A pontuação extra será atribuída conforme a **qualidade** , **relevância** e **utilidade**
do recurso desenvolvido para o contexto do projeto.

## Observação Final

O projeto deve demonstrar a capacidade da equipe de transformar dados em
conhecimento útil para apoiar decisões. No entanto, é importante lembrar que o
foco **não deve estar apenas no conteúdo técnico**.

A equipe deve se atentar à **comunicação em formato de pitch e técnica** , nos
momentos adequados. Durante a apresentação, vocês precisam apresentar
bem o problema, mostrar como chegaram até ele por meio da análise dos
dados e defender a melhor solução encontrada. Em outras palavras: **vendam o
seu peixe.**

Por exemplo, se o problema identificado for uma queda no número de reservas
em períodos de baixa temporada, a equipe deve explicar **como** chegou a essa
conclusão, **quais gargalos** foram encontrados na base e **quais evidências**
sustentam essa análise. A partir disso, devem ser propostas **soluções
práticas** , como promoções, programas de fidelização, cashback, campanhas
direcionadas ou outras estratégias capazes de contornar o problema.

Assim, a apresentação deve deixar claro não apenas quais técnicas foram
utilizadas, mas principalmente como os resultados encontrados podem gerar
valor e orientar uma tomada de decisão fundamentada em dados.


