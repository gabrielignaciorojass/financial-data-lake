from extraction import extract_financial_data
from load_data import load_to_sql


def run_pipeline():
    print(">>> Iniciando Pipeline de Indicadores Financieros (Batch Diario)")
    
    # 1. EXTRAER (API Gobierno)
    df_indicadores = extract_financial_data()
    
    if not df_indicadores.empty:
        print(f">>> Se obtuvieron {len(df_indicadores)} indicadores críticos.")
        
        # 2. CARGAR (Aquí iría tu código de guardar en BD o CSV)
        # load_to_sql(df_indicadores) 
        
        # Por ahora, guardamos un CSV local para evidencia
        df_indicadores.to_csv("indicadores_hoy.csv", index=False)
        print(">>> Datos guardados localmente en 'indicadores_hoy.csv'")
    else:
        print(">>> No hay datos para procesar.")

if __name__ == "__main__":
    run_pipeline()