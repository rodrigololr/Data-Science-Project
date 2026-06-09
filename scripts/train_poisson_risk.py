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
from utils import (
    idade_para_faixa, hora_para_grupo
)
from domain import SEXOS, DIAS, LOCAIS

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

# Criar todas as combinações (Censo 2022) - REMOVIDO TRIMESTRES
grid = list(itertools.product(
    bairros_validos, SEXOS, faixas, DIAS, turnos, LOCAIS
))

df_grid = pd.DataFrame(grid, columns=[
    'bairro_input', 'sexo_input', 'faixa_input', 
    'dia_input', 'hora_input', 'local_input'
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

groupby_cols = ['sexo_input', 'faixa_input', 'bairro_input_norm', 'dia_input', 'local_input', 'hora_input']
counts = cvli.groupby(groupby_cols).size().reset_index(name='crimes')

# Merge com o Grid (para garantir os ZEROS)
df = df_grid.merge(
    counts, 
    left_on=['sexo_input', 'faixa_input', 'bairro_norm', 'dia_input', 'local_input', 'hora_input'],
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
df['populacao_perfil'] = df['populacao_perfil'].fillna(1).replace(0, 1)

# 4.5. Fórmula: Taxa Anualizada por 100k habitantes DO MESMO PERFIL
anos_historico = cvli['ano'].nunique() if cvli['ano'].nunique() > 0 else 1
df['crimes_anuais'] = df['crimes'] / anos_historico

# Agora o denominador é a população do perfil, não mais a do bairro inteiro!
df['target_taxa'] = (df['crimes_anuais'] / df['populacao_perfil']) * 100000

# CORREÇÃO DA MÉDIA: A média da cidade deve ser o total de crimes dividido pela população total
total_crimes_maceio = len(cvli)
populacao_total_maceio = pop['populacao_2022'].sum()
media_real_cidade = (total_crimes_maceio / anos_historico) / populacao_total_maceio * 100000

print(f"   Taxa média real de Maceió: {media_real_cidade:.4f}")

print("5. Treinando Modelo Poisson (XGBoost)...")
# Features do formulário original
features = ['bairro_input', 'sexo_input', 'faixa_input', 'dia_input', 'hora_input', 'local_input']
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
        n_estimators=150,
        learning_rate=0.05, 
        max_depth=5, 
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    ))
])

model.fit(X, y)

# 6. Salvando Artefatos...
# Cálculo da Média de Referência para Classificação (Recalibração Relativa ao Gênero)
# Usamos a média das predições nos dados REAIS de crime separados por sexo para ter uma base comparativa justa intra-grupo

mask_crimes = y > 0
preds_reais = model.predict(X[mask_crimes])

media_referencia_geral = float(np.mean(preds_reais))

# Média específica por sexo nos locais de crime
mask_masc = (X['sexo_input'] == 'Masculino') & mask_crimes
mask_fem = (X['sexo_input'] == 'Feminino') & mask_crimes

media_referencia_masculino = float(np.mean(model.predict(X[mask_masc]))) if mask_masc.sum() > 0 else media_referencia_geral
media_referencia_feminino = float(np.mean(model.predict(X[mask_fem]))) if mask_fem.sum() > 0 else media_referencia_geral

print(f"   Média de referência (Geral): {media_referencia_geral:.4f}")
print(f"   Média de referência (Homens): {media_referencia_masculino:.4f}")
print(f"   Média de referência (Mulheres): {media_referencia_feminino:.4f}")

joblib.dump(model, 'models/preditor_poisson_final.joblib')

meta = {
    'modelo': 'Regressão de Poisson (Full Grid)',
    'media_cidade_taxa': {
        'Geral': media_referencia_geral,
        'Masculino': media_referencia_masculino,
        'Feminino': media_referencia_feminino
    },
    'taxa_real_maceio': float(media_real_cidade),
    'anos_historico': int(anos_historico),
    'features': features,
    'bairros_disponiveis': sorted(list(bairros_validos))
}

with open('models/preditor_poisson_final_meta.json', 'w') as f:
    json.dump(meta, f)

print("✅ Sucesso! O modelo agora entende o que é segurança (zeros) e o peso da população (ibge).")
