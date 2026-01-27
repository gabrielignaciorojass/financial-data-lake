# 🏦 Financial Data Lake & Economic Indicators ETL

Este proyecto implementa una arquitectura de datos híbrida diseñada para simular operaciones críticas de un Banco Retail. Combina el procesamiento masivo de transacciones locales (Big Data) con la ingesta de indicadores económicos en la nube (Cloud Data Engineering).

## 📋 Descripción del Negocio

El sistema resuelve dos necesidades fundamentales de la banca moderna:
1.  **Análisis Transaccional (Core Bancario):** Procesamiento de grandes volúmenes de transacciones para detectar fraude, calcular riesgo crediticio y medir eficiencia operativa.
2.  **Tesorería y Riesgo de Mercado:** Actualización diaria de indicadores económicos críticos (UF, Dólar) necesarios para la valoración de pasivos y créditos hipotecarios.

---

## 🏗 Arquitectura del Proyecto

El repositorio opera como un **Monorepo** con dos pipelines desacoplados:

### Módulo 1: Bank Data Lake (PySpark)
Motor de procesamiento distribuido contenedorizado.
* **Ingesta (Bronze):** Generación de datos sintéticos con inyección controlada de errores (ruido/calidad).
* **Limpieza (Silver):** Pipeline de Calidad de Datos que elimina duplicados y nulos, particionando la data por fecha (`Hive Style Partitioning`).
* **Explotación (Gold):** Cálculo de KPIs de negocio:
    * 🚨 **Alerta de Fraude:** Detección de movimientos inusuales (AML).
    * 💎 **Clientes VIP:** Scoring para fidelización y aumento de cupo.
    * 🏢 **Eficiencia de Sucursales:** Métricas operativas.

### Módulo 2: Indicadores Económicos (Python + AWS)
ETL de misión crítica para datos de mercado.
* **Extracción:** Conexión a la API de `mindicador.cl` (Fuente oficial Banco Central de Chile).
* **Indicadores:** UF, Dólar Observado, Euro, UTM.
* **Carga:** Persistencia histórica en **AWS RDS (PostgreSQL)** para consumo de sistemas financieros.

---

## 🛠 Tech Stack

* **Lenguaje:** Python 3.9
* **Big Data:** Apache Spark (PySpark)
* **Infraestructura:** Docker & Docker Compose
* **Nube:** AWS RDS (PostgreSQL), AWS S3
* **Calidad de Datos:** Scripts de auditoría automatizada
* **Versionamiento:** Git / GitHub

---

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
* Docker Desktop instalado y corriendo.
* Archivo `.env` configurado con credenciales de AWS.

### 1. Ejecutar Pipeline Bancario (Data Lake)
Este comando genera datos, los limpia, audita la calidad y calcula los KPIs.
```bash
docker run --rm -v ${PWD}/output:/app/output financial-etl sh -c "python src/bank_pyspark/generar_datos.py && python src/bank_pyspark/etl_limpieza.py && python src/bank_pyspark/calculo_kpis.py"
