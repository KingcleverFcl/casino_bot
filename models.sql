CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT PRIMARY KEY,
    nickname TEXT NOT NULL,
    password TEXT NOT NULL,
    balance INTEGER DEFAULT 100,
    total_games INTEGER DEFAULT 0,
    vin_games INTEGER DEFAULT 0,
    percent_wins REAL DEFAULT 0.0
);