# 2.1 Запрос на получение информации о сумме товаров, заказанных каждым клиентом
SELECT
    c.name AS client_name,
    COALESCE(SUM(o.total_price), 0) AS total_sum
FROM client c
LEFT JOIN "order" AS o ON c.id = o.client_id AND o.status = 'confirmed'
GROUP BY c.id, c.name
ORDER BY total_sum DESC;

# 2.2 Запрос на получение дочерних элементов первого уровня вложенности для категорий номенклатуры
SELECT
    parent.id AS category_id,
    parent.name AS category_name,
    COUNT(child.id) AS count_direct_child
FROM
    category AS parent
LEFT JOIN category AS child ON child.parent_category_id = parent.id
GROUP BY parent.id, parent.name;

# 2.3.1 Топ-5 самых покупаемых товаров за последний месяц
WITH RECURSIVE top_products AS (
    -- Находим топ-5 товаров
    SELECT
        n.id AS nomenclature_id,
        n.name AS product_name,
        n.category_id,
        SUM(oi.quantity) AS total_quantity_sold
    FROM orderitem oi
    JOIN nomenclature n ON oi.nomenclature_id = n.id
    JOIN "order" o ON oi.order_id = o.id
    WHERE
        o.status = 'confirmed'
        AND o.created_at >= CURRENT_DATE - INTERVAL '1 month'
    GROUP BY n.id, n.name, n.category_id
    ORDER BY total_quantity_sold DESC
    LIMIT 5
),
category_ancestors AS (
    -- Поиск категории 1-го уровня
    SELECT
        c.id AS current_category_id,
        c.id AS ancestor_id,
        c.name AS ancestor_name,
        c.parent_category_id,
        0 AS depth
    FROM category c
    WHERE c.id IN (SELECT category_id FROM top_products)

    UNION ALL

    -- Поиск родительской категории
    SELECT
        ca.current_category_id,
        c.id AS ancestor_id,
        c.name AS ancestor_name,
        c.parent_category_id,
        ca.depth + 1
    FROM category c
    INNER JOIN category_ancestors ca ON c.id = ca.parent_category_id
    WHERE ca.parent_category_id IS NOT NULL
),
root_categories AS (
    -- Выбор только корневых категорий
    SELECT
        current_category_id,
        ancestor_name AS root_name
    FROM category_ancestors
    WHERE parent_category_id IS NULL
)
-- Формирование итогового отчета
SELECT
    tp.product_name,
    rc.root_name AS top_level_category,
    tp.total_quantity_sold
FROM top_products tp
JOIN root_categories rc ON tp.category_id = rc.current_category_id
ORDER BY tp.total_quantity_sold DESC;


# 2.3.2 Варианты оптимизации запроса Топ-5 товаров и общей схемы данных
# для повышения производительности системы в устовиях роста данных

# 1. Индексация
Добавить индексы:
    category -> (parent_category_id) INCLUDE (id, name) -  ускорение рекурсивного поиска дерева категорий
    order -> (status, created_at DESC) - фильтрация заказов по статусу и дате
    orderItem -> (nomenclature_id) INCLUDE (quantity) - агрегация по товарам заказа
    nomenclature -> (category_id) INCLUDE(id, name, price, stock) - получение данных номенклатуры

# 2. Кэширование на уровне приложения (Redis)

# 3. Денормализация корня категории
Можно добавить в таблицу category поле root_category_id
В этом случае сложность вычислений смещается в сторону обновления, что лучше,
так как изменение категорий происходит гораздо реже, чем запрос отчетов
В результате запрос будет выглядеть так:

SELECT
    n.name AS product_name,
    root.name AS top_level_category,
    SUM(oi.quantity) AS total_quantity
FROM orderitem oi
JOIN nomenclature n ON oi.nomenclature_id = n.id
JOIN category cat ON n.category_id = cat.id
JOIN category root ON cat.root_category_id = root.id
JOIN "order" o ON oi.order_id = o.id
WHERE
    o.status = 'confirmed'
    AND o.created_at >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY n.id, n.name, root.name
ORDER BY total_quantity DESC
LIMIT 5;

# 4. Создать агрегационную таблицу для статистики и ежедневно обновлять ее в фоне

# 6. Для очень больших объемов можно разделить таблицу на партиции по времени

# 7. Архивировать старые данные - перемещать старые заказы в архивную таблицу

# 8. Создать горизонтальное масштабирование - читать отчет с реплик, не нагружая мастер
