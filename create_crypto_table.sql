CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    coin TEXT,
    price FLOAT
);
