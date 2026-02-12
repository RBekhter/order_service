-- ========================================
-- Тестовые данные для разработки
-- ========================================

INSERT INTO category (id, name, parent_category_id) VALUES
  (1, 'Электроника', NULL),
  (2, 'Смартфоны', 1),
  (3, 'Планшеты', 1),
  (4, 'Ноутбуки', 1),
  (5, 'Аксессуары', 1),
  (6, 'Чехлы', 5),
  (7, 'Защитные стёкла', 5),
  (8, 'Зарядные устройства', 5),
  (9, 'Наушники', 5),
  (10, 'Бытовая техника', NULL),
  (11, 'Холодильники', 10),
  (12, 'Стиральные машины', 10);

INSERT INTO nomenclature (id, name, stock, price, category_id) VALUES

  (1, 'iPhone 15 Pro 256GB', 10, 79990.00, 2),
  (2, 'Samsung Galaxy S24 Ultra 512GB', 8, 85000.00, 2),
  (3, 'Google Pixel 8 Pro', 12, 65000.00, 2),
  (4, 'Xiaomi 14 Ultra', 15, 59990.00, 2),

  (5, 'iPad Pro 12.9" 256GB', 5, 120000.00, 3),
  (6, 'Samsung Galaxy Tab S9 Ultra', 7, 95000.00, 3),

  (7, 'MacBook Pro 16" M3 Max', 3, 299990.00, 4),
  (8, 'Dell XPS 15', 6, 150000.00, 4),

  (9, 'Чехол кожаный для iPhone', 50, 2990.00, 6),
  (10, 'Защитное стекло 9H (2 шт.)', 100, 990.00, 7),
  (11, 'Зарядное устройство 65W GaN', 30, 3500.00, 8),
  (12, 'AirPods Pro 2', 20, 24990.00, 9),
  (13, 'Силиконовый чехол для Samsung', 45, 1990.00, 6),

  (14, 'Холодильник LG GR-B247', 4, 65000.00, 11),
  (15, 'Стиральная машина Bosch WAT284', 3, 42000.00, 12);

INSERT INTO client (id, name, address) VALUES
  (1, 'Иван Петров', 'г. Москва, ул. Ленина, д. 10, кв. 45'),
  (2, 'Мария Сидорова', 'г. Санкт-Петербург, пр. Невский, д. 5'),
  (3, 'Алексей Козлов', 'г. Екатеринбург, ул. Мамина-Сибиряка, д. 100'),
  (4, 'Елена Васильева', 'г. Новосибирск, ул. Советская, д. 15'),
  (5, 'Дмитрий Смирнов', 'г. Казань, ул. Баумана, д. 25');

-- Заказ 1: Черновик (статус 'draft')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (1, 1, 0.00, 'draft');

INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (2, 2, 87980.00, 'confirmed');

INSERT INTO orderitem (order_id, nomenclature_id, quantity, fixed_price) VALUES
  (2, 1, 1, 79990.00),  -- iPhone 15 Pro
  (2, 10, 2, 990.00);   -- Защитное стекло (2 шт.)

-- Заказ 3: ПОДТВЕРЖДЁННЫЙ (статус 'confirmed')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (3, 3, 153500.00, 'confirmed');

-- Позиции подтвержденного заказа #3
INSERT INTO orderitem (order_id, nomenclature_id, quantity, fixed_price) VALUES
  (3, 5, 1, 120000.00),  -- iPad Pro
  (3, 11, 1, 3500.00),   -- Зарядное устройство
  (3, 12, 1, 24990.00);  -- AirPods Pro 2

-- Заказ 4: ПОДТВЕРЖДЁННЫЙ (статус 'confirmed')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (4, 4, 124980.00, 'confirmed');

-- Позиции подтвержденного заказа #4
INSERT INTO orderitem (order_id, nomenclature_id, quantity, fixed_price) VALUES
  (4, 2, 1, 85000.00),   -- Samsung Galaxy S24 Ultra
  (4, 13, 2, 1990.00),   -- Силиконовый чехол (2 шт.)
  (4, 10, 1, 990.00);    -- Защитное стекло

-- Заказ 5: Отменённый (статус 'cancelled')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (5, 5, 299990.00, 'cancelled');

-- Позиции отменённого заказа #5
INSERT INTO orderitem (order_id, nomenclature_id, quantity, fixed_price) VALUES
  (5, 7, 1, 299990.00);  -- MacBook Pro

-- Заказ 6: ПОДТВЕРЖДЁННЫЙ (статус 'confirmed')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (6, 1, 106980.00, 'confirmed');

-- Позиции подтвержденного заказа #6
INSERT INTO orderitem (order_id, nomenclature_id, quantity, fixed_price) VALUES
  (6, 3, 1, 65000.00),   -- Google Pixel 8 Pro
  (6, 9, 1, 2990.00),    -- Чехол кожаный
  (6, 10, 1, 990.00),    -- Защитное стекло
  (6, 11, 1, 3500.00);   -- Зарядное устройство

-- Заказ 7: ПОДТВЕРЖДЁННЫЙ (статус 'confirmed')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (7, 2, 107000.00, 'confirmed');

-- Позиции подтвержденного заказа #7
INSERT INTO orderitem (order_id, nomenclature_id, quantity, fixed_price) VALUES
  (7, 14, 1, 65000.00),  -- Холодильник LG
  (7, 15, 1, 42000.00);  -- Стиральная машина Bosch

-- Заказ 8: Черновик (статус 'draft')
INSERT INTO "order" (id, client_id, total_price, status) VALUES
  (8, 3, 0.00, 'draft');

UPDATE nomenclature SET stock = stock - 1 WHERE id = 1;   -- iPhone 15 Pro (заказ #2)
UPDATE nomenclature SET stock = stock - 2 WHERE id = 10;  -- Защитное стекло (заказ #2)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 5;   -- iPad Pro (заказ #3)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 11;  -- Зарядное устройство (заказ #3)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 12;  -- AirPods Pro 2 (заказ #3)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 2;   -- Samsung S24 Ultra (заказ #4)
UPDATE nomenclature SET stock = stock - 2 WHERE id = 13;  -- Силиконовый чехол (заказ #4)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 10;  -- Защитное стекло (заказ #4)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 3;   -- Google Pixel 8 Pro (заказ #6)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 9;   -- Чехол кожаный (заказ #6)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 10;  -- Защитное стекло (заказ #6)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 11;  -- Зарядное устройство (заказ #6)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 14;  -- Холодильник (заказ #7)
UPDATE nomenclature SET stock = stock - 1 WHERE id = 15;  -- Стиральная машина (заказ #7)

BEGIN
    RAISE NOTICE '=== Статистика базы данных ===';
    RAISE NOTICE 'Категории: %', (SELECT COUNT(*) FROM category);
    RAISE NOTICE 'Номенклатура: %', (SELECT COUNT(*) FROM nomenclature);
    RAISE NOTICE 'Клиенты: %', (SELECT COUNT(*) FROM client);
    RAISE NOTICE 'Заказы: %', (SELECT COUNT(*) FROM "order");
    RAISE NOTICE 'Позиции заказов: %', (SELECT COUNT(*) FROM orderitem);
    RAISE NOTICE '';
    RAISE NOTICE 'Заказы по статусам:';
    RAISE NOTICE '  draft: %', (SELECT COUNT(*) FROM "order" WHERE status = 'draft');
    RAISE NOTICE '  confirmed: %', (SELECT COUNT(*) FROM "order" WHERE status = 'confirmed');
    RAISE NOTICE '  cancelled: %', (SELECT COUNT(*) FROM "order" WHERE status = 'cancelled');
    RAISE NOTICE '';
    RAISE NOTICE 'Остатки на складе (топ 5):';
    PERFORM n.name, n.stock
    FROM nomenclature n
    ORDER BY n.stock DESC
    LIMIT 5;
END $$;
