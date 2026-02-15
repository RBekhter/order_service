import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import (create_order_item, get_nomenclature, get_order,
                   get_order_item, update_order_item)
from .database import engine, get_db
from .exceptions import (InsufficientStockException,
                         NomenclatureNotFoundException, OrderClosedException,
                         OrderNotFoundException)
from .handlers import (insufficient_stock_handler,
                       nomenclature_not_found_handler, order_closed_handler,
                       order_not_found_handler)
from .models import Order
from .repository.nomenclature_repository import NomenclatureRepository
from .repository.order_item_repository import OrderItemRepository
from .repository.order_repository import OrderRepository
from .schemas import AddItemToOrderRequest, ErrorResponse, OrderResponse
from .use_case.add_item import AddItemUseCase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✓ Подключение к БД установлено")
    except SQLAlchemyError as e:
        logger.error(f"✗ Невозможно подключиться к БД: {e}")
        raise SystemExit(1)
    yield
    await engine.dispose()
    logger.info("✓ Соединение с БД закрыто")

app = FastAPI(
    title="Order Service API",
    lifespan=lifespan
)

app.add_exception_handler(OrderNotFoundException, order_not_found_handler)
app.add_exception_handler(
    NomenclatureNotFoundException,
    nomenclature_not_found_handler
)
app.add_exception_handler(
    InsufficientStockException,
    insufficient_stock_handler
)
app.add_exception_handler(OrderClosedException, order_closed_handler)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"}
    )


@app.post(
    "/orders/items",
    response_model=OrderResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Заказ или номенклатура не найдены"},
        400: {"model": ErrorResponse, "description": "Недостаточно товара или заказ закрыт"}
    },
    summary="Добавить товар в заказ",
    description="""
    Добавляет товар в заказ. Если товар уже есть в заказе — увеличивает количество

    Проверки:
    - Заказ существует и имеет статус 'draft'
    - Номенклатура существует
    - Достаточное количество товара на остатке

    Изменения:
    - Обновляется `total_price` заказа
    - Уменьшается `stock` номенклатуры
    - Обновляется `updated_at` заказа
    """
)
async def add_item_to_order(
    request: AddItemToOrderRequest,
    db: AsyncSession = Depends(get_db)
) -> Order:
    use_case = AddItemUseCase(OrderRepository(db), NomenclatureRepository(db), OrderItemRepository(db), db)
    order = await use_case.execute(order_id=request.order_id, nomenclature_id=request.nomenclature_id, quantity=request.quantity)

    return order


@app.get("/health")
async def health_check():
    return {"status": "ок", "service": "order-service"}


@app.get("/")
async def root():
    return {
        "message": "Order Service API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }
