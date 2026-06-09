"""
Data Preprocessing Utilities - Discretization and normalization helpers.
"""

def idade_para_faixa(idade: int) -> str:
    """Converts numeric age to demographic categorical bins."""
    if idade < 12: return "0-11"
    if idade < 18: return "12-17"
    if idade < 25: return "18-24"
    if idade < 30: return "25-29"
    if idade < 40: return "30-39"
    if idade < 60: return "40-59"
    return "60+"

def hora_para_grupo(hora: int) -> str:
    """Groups 24h format into 4 main periods of day."""
    if hora < 6: return "Madrugada"
    if hora < 12: return "Manha"
    if hora < 18: return "Tarde"
    return "Noite"
