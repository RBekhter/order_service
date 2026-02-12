from fastapi import Request, status
from fastapi.responses import JSONResponse

from .exceptions import (InsufficientStockException,
                         NomenclatureNotFoundException, OrderClosedException,
                         OrderNotFoundException)


async def order_not_found_handler(
    request: Request,
    exc: OrderNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "order_not_found", "message": exc.detail}
    )


async def nomenclature_not_found_handler(
    request: Request,
    exc: NomenclatureNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "nomenclature_not_found", "message": exc.detail}
    )


async def insufficient_stock_handler(
    request: Request,
    exc: InsufficientStockException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "insufficient_stock",
            "message": exc.detail,
            "requested": exc.requested,
            "available": exc.available
        }
    )


async def order_closed_handler(request: Request, exc: OrderClosedException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "order_closed", "message": exc.detail}
    )
