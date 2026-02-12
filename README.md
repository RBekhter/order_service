### Микросервис управления заказами, реализующий бизнес-логику добавления товаров в заказ

#### Сервис позволяет:
* Добавлять товары в существующий заказ
* Увеличивать количество существующих позиций (без дублирования)
* Проверять наличие товара на остатке
* Работать только с заказами в статусе Черновик
* Автоматически расчитывать итоговую стоимость заказа
* Возвращать структурированные ошибки для интеграции

#### Запуск в контейнере:
* cd order_service
* docker-compose up -d --build

#### Открыть базу данных:
* http://localhost:5050/browser/
* Login: user
* Password: 1234
* host: db
* database: my_db

#### Проверить состояние сервиса
* GET -> http://localhost:8000/health

#### Пример API-запроса на добавление номенклатуры в заказ:
* POST -> http://localhost:8000/orders/items

```json
{
"order_id": "1",
"nomenclature_id": 2,
"quantity": 1
}
```
* Пример успешного ответа:

```json
{
    "id": 1,
    "client_id": 1,
    "total_price": "85000.00",
    "status": "draft",
    "created_at": "2026-02-12T07:35:04.036050",
    "updated_at": "2026-02-12T07:41:16.965556",
    "items": [
        {
            "id": 34,
            "nomenclature": {
                "id": 2,
                "name": "Samsung Galaxy S24 Ultra 512GB",
                "price": "85000.00"
            },
            "quantity": 1,
            "fixed_price": "85000.00"
        }
    ]
}
```

#### Открыть документацию API
* http://localhost:8000/docs

#### Возможные ошибки:
* 404 - order_not_found
* 404 - nomenclature_not_found
* 400 - insufficient_stock
* 400 - order_closed (нельзя изменить заказ со статусом, отличным от draft)

#### Технологический стек
* Backend: FastAPI (Python 3.11)
* Database: PostgreSQL 15
* ORM: SQLAlchemy 2.0
* Containerization: Docker, Docker Compose