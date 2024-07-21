from datetime import datetime, timedelta

from sqlalchemy import select, func, and_, alias, desc, column
from sqlalchemy.orm import Session, selectinload, joinedload

from tables import (
    User, UserLogin, Product, Order, OrderItem, Category, Review
)
from session_manager import SessionManager


def get_unique_usernames() -> None:
    with manager.session() as session:
        session: Session
        values = session.execute(select(User.username)).scalars().unique().all()

        for user in values:
            print(user)  # strings


def get_users_within_time_range__and__username_startswith() -> None:
    yesterday = datetime.now() - timedelta(days=1)
    today = datetime.now()

    with manager.session() as session:
        session: Session
        users = session.execute(
            select(User)
            .where(
                and_(
                    User.created_at.between(yesterday, today),
                    User.username.startswith("j")
                )
            )
        ).scalars().all()

        for user in users:
            print(user.username, user.created_at, user.email)


def get_user_and_total_bought_items() -> None:
    """
        JOIN three tables, group by and use aggregate function
        then order by
    :return:
    """
    with manager.session() as session:
        session: Session
        values = session.execute(
            select(User.username, func.sum(OrderItem.quantity).label("total sum"))
            .join(Order, User.id == Order.user_id)
            .join(OrderItem, OrderItem.order_id == Order.id)
            .group_by(User.username)
            .order_by(desc("total sum"))
        ).all()

        print(values)
        print(values[0])  # tuple of username and total sum


def get_user_prefetch_reviews() -> None:
    with manager.session() as session:
        session: Session

        users = (
            session.query(User)
            .options(selectinload(User.reviews))
            .all()
        )

        for user in users:
            print(user.as_dict())


def get_top_products__with_total_sold() -> None:
    with manager.session() as session:
        session: Session

        top_products = (
            session.query(Product)
            .options(selectinload(Product.order_items))
            .order_by(desc(Product.id))
            .limit(3)
            .all()
        )

        print("\n\n=====================\n\n")

        for product in top_products:
            print(product.as_dict(), product.total_sold)


def get_orders__with_custom_column() -> None:
    with manager.session() as session:
        session: Session

        year_ago_date = datetime.now() - timedelta(days=365)

        result = (
            session.query(Order)
            .add_columns(func.sum(OrderItem.quantity).label("total_items"))
            .join(OrderItem, Order.id == OrderItem.order_id)
            .filter(Order.created_at.between(year_ago_date, datetime.now()))
            .group_by(Order.id)
            .all()
        )

        print("\n\n=====================\n\n")

        for order, total_items in result:
            print(order.id, total_items)


def get_orders_with_prejoin__and_custom_column() -> None:
    with manager.session() as session:
        session: Session

        orders_with_total_items__cte = (
            session.query(Order)
            .add_columns(func.sum(OrderItem.quantity).label("total_items"))
            .join(OrderItem, Order.id == OrderItem.order_id)
            .group_by(Order.id)
            .cte("orders_with_total_items")
        )

        result = (
            session.query(Order)
            .add_columns(orders_with_total_items__cte.c.total_items)
            .join(orders_with_total_items__cte, Order.id == orders_with_total_items__cte.c.id)
            .options(
                selectinload(Order.order_items).joinedload(OrderItem.product),
                joinedload(Order.user),
            )
            .all()
        )

        print("\n\n=====================\n\n")

        for order, total_items in result:
            print(order.id, total_items, order.user.username, [item.product.name for item in order.order_items])


def get_orders__additional_column(session: SessionManager) -> None:
    with session.session() as session:
        session: Session

        result = (
            session.query(Order)
            .add_columns(
                column("quantity", _selectable=(
                        session.query(OrderItem)
                        .where(OrderItem.order_id == Order.id)
                        .cte()
                    )
                )
            )
            .join(OrderItem, Order.id == OrderItem.order_id)
            .all()
        )

        for order, quantity in result:
            print(order.id, quantity)


def query_hybrid_property(session: SessionManager) -> None:
    with session.session() as session:
        session: Session

        query = (
            select(Order)
            .where(Order.total_items > 2)
        )

        items = session.execute(query).all()

        for row in items:
            print(row[0])


if __name__ == "__main__":
    manager = SessionManager("postgresql+psycopg2://postgres:postgres@localhost/shop_db")

    # get_unique_usernames()
    # get_users_within_time_range__and__username_startswith()
    # get_user_and_total_bought_items()
    # get_top_products__with_total_sold()
    # get_orders__with_custom_column()
    # get_orders_with_prejoin__and_custom_column()
    # get_orders__additional_column(manager)
    query_hybrid_property(manager)
