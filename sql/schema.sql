-- Crea la tabla si no existe
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price_usd DECIMAL(18, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crea un índice para buscar rápido por fecha 
CREATE INDEX IF NOT EXISTS idx_timestamp ON crypto_prices(timestamp);