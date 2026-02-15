from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order
from app.repository.base_repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Order)
