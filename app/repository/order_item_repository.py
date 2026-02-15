from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrderItem
from app.repository.base_repository import BaseRepository


class OrderItemRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, OrderItem)

    async def get_order_and_nomenclature_id(self, order_id: int, nomenclature_id: int):
        result = await self.db.execute(
            select(self.model).where(self.model.order_id == order_id, self.model.nomenclature_id == nomenclature_id)
        )
        return result.scalar_one_or_none()