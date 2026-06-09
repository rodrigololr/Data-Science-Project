# ADR: Preditor de Risco Real (Poisson + IBGE)

## Contexto
O modelo inicial de classificação por tercis de contagem era enviesado: ele rotulava perfis como "Alta" apenas pelo volume bruto de crimes, ignorando que perfis majoritários (ex: mulheres adultas) naturalmente têm mais registros sem que o risco individual seja necessariamente maior.

## Decisões

### D1: Mudança para Regressão de Poisson
**Status:** Decidido.
Substituímos o classificador Multiclasse por um **XGBRegressor com objetivo Poisson**.
- **Razão:** Poisson é estatisticamente superior para modelar contagens de eventos raros e permite prever uma **Taxa Contínua** em vez de apenas classes discretas.

### D2: Imputação por Proxy Demográfico (IBGE)
**Status:** Decidido.
Utilizamos a população do Censo 2022 por bairro cruzada com as proporções de Sexo/Idade oficiais de Maceió.
- **Fórmula:** `populacao_perfil = populacao_bairro * prop_sexo * prop_faixa_etaria`.
- **Razão:** Garante que o denominador do risco seja condizente com o subgrupo demográfico, gerando a **Taxa Real por 100k habitantes** específica do perfil.

### D3: Recalibração de Média de Referência
**Status:** Decidido.
A classificação de risco (Baixa/Média/Alta) agora usa como base a **média das predições em locais com crimes reais (3.04)**.
- **Razão:** Evita que a vastidão de locais "seguros" (zeros no grid) puxe a média da cidade para perto de zero e cause um falso positivo de "Risco Alto" em quase todos os testes.

### D4: Integração de XAI (SHAP) + LLM (Gemini)
**Status:** Decidido.
Utilizamos SHAP para extrair as 3 features de maior impacto e o Google Gemini para gerar a explicação textual.
- **Razão:** Transparência algorítmica. O usuário entende *por que* seu risco foi classificado daquela forma.

### D5: Arquitetura Modular (Separation of Concerns)
**Status:** Decidido.
Código dividido em `ai_engine.py`, `ui_components.py`, `domain.py`, `utils.py` e `predictor.py`.
- **Razão:** Manutenibilidade e conformidade com padrões de engenharia de software sênior.

## Consequências
- Aumento na precisão estatística do ranking de risco.
- Eliminação do viés de volume bruto.
- Interface mais limpa e informativa.
- Dependência externa da API Key do Google AI Studio para explicações.
