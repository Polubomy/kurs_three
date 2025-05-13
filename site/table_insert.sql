-- 1. users
INSERT INTO users (email, password_hash) VALUES
('admin@example.com', 'pbkdf2:sha256:150000$abc$hashedpassword'),
('user1@example.com', 'pbkdf2:sha256:150000$def$hashedpassword');

-- 2. clients
INSERT INTO clients (name, email, phone, created_at) VALUES
('Иванов Иван Иванович', 'ivanov@example.com', '+7 910 123-45-67', '2025-01-15T10:00:00Z'),
('Петрова Мария Петровна', 'petrova@example.com', '+7 915 234-56-78', '2025-02-20T14:30:00Z'),
('Сидоров Алексей Николаевич', 'sidorov@example.com', '+7 920 345-67-89', '2025-03-05T09:15:00Z');

-- 3. managers
INSERT INTO managers (code, name) VALUES
('МД', 'Мария Дмитриевна'),
('АА', 'Александр Александрович'),
('АБ', 'Алена Борисовна');

-- 4. orders
INSERT INTO orders (order_number, client_id, manager_code, status, contract_price, total_amount, order_type, items_description, created_at, full_payment_date, payment_status) VALUES
('ORD-1001', 1, 'МД', 'В обработке', 150000.00, 150000.00, 'Офлайн', 'Станок токарный, Сверлильный станок', '2025-04-05T11:20:00Z', NULL, 'Не оплачен'),
('ORD-1002', 2, 'АА', 'Завершён', 250000.00, 250000.00, 'Онлайн', 'Компрессор промышленный', '2025-04-10T09:45:00Z', '2025-04-15T16:00:00Z', 'Оплачен'),
('ORD-1003', 3, 'АБ', 'В обработке', 175000.00, 175000.00, 'Офлайн', 'Насос промышленный, Станок фрезерный', '2025-04-20T13:30:00Z', NULL, 'Предоплата'),
('ORD-1004', 1, 'МД', 'Завершён', 300000.00, 300000.00, 'Онлайн', 'Станок шлифовальный', '2025-04-25T08:10:00Z', '2025-04-30T12:00:00Z', 'Оплачен');

-- 5. order_items
INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES
(1, 'Станок токарный', 1, 100000.00),
(1, 'Сверлильный станок', 1, 50000.00),
(2, 'Компрессор промышленный', 2, 125000.00),
(3, 'Насос промышленный', 3, 50000.00),
(3, 'Станок фрезерный', 1, 25000.00),
(4, 'Станок шлифовальный', 1, 300000.00);
