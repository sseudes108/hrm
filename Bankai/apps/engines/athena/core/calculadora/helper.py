import pandas as pd

def hora_para_bloco(hora_str: str, sla_minutos: int) -> int:
    """Converte '08:00' para o bloco correspondente (ex: 16)."""
    try:
        h, m = map(int, hora_str.split(":"))
        total_minutos = (h * 60) + m
        return int(total_minutos / sla_minutos)
    except Exception:
        # Fallback seguro caso o usuário digite besteira (ex: "8h")
        return 0 
    
def hora_para_minuto(hora_str: str) -> int:
    """Transforma '08:00' ou '0800' no minuto absoluto do dia (ex: 480)."""
    if not hora_str: return 0
    h_limpa = str(hora_str).strip()
    if ":" not in h_limpa and len(h_limpa) >= 3:
        h_limpa = f"{h_limpa[:-2]}:{h_limpa[-2:]}"
    try:
        h, m = map(int, h_limpa.split(":"))
        return (h * 60) + m
    except:
        return 0
    
def minuto_para_hora(minuto: int) -> str:
    if pd.isna(minuto): return "--:--"
    h = (int(minuto) // 60) % 24
    m = int(minuto) % 60
    return f"{h:02d}:{m:02d}"