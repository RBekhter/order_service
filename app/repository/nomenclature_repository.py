from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Nomenclature
from app.repository.base_repository import BaseRepository


class NomenclatureRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Nomenclature)
