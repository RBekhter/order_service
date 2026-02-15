from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository:
    def __init__(self, db: AsyncSession, model):
        self.db = db
        self.model = model

    async def get(self, id: int):
        """Получить объект по ID"""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_or_raise(self, id: int):
        """Получить объект по ID или вызвать исключение"""
        obj = await self.get(id)
        if not obj:
            raise Exception(f"{self.model.__name__} with id {id} not found")
        return obj

    async def get_many(
            self,
            skip: int = 0,
            limit: int = 100,
            **filters
    ):
        """Получить список объектов с фильтрацией"""
        query = select(self.model)

        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, schema):
        """Создать новый объект"""
        obj_data = schema.model_dump()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            id: int,
            schema,
            **extra_data
    ):
        """Обновить объект"""
        obj = await self.get_or_raise(id)

        # Обновляем атрибуты
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in {**update_data, **extra_data}.items():
            if hasattr(obj, field):
                setattr(obj, field, value)

        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, id: int) -> bool:
        """Удалить объект"""
        obj = await self.get_or_raise(id)
        await self.db.delete(obj)
        await self.db.flush()
        return True
