-- Create the finance_manager database if it doesn't exist
CREATE DATABASE IF NOT EXISTS finance_manager;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    balance FLOAT DEFAULT 0.0
);

-- Create the transactions table linked to users table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    description VARCHAR(255),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Create the debts table linked to users table
CREATE TABLE IF NOT EXISTS debts (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    description VARCHAR(255),
    debt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
