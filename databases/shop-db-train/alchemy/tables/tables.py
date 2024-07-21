from datetime import datetime

from sqlalchemy import String, DateTime, func, Text, DECIMAL, ForeignKey, select, Select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from alchemy.tables.mixins import MixinAsDict


class Base(DeclarativeBase):
    pass


class User(MixinAsDict, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    profile_description: Mapped[str] = mapped_column(Text(), nullable=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    logins: Mapped[list["UserLogin"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Category(MixinAsDict, Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Product(MixinAsDict, Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))

    category: Mapped[Category] = relationship("Category", back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
    reviews: Mapped[list["Review"]] = relationship(back_populates="product")

    @hybrid_property
    def total_sold(self) -> int:
        """
        This works only on instance level, not on query level
        """
        return sum([item.quantity for item in self.order_items])


class Order(MixinAsDict, Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")

    @hybrid_property
    def total_items(self) -> int:
        return len(self.order_items)

    @total_items.expression
    def total_items(cls) -> int:
        return (
            select(func.sum(OrderItem.quantity))
            .where(OrderItem.order_id == cls.id)
            .group_by(cls.id)
            .scalar_subquery()
        )

    def __str__(self) -> str:
        return f"Order: {self.id}, of user {self.user_id}"


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="SET NULL"), nullable=True)

    order: Mapped[Order] = relationship("Order", back_populates="order_items")
    product: Mapped[Product] = relationship("Product", back_populates="order_items")


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(Text(), nullable=True)
    review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="reviews")

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    product: Mapped[Product] = relationship(back_populates="reviews")


class UserLogin(Base):
    __tablename__ = "user_login"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    logout_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(15))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="logins")
