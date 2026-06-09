"""
AI Engine - Handles SHAP factor identification and Google Gemini integration.
"""
from __future__ import annotations
import os
import io
import pandas as pd
import shap
import streamlit as st
from typing import Any
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from data_loader import load_clean
from utils import hora_para_grupo

# Carregamento do .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Configuração do Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

@st.cache_data(show_spinner=False, ttl=3600)
def get_ai_explanation(_model: Any, X_json: str, taxa_predita: float, media_cidade: float) -> str:
    """
    Generates Natural Language explanation using SHAP and Google Gemini.
    """
    try:
        X = pd.read_json(io.StringIO(X_json))
        perfil = X.to_dict(orient='records')[0]
        
        # 1. SHAP Factor Identification
        preprocessor = _model.named_steps['preprocessor']
        xgb_model = _model.named_steps['regressor']
        
        X_transformed = preprocessor.transform(X)
        feature_names = preprocessor.get_feature_names_out()
        
        explainer = shap.TreeExplainer(xgb_model)
        shap_values = explainer.shap_values(X_transformed)
        
        contributions = pd.Series(shap_values[0], index=feature_names)
        top_factors = contributions.sort_values(ascending=False).head(3)
        
        tradutor = {
            'sexo': 'seu sexo', 'faixa': 'sua idade', 'bairro': 'este bairro específico',
            'dia': 'o dia da semana', 'local': 'o tipo de ambiente', 
            'hora': 'o horário'
        }

        fatores_limpos = [
            tradutor.get(f.replace('cat__', '').replace('_input', ''), f) 
            for f in top_factors.index
        ]
        fatores_str = ", ".join(fatores_limpos)

        # 2. Estatísticas do Mundo Real (Data-Driven Context)
        try:
            cvli = load_clean()
            maceio = cvli[cvli['CIDADE DO FATO'] == 'Maceió'].copy()
            maceio['bairro_norm'] = maceio['BAIRRO DO FATO'].astype(str).str.strip().str.upper()
            maceio['turno'] = maceio['hora'].apply(hora_para_grupo)
            
            bairro_alvo = perfil['bairro_input'].strip().upper()
            sexo_alvo = perfil['sexo_input']
            turno_alvo = perfil['hora_input']
            
            casos_bairro = len(maceio[maceio['bairro_norm'] == bairro_alvo])
            casos_sexo_bairro = len(maceio[(maceio['bairro_norm'] == bairro_alvo) & (maceio['SEXO DA VITIMA'] == sexo_alvo)])
            casos_exatos = len(maceio[(maceio['bairro_norm'] == bairro_alvo) & (maceio['SEXO DA VITIMA'] == sexo_alvo) & (maceio['turno'] == turno_alvo)])
            
            stats_context = (
                f"\nEstatísticas Reais do Dataset (14 anos em Maceió):\n"
                f"- Total de crimes letais no bairro {bairro_alvo}: {casos_bairro}\n"
                f"- Total de vítimas do sexo {sexo_alvo} no bairro {bairro_alvo}: {casos_sexo_bairro}\n"
                f"- Vítimas exatas (sexo {sexo_alvo} + bairro {bairro_alvo} + turno da {turno_alvo}): {casos_exatos}\n"
            )
        except Exception as e:
            stats_context = "" # Fallback se falhar a contagem

        # 3. Prompt Engineering Avançado
        prompt = (
            f"Aja como um Cientista de Dados e Especialista em Segurança Pública de Alagoas. "
            f"O modelo matemático calculou um risco de {taxa_predita:.1f} para este perfil "
            f"(a média de referência deste grupo é {media_cidade:.1f}). O risco relativo é {(taxa_predita/media_cidade) if media_cidade > 0 else 0:.1f}x a média.\n\n"
            f"Perfil Testado: {perfil['sexo_input']}, {perfil['faixa_input']} anos, bairro {perfil['bairro_input']}, ambiente: {perfil['local_input']}, turno: {perfil['hora_input']}.\n"
            f"Fatores matemáticos (SHAP) dominantes: {fatores_str}.\n"
            f"{stats_context}\n"
            f"Instrução Crucial:\n"
            f"Escreva exatamente 1 parágrafo fluido, analítico e jornalístico (3 a 4 frases) focado na CAUSA RAIZ (Root Cause) matemática desse resultado.\n"
            f"NUNCA use a estrutura repetitiva 'Como você é...'. NUNCA divida em tópicos.\n"
            f"CITE OBRIGATORIAMENTE os números exatos do 'Estatísticas Reais do Dataset' fornecidos acima para dar peso probatório à explicação "
            f"(ex: 'O algoritmo atribuiu esse nível de alerta porque em nossa base histórica de 14 anos cruzamos [X] casos...').\n"
            f"Conecte os dados à realidade urbana de forma séria e descritiva."
        )

        # 4. Call Google Gemini
        if not GEMINI_KEY:

            return "Erro: GEMINI_API_KEY não configurada no arquivo .env."

        # Modelo Gemini 1.5 Flash (Rápido e estável para explicações curtas)
        model_gemini = genai.GenerativeModel('gemini-3.1-flash-lite')
        
        response = model_gemini.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        
        return f"O Gemini não retornou texto. Análise técnica: Risco {taxa_predita:.1f} por concentração em {perfil['bairro_input']}."
            
    except Exception as e:
        return f"Falha na integração com o Gemini: {str(e)}"
