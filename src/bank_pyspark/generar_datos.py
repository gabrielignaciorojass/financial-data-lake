import csv
import random
from datetime import datetime, timedelta

# Configuración
NUM_TRANSACCIONES = 1000  # Puedes subirlo a 100,000 para probar "Big Data" real
CLIENTES = [f"Cliente_{i}" for i in range(1, 21)] # 20 Clientes
TIPOS = ["Transferencia", "Pago_Servicios", "Retiro_Cajero", "Compra_Web"]

print(f"Generando {NUM_TRANSACCIONES} transacciones falsas...")

with open('transacciones_banco.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Header (Encabezados)
    writer.writerow(["id_transaccion", "cliente_id", "tipo", "monto", "fecha", "sucursal"])
    
    for i in range(NUM_TRANSACCIONES):
        transaccion_id = i + 1000
        cliente = random.choice(CLIENTES)
        tipo = random.choice(TIPOS)
        monto = round(random.uniform(10.0, 500000.0), 2)
        
        # Fecha aleatoria en el último mes
        dias_atras = random.randint(0, 30)
        fecha = (datetime.now() - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
        
        sucursal = random.choice(["Santiago_Centro", "Providencia", "Las_Condes", "Digital"])
        
        writer.writerow([transaccion_id, cliente, tipo, monto, fecha, sucursal])

print("¡Archivo 'transacciones_banco.csv' creado exitosamente!")