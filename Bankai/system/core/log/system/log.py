import datetime

DEBUG = True

def log(msg: str, t: str = "info", emoji: str = "📰"):
    if not DEBUG:
        return
        
    agora = datetime.datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
    # ljust(7) preenche com espaços à direita para manter a consistência visual
    tipo = t.upper().ljust(7) 
    
    print(f"[{agora}] - {tipo} - {emoji} - {msg}")