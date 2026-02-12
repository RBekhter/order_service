-- Индекс для фильтрации заказов по статусу и дате
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_order_status_created
  ON "order"(status, created_at DESC);

-- Covering индекс для агрегации ТОП-продаж
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orderitem_nomenclature_agg
  ON orderitem(nomenclature_id) INCLUDE (quantity);

-- Индекс для быстрого поиска номенклатуры по категории
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_nomenclature_category
  ON nomenclature(category_id) INCLUDE (id, name, price, stock);

-- Индекс для иерархии категорий (рекурсивный поиск)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_category_parent
  ON category(parent_category_id) INCLUDE (id, name);