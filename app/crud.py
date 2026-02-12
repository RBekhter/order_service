from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import (InsufficientStockException,
                         NomenclatureNotFoundException, OrderNotFoundException)
from .models import Nomenclature, Order, OrderItem


async def get_order(db: AsyncSession, order_id: int) -> Order:
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise OrderNotFoundException(order_id)
    await db.refresh(order)
    return order


async def get_nomenclature(
    db: AsyncSession,
    nomenclature_id: int
) -> Nomenclature:
    result = await db.execute(
        select(Nomenclature).where(Nomenclature.id == nomenclature_id)
    )
    nomenclature = result.scalar_one_or_none()
    if not nomenclature:
        raise NomenclatureNotFoundException(nomenclature_id)
    await db.refresh(nomenclature)
    return nomenclature


async def get_order_item(
    db: AsyncSession,
    order_id: int,
    nomenclature_id: int
) -> OrderItem | None:
    result = await db.execute(
        select(OrderItem).where(
            OrderItem.order_id == order_id,
            OrderItem.nomenclature_id == nomenclature_id
        )
    )
    order_item = result.scalar_one_or_none()
    if order_item:
        await db.refresh(order_item)
    return order_item


async def create_order_item(
    db: AsyncSession,
    order: Order,
    nomenclature: Nomenclature,
    quantity: int
) -> OrderItem:
    await db.refresh(nomenclature)
    if nomenclature.stock < quantity:
        raise InsufficientStockException(
            nomenclature_id=nomenclature.id,
            requested=quantity,
            available=nomenclature.stock
        )
    await db.refresh(order)
    order_item = OrderItem(
        order_id=order.id,
        nomenclature_id=nomenclature.id,
        quantity=quantity,
        fixed_price=nomenclature.price
    )
    db.add(order_item)
    order.total_price += Decimal(quantity) * nomenclature.price
    order.updated_at = datetime.utcnow()
    nomenclature.stock -= quantity
    return order_item


async def update_order_item(
    db: AsyncSession,
    order_item: OrderItem,
    nomenclature: Nomenclature,
    additional_quantity: int
) -> OrderItem:
    await db.refresh(nomenclature)
    await db.refresh(order_item)
    await db.refresh(order_item.order)

    if nomenclature.stock < additional_quantity:
        raise InsufficientStockException(
            nomenclature_id=nomenclature.id,
            requested=additional_quantity,
            available=nomenclature.stock
        )
    new_quantity = order_item.quantity + additional_quantity
    order_item.quantity = new_quantity
    order_item.order.total_price += (
        Decimal(additional_quantity) * nomenclature.price
    )
    order_item.order.updated_at = datetime.utcnow()
    nomenclature.stock -= additional_quantity
    return order_item
