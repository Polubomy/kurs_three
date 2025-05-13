
-- 1. users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. clients table
CREATE TABLE clients (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(50),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. managers table
CREATE TABLE managers (
  code VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

-- 4. orders table
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  order_number VARCHAR(50) UNIQUE NOT NULL,
  client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  manager_code VARCHAR(10) REFERENCES managers(code),
  status VARCHAR(50) NOT NULL,
  contract_price NUMERIC(12,2),
  total_amount NUMERIC(12,2),
  order_type VARCHAR(100),
  items_description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  full_payment_date TIMESTAMPTZ,
  payment_status VARCHAR(50)
);

-- 5. order_items table
CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_name VARCHAR(200) NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  unit_price NUMERIC(12,2) NOT NULL
);


CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);
CREATE INDEX idx_orders_manager ON orders(manager_code);
