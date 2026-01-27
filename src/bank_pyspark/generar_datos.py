import csv
import random
from datetime import datetime, timedelta

# Configuración
NUM_TRANSACCIONES = 1000
CLIENTES = [f"Cliente_{i}" for i in range(1, 21)]
TIPOS = ["Transferencia", "Pago_Servicios", "Retiro_Cajero", "Compra_Web"]

print(f"Generando {NUM_TRANSACCIONES} transacciones (con errores intencionales)...")

with open('transacciones_banco.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id_transaccion", "cliente_id", "tipo", "monto", "fecha", "sucursal"])
    
    for i in range(NUM_TRANSACCIONES):
        transaccion_id = i + 1000
        cliente = random.choice(CLIENTES)
        tipo = random.choice(TIPOS)
        
        # --- SABOTAJE 1: DATOS NULOS (5% de probabilidad) ---
        # Simulamos que el sistema falló y no guardó el monto
        if random.random() < 0.05:
            monto = None 
        else:
            monto = round(random.uniform(10.0, 500000.0), 2)
        
        # Fecha aleatoria
        dias_atras = random.randint(0, 30)
        fecha = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        
        sucursal = random.choice(["Santiago_Centro", "Providencia", "Las_Condes", "Digital"])
        
        # Escribimos la fila
        row = [transaccion_id, cliente, tipo, monto, fecha, sucursal]
        writer.writerow(row)

        # --- SABOTAJE 2: DUPLICADOS (5% de probabilidad) ---
        # Simulamos un error de red que envía la misma transacción dos veces
        if random.random() < 0.05:
            writer.writerow(row) # Escribimos EXACTAMENTE lo mismo otra vez

print("¡Archivo 'transacciones_banco.csv' creado con datos SUCIOS!")