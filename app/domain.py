"""
Domain definitions and constants for the CVLI project.
Centralized source of truth for categorical values.
"""
from typing import List, Final

# Standard domain values used across models and UI
SEXOS: Final[List[str]] = ["Masculino", "Feminino"]
DIAS: Final[List[str]] = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
LOCAIS: Final[List[str]] = [
    "Ambiente interno", "Entorno de casa", "Espaco publico",
    "Area externa/isolada", "Outros",
]

# Risk classification levels
CLASSES_CANONICAS: Final[List[str]] = ["baixa", "media", "alta"]
