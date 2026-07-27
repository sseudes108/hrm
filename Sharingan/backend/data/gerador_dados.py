import pandas as pd
import random

def gerar_dados(n=10800):
    status_list = ["Aprovada", "Pendenciada", "Reprovada", "Fraude"]
    # Coordenadas aproximadas do Brasil (Lat: -33 a 5, Lng: -73 a -34)
    data = []
    for i in range(n):
        status = random.choices(status_list, weights=[70, 15, 10, 5])[0]
        risco = random.randint(85, 100) if status == "Fraude" else random.randint(0, 70)
        
        data.append({
            "id": i,
            "cliente": f"Cliente {i}",
            "valor": round(random.uniform(100, 50000), 2),
            "status": status,
            "lat": round(random.uniform(-30.0, -5.0), 4),
            "lng": round(random.uniform(-60.0, -35.0), 4),
            "risco_score": risco
        })
    
    df = pd.DataFrame(data)
    df.to_csv("dados_fraude.csv", index=False)
    print("CSV 'dados_fraude.csv' gerado com 10.800 registros.")

if __name__ == "__main__":
    gerar_dados()