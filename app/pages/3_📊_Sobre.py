"""Pagina 3 - Sobre (metodologia, limitacoes, fonte)."""
import streamlit as st

st.set_page_config(page_title="Sobre", page_icon="📊", layout="wide")
st.title("📊 Sobre o Projeto")

st.markdown(
    """
    ## Contexto
    
    Este dashboard é parte do **Projeto Final da disciplina de Ciência de Dados**
    da Universidade Federal de Alagoas (UFAL), 2026.1.
    
    **Base de dados:** Crimes Violentos Letais Intencionais (CVLI) — Alagoas, 2012 a abril de 2026.
    **Fonte:** Secretaria de Estado da Segurança Pública de Alagoas (portal de dados abertos).
    **Equipe:** Antônio Guilherme · Antônio Rodrigo Tenório · Sandro Gomes Paulino.
    
    ## Metodologia
    
    ### Preditor (Tab 🎯)
    - Treinado **apenas com dados de Maceió** (~6.800 registros)
    - Classes definidas por **tercis de contagem histórica** por (sexo, faixa_etaria):
      - `baixa`: ≤33% percentil
      - `média`: ≤66% percentil
      - `alta`: >66% percentil
    - Features: sexo, idade, faixa_etaria, periodo_dia, dia_semana, grupo_local, mês, hora
    - Modelos testados: RandomForest, XGBoost, LogisticRegression
    - Validação: Stratified 5-fold cross-validation
    
    > **Aviso metodológico importante:** o target é derivado das próprias features
    > demográficas (segmento = sexo × faixa_etária). Isso significa que o modelo
    > funciona essencialmente como uma **tabela de lookup** do segmento, com
    > refinamento por contexto. A acurácia reportada (F1 macro ~0.99 em CV) reflete
    > isso, NÃO generalização preditiva para fora da amostra.
    > Para um preditor genuíno, seria necessário:
    > - Splits temporais (treino em 2012-2022, teste em 2023-2026)
    > - Targets não derivados das features
    > - Validação out-of-segment
    
    ### Mapa (Tab 🗺️)
    - Geocoding dos 102 municípios de Alagoas via centroide (capital)
    - HeatMap por bairro nas top 5 cidades por volume (Maceió, Arapiraca, Rio Largo, União dos Palmares, Marechal Deodoro)
    - Coordenadas de bairro: centroide da cidade + offset determinístico (limitação discutida abaixo)
    
    ## Limitações
    
    1. **Preditor = lookup disfarçado:** o modelo é essencialmente uma tabela de consulta
       do segmento. Para uma predição genuína, seria necessário outro desenho experimental.
    2. **Viés geográfico:** treinado SÓ em Maceió. Outras cidades têm amostras pequenas que gerariam
       estimativas instáveis. Por isso o preditor só responde para Maceió.
    3. **Coordenadas de bairro:** aproximadas (centroide + offset). Para uso operacional, seria
       necessário cruzar com shapefiles do IBGE ou Nominatim em batch.
    4. **Missing data:** duas colunas com >60% faltantes foram descartadas (Escolaridade, Ocupação).
       Imputação nessas colunas seria invenção.
    5. **Janela temporal 2026:** ano parcial (janeiro a abril) — séries temporais têm viés de subnotificação.
    6. **Acurácia inflada pelo leakage:** o F1 macro de ~0.99 reflete que o modelo aprendeu
       a identificar o segmento. Em uso real (perfil novo, fora do dicionário), a
       performance cairia drasticamente.
    
    ## Aspectos Éticos
    
    - Não prometemos "predição de vitimização" — prometemos ranking estatístico
    - O preditor não inclui variáveis socioeconômicas (renda, escolaridade) por decisão metodológica
    - O modelo é **descritivo do passado**, não prescritivo do futuro
    - Risco de uso indevido: este modelo pode reforçar estigmas se apresentado sem contexto
    - **Recomendação:** usar apenas para fins de planejamento de políticas públicas,
      nunca para vigilância individual
    
    ## Reprodutibilidade
    
    ```bash
    # Ambiente
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # Pipeline (em ordem)
    jupyter nbconvert --to notebook --execute notebooks/01b_data_quality.ipynb
    jupyter nbconvert --to notebook --execute notebooks/03_geo_temporal.ipynb
    jupyter nbconvert --to notebook --execute notebooks/04_preditor_maceio.ipynb
    
    # Dashboard
    streamlit run app/streamlit_app.py
    ```
    
    ## Stack
    
    Python · Pandas · Scikit-learn · XGBoost · SHAP · GeoPandas · Folium · Streamlit · Plotly
    
    ---
    """
)
st.caption("Projeto acadêmico · UFAL · Ciência de Dados · 2026.1")
