from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric, String,
                        UniqueConstraint, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_category_id = Column(
        Integer,
        ForeignKey('category.id'),
        nullable=True
    )

    parent = relationship("Category", remote_side=[id], backref="children")
    nomenclatures = relationship("Nomenclature", back_populates="category")


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    category = relationship("Category", back_populates="nomenclatures")
    order_items = relationship("OrderItem", back_populates="nomenclature")


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)

    orders = relationship("Order", back_populates="client")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False, default=0)
    status = Column(String(50), nullable=False, default='draft')  # draft, confirmed, cancelled
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    client = relationship("Client", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "orderitem"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    nomenclature_id = Column(Integer, ForeignKey('nomenclature.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    fixed_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    nomenclature = relationship("Nomenclature", back_populates="order_items")

    __table_args__ = (
        UniqueConstraint('order_id', 'nomenclature_id', name='uq_order_nomenclature'),
    )
