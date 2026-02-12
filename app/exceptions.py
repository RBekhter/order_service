from fastapi import HTTPException, status


class OrderNotFoundException(HTTPException):
    def __init__(self, order_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден"
        )


class NomenclatureNotFoundException(HTTPException):
    def __init__(self, nomenclature_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Номенклатура с ID {nomenclature_id} не найдена"
        )


class InsufficientStockException(HTTPException):
    def __init__(self, nomenclature_id: int, requested: int, available: int):
        self.nomenclature_id = nomenclature_id
        self.requested = requested
        self.available = available
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Недостаточно товара на остатке. "
                f"Запрошено: {requested}, Доступно: {available}"
            )
        )


class OrderClosedException(HTTPException):
    def __init__(self, order_id: int, order_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Нельзя изменить заказ #{order_id} "
                f"со статусом '{order_status}'"
            )
        )
