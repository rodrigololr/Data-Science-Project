import sys
import os
import pandas as pd
import numpy as np
import itertools
import unicodedata
import joblib
import json
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

# Adicionar o path do app para usar os helpers
sys.path.insert(0, 'app')
from predictor import (
    idade_para_faixa, hora_para_grupo, mes_para_grupo,
    SEXOS, DIAS, LOCAIS
)

def normalize(text):
    if not isinstance(text, str): return ""
    text = text.strip().upper()
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")

print("1. Carregando e Normalizando dados...")
cvli = pd.read_csv('data/processed/cvli_clean.csv', low_memory=False)
pop = pd.read_csv('data/geo/populacao_maceio_bairros.csv')

cvli = cvli[cvli['CIDADE DO FATO'] == 'Maceió'].copy()
cvli['bairro_norm'] = cvli['BAIRRO DO FATO'].apply(normalize)
pop['bairro_norm'] = pop['bairro'].apply(normalize)

# Bairros habitados
bairros_validos = pop[pop['populacao_2022'] > 0]['bairro'].unique()
bairros_norm_validos = [normalize(b) for b in bairros_validos]

print("2. Criando MATRIZ TOTAL de cenários (Grid)...")
# Faixas etárias do predictor.py
faixas = ["0-11", "12-17", "18-24", "25-29", "30-39", "40-59", "60+"]
# Turnos
turnos = ["Madrugada", "Manha", "Tarde", "Noite"]
# Trimestres
trimestres = ["T1", "T2", "T3", "T4"]

# Criar todas as combinações (Censo 2022)
grid = list(itertools.product(
    bairros_validos, SEXOS, faixas, DIAS, turnos, LOCAIS, trimestres
))

df_grid = pd.DataFrame(grid, columns=[
    'bairro_input', 'sexo_input', 'faixa_input', 
    'dia_input', 'hora_input', 'local_input', 'mes_input'
])
df_grid['bairro_norm'] = df_grid['bairro_input'].apply(normalize)

print(f"   Grid gerado com {len(df_grid):,} combinações.")

print("3. Agregando crimes reais sobre o Grid...")
# Preparar CVLI para o match
cvli['faixa_input'] = cvli['IDADE DA VITIMA'].apply(idade_para_faixa)
cvli['sexo_input'] = cvli['SEXO DA VITIMA']
cvli['bairro_input_norm'] = cvli['BAIRRO DO FATO'].apply(normalize)
cvli['dia_input'] = cvli['dia_semana']
cvli['local_input'] = cvli['grupo_local']
cvli['hora_input'] = cvli['hora'].apply(hora_para_grupo)
cvli['mes_input'] = cvli['mes'].apply(mes_para_grupo)

groupby_cols = ['sexo_input', 'faixa_input', 'bairro_input_norm', 'dia_input', 'local_input', 'hora_input', 'mes_input']
counts = cvli.groupby(groupby_cols).size().reset_index(name='crimes')

# Merge com o Grid (para garantir os ZEROS)
df = df_grid.merge(
    counts, 
    left_on=['sexo_input', 'faixa_input', 'bairro_norm', 'dia_input', 'local_input', 'hora_input', 'mes_input'],
    right_on=groupby_cols, 
    how='left'
)
df['crimes'] = df['crimes'].fillna(0)

print("4. Incorporando População (Denominador Específico) e Calculando Taxa...")
# 4.1. Traz a população total do bairro
df = df.merge(pop[['bairro_norm', 'populacao_2022']], on='bairro_norm', how='inner')

# 4.2. Mapeia os pesos demográficos de Maceió (Baseado nas imagens oficiais)
prop_sexo_map = {'Masculino': 0.468, 'Feminino': 0.532}
prop_faixa_map = {
    "0-11": 0.165, "12-17": 0.086, "18-24": 0.091, 
    "25-29": 0.081, "30-39": 0.156, "40-59": 0.256, "60+": 0.125
}

# 4.3. Cria os fatores multiplicadores para cada linha do grid
df['fator_sexo'] = df['sexo_input'].map(prop_sexo_map).fillna(0.5)
df['fator_faixa'] = df['faixa_input'].map(prop_faixa_map).fillna(0.1)

# 4.4. Calcula a população real daquele perfil específico no bairro
df['populacao_perfil'] = df['populacao_2022'] * df['fator_sexo'] * df['fator_faixa']

# Evita divisão por zero caso algum bairro venha sem população no censo
df['populacao_perfil'] = df['populacao_perfil'].replace(0, 1)

# 4.5. Fórmula: Taxa Anualizada por 100k habitantes DO MESMO PERFIL
anos_historico = cvli['ano'].nunique() if cvli['ano'].nunique() > 0 else 1
df['crimes_anuais'] = df['crimes'] / anos_historico

# Agora o denominador é a população do perfil, não mais a do bairro inteiro!
df['target_taxa'] = (df['crimes_anuais'] / df['populacao_perfil']) * 100000

print(f"   Taxa média encontrada para os perfis: {df['target_taxa'].mean():.4f}")

print("5. Treinando Modelo Poisson (XGBoost)...")
# Features do formulário original
features = ['bairro_input', 'sexo_input', 'faixa_input', 'dia_input', 'hora_input', 'local_input', 'mes_input']
X = df[features]
y = df['target_taxa']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), features)
    ]
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(
        objective='count:poisson', 
        n_estimators=100, # Reduzido para velocidade no grid grande
        learning_rate=0.1, 
        max_depth=5, 
        random_state=42
    ))
])

model.fit(X, y)

print("6. Salvando Artefatos...")
joblib.dump(model, 'models/preditor_poisson_final.joblib')

meta = {
    'modelo': 'Regressão de Poisson (Full Grid)',
    'media_cidade_taxa': float(y.mean()),
    'anos_historico': int(anos_historico),
    'features': features,
    'bairros_disponiveis': sorted(list(bairros_validos))
}

with open('models/preditor_poisson_final_meta.json', 'w') as f:
    json.dump(meta, f)

print("✅ Sucesso! O modelo agora entende o que é segurança (zeros) e o peso da população (ibge).")
