from app.crud import update_order_item, create_order_item
from app.exceptions import OrderClosedException
from app.repository.nomenclature_repository import NomenclatureRepository
from app.repository.order_item_repository import OrderItemRepository
from app.repository.order_repository import OrderRepository


class AddItemUseCase:
    def __init__(self, order_repo: OrderRepository,
                 nomenclature_repo: NomenclatureRepository,
                 order_item_repo: OrderItemRepository,
                 db) -> None:
        self.order_repo = order_repo
        self.nomenclature_repo = nomenclature_repo
        self.order_item_repo = order_item_repo
        self.db = db

    async def execute(self, order_id: int, nomenclature_id: int, quantity: int):
        order = await self.order_repo.get(order_id)

        if order.status != 'draft':
            raise OrderClosedException(order.id, order.status)

        nomenclature = await self.nomenclature_repo.get(nomenclature_id)
        existing_item = await self.order_item_repo.get_order_and_nomenclature_id(order_id, nomenclature_id)
        if existing_item:
            await update_order_item(
                self.db,
                existing_item,
                nomenclature,
                quantity
            )
        else:
            await create_order_item(
                self.db,
                order,
                nomenclature,
                quantity
            )
        await self.db.refresh(order, ['items'])
        for item in order.items:
            await self.db.refresh(item, ['nomenclature'])
        return order
