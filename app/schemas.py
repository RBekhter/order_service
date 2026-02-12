from pydantic import BaseModel, Field, validator
from decimal import Decimal
from datetime import datetime


class AddItemToOrderRequest(BaseModel):
    order_id: int = Field(..., gt=0, description="ID заказа")
    nomenclature_id: int = Field(..., gt=0, description="ID номенклатуры")
    quantity: int = Field(..., gt=0, le=1000, description="Количество (1-1000)")

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Количество должно быть больше 0')
        if v > 1000:
            raise ValueError('Максимальное количество — 1000')
        return v


class NomenclatureResponse(BaseModel):
    id: int
    name: str
    price: Decimal

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    id: int
    nomenclature: NomenclatureResponse
    quantity: int
    fixed_price: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    client_id: int
    total_price: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
