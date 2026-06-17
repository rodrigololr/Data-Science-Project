"""Pagina 3 - Sobre (metodologia, limitações, fonte)."""
import streamlit as st

st.set_page_config(page_title="Sobre", page_icon="📊", layout="wide")
st.title("📊 Sobre o Projeto")

st.markdown(
    """
    ## Contexto
    
    Este dashboard é o resultado final do **Projeto de Ciência de Dados** (UFAL, 2026.1).
    A ferramenta evoluiu de um classificador simples para um **Sistema de Inferência de Risco Real**, 
    integrando modelos estatísticos avançados com inteligência artificial generativa.
    
    **Equipe:** Antônio Guilherme · Antônio Rodrigo · Sandro Gomes
    
    ---

    ## Metodologia de Risco Real
    
    ### 1. Modelo Preditivo (Poisson Regression)
    Diferente de modelos de classificação tradicionais, utilizamos a **Regressão de Poisson** 
    (via XGBoost) para estimar a **taxa esperada de ocorrências** por 100 mil habitantes. 
    Este método é o padrão-ouro na epidemiologia e criminologia para modelar eventos raros.

    ### 2. Denominador IBGE (Proxy Demográfico)
    Para calcular o risco real, não basta contar crimes. É necessário saber quantas pessoas daquele perfil 
    existem no local. Utilizamos a técnica de **Imputação por Proporção**:
    - Cruzamos a população total por bairro (Censo 2022) com as proporções oficiais de Sexo e Faixa Etária de Maceió.
    - **Resultado:** O modelo entende, por exemplo, que o risco de um homem jovem é calculado sobre a 
      *estimativa de homens jovens* naquele bairro específico, e não sobre a população geral.

    ### 3. O Paradoxo do Risco (Volume vs. Taxa)
    Uma das maiores quebras de paradigma deste modelo é a diferença entre **Sensação de Perigo (Volume)** e **Risco Matemático (Taxa)**:
    - **O Viés do Volume:** Bairros como *Benedito Bentes* (110 mil hab.) e *Jacintinho* (73 mil hab.) lideram as estatísticas de volume bruto de crimes. A mídia foca nisso.
    - **A Realidade da Taxa:** O modelo de Poisson revela que o risco individual é diluído por essa massa populacional. Em contrapartida, bairros como *Bebedouro* (1.128 hab., fortemente esvaziado) ou o *Centro* (2.012 residentes, deserto à noite) possuem um volume menor de crimes, mas um denominador populacional minúsculo. 
    - **Conclusão:** Matematicamente, a chance individual de vitimização (Risco Relativo) é estratosfericamente maior nestes locais esvaziados do que nos bairros superpopulosos.

    ### 4. Calibração e Ranking
    O sistema classifica o risco como **BAIXA, MEDIA ou ALTA** comparando a estimativa individual com
    uma **Média de Referência Recalibrada (3.04)**. Essa média é baseada nos locais onde crimes 
    realmente ocorrem, garantindo que o ranking seja justo e reflita a periculosidade relativa real intra-grupo.

    ### 5. Explicabilidade (XAI + LLM)
    Utilizamos o algoritmo **SHAP (SHapley Additive exPlanations)** para abrir a "caixa-preta" do modelo.
    Os fatores que mais pesaram na sua estimativa são identificados matematicamente e enviados ao
    **Google Gemini**, que traduz os dados técnicos em uma explicação humana direta.

    ---

    ## Limitações & Ética
    
    1. **Dados Históricos:** O modelo reflete o passado (2012-2026). Mudanças recentes no policiamento 
       ou dinâmica urbana podem levar tempo para serem captadas.
    2. **Foco Geográfico:** O estimador é restrito a **Maceió** devido à disponibilidade de dados populacionais
       refinados por bairro.
    3. **Natureza Descritiva:** Esta ferramenta é um **instrumento estatístico** para auxílio em políticas públicas. 
       Não deve ser interpretada como uma "sentença" ou predição individual infalível.
    4. **Responsabilidade:** O uso desses dados deve ser feito com cautela ética para evitar o 
       reforço de estigmas territoriais ou sociais.

    ## Fonte de Dados
    - **Microdados de CVLI:** Secretaria de Segurança Pública de Alagoas (SSP/AL).
    - **Dados Populacionais:** Censo Demográfico 2022 (IBGE).
    - **Processamento:** Python 3.12, XGBoost, SHAP, Streamlit, Google Generative AI.
    """
)
st.caption("Projeto acadêmico · UFAL · Ciência de Dados · 2026.1")
