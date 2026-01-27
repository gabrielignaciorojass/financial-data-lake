# Financial Data Lake Project  📊

Este repositorio contiene implementaciones de Ingeniería de Datos utilizando Docker, AWS y Python.

## Estructura del Proyecto

El proyecto está modularizado en dos pipelines distintos:

### 1. Crypto ETL (`src/crypto_etl`)
Pipeline tradicional usando **Pandas** y **PostgreSQL**.
- Extracción de API de Criptomonedas.
- Carga hacia AWS S3 y Data Warehouse.

### 2. Bank Simulation (`src/bank_spark`)
Pipeline de Big Data simulado usando **Apache Spark (PySpark)**.
- Generación de datasets masivos de transacciones.
- Procesamiento distribuido y cálculo de KPIs con SQL.
- Almacenamiento en formato **Parquet**.

## Tecnologías
- **Core:** Python 3.9, Docker
- **Big Data:** Apache Spark (PySpark), Java 17
- **Cloud:** AWS S3 (boto3)