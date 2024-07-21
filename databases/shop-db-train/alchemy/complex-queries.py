from datetime import datetime, timedelta

from sqlalchemy import select, func, and_, desc, column
from sqlalchemy.orm import Session

from tables import (
    User, UserLogin, Product, Order, OrderItem, Category, Review
)
from session_manager import SessionManager


def get_top_5_users__in_most_popular_category() -> None:
    """
        Create a SQLAlchemy query that retrieves the top 5 users
         who have made the most purchases in the last month,
         but only for products that belong to the category with the most products.

        The result should include the username,total quantity of products purchased, and the total amount spent.
        The results should be ordered by the total amount spent in descending order.
    """

    with manager.session() as session:
        session: Session

        categories_popularity = (
            select(Category.id.label("category_id"), func.sum(OrderItem.quantity).label("total_sold"))
            .join(Product, Product.category_id == Category.id)
            .join(OrderItem, OrderItem.product_id == Product.id)
            .group_by(Category.id)
            .subquery("categories_popularity")
        )

        most_popular_category_subquery = (
            select(categories_popularity.columns.get("category_id"))
            .where(
                column("total_sold")
                ==
                select(func.max(column("total_sold")))
                .select_from(categories_popularity).scalar_subquery()
            )
            # we need this .limit(1) in order if there's several "most" popular categories
            # we just take first one that case
            .limit(1)
            .subquery()
        )

        query = (
            select(
                User.username,
                func.sum(OrderItem.quantity).label("total_items"),
                func.sum(OrderItem.quantity*Product.price).label("total_money_spent"),
            )
            .join(Order, Order.user_id == User.id)
            .join(OrderItem, OrderItem.order_id == Order.id)
            .join(Product, OrderItem.product_id == Product.id)
            .where(
                Product.category_id
                ==
                select(most_popular_category_subquery.columns.get("category_id")).scalar_subquery()
            )
            .group_by(User.username)
            .order_by(desc("total_items"))
        )

        results = session.execute(query)

        print(list(results))


def get_top_5_users__logged_most_frequently_with_filters() -> None:
    """
        You are tasked with creating a SQLAlchemy query that retrieves the top 5 users who have logged in
         the most frequently in the last week, but only if they have made at least one purchase in the last month.

        However, the twist is that these users must have also written at least 3 reviews in the
         last month, and their average review rating must be above 3.

        The result should include the username,
         total number of logins in the last week,
         the total amount spent in the last month, the number of reviews written, and the average review rating.
    """

    with manager.session() as session:
        session: Session

        week_ago_date = datetime.now() - timedelta(weeks=1)
        month_ago_date = datetime.now() - timedelta(days=30)

        user_login_freq_cte = (
            select(User.id, func.count().label("login_frequency"))
            .join(UserLogin, User.id == UserLogin.user_id)
            .where(UserLogin.login_date > week_ago_date)
            .group_by(User.id)
            .cte("user_login_freq")
        )

        user_reviews_stats_cte = (
            select(User.id, func.count().label("reviews_count"), func.avg(Review.rating).label("avg_rating"))
            .join(Review, Review.user_id == User.id)
            .where(Review.review_date > month_ago_date)
            .group_by(User.id)
            .cte("user_reviews_stats")
        )

        user_spent_money_cte = (
            select(User.id, func.sum(OrderItem.quantity * Product.price).label("total_money_spent"))
            .join(Order, Order.user_id == User.id)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, Product.id == OrderItem.order_id)
            .where(Order.created_at > month_ago_date)
            .group_by(User.id)
            .cte("user_spent_money")
        )

        query = (
            select(
                User.id,
                User.username,
                user_login_freq_cte.c.login_frequency,
                user_reviews_stats_cte.c.reviews_count,
                user_reviews_stats_cte.c.avg_rating,
                user_spent_money_cte.c.total_money_spent
            )
            .join(user_login_freq_cte, User.id == user_login_freq_cte.c.id)
            .join(user_reviews_stats_cte, User.id == user_reviews_stats_cte.c.id)
            .join(user_spent_money_cte, User.id == user_spent_money_cte.c.id)
            .where(
                and_(
                    user_reviews_stats_cte.c.reviews_count > 3,
                    user_reviews_stats_cte.c.avg_rating > 3
                )
            )
            .order_by(desc(user_login_freq_cte.c.login_frequency))
            .limit(3)
        )

        users_info = session.execute(query).all()

        print(list(users_info))


def get_top_products__with_reviews() -> None:
    with manager.session() as session:
        session: Session

        products_reviews_cte = (
            select(
                Product.id,
                func.count().label("product_reviews"),
                func.avg(Review.rating).label("product_avg_rate")
            )
            .join(Review, Review.product_id == Product.id)
            .group_by(Product.id)
            .cte("products_reviews")
        )

        query = (
            select(
                Product.name,
                Category.name,
                func.sum(Product.price*OrderItem.quantity).label("total_revenue"),
            )
            .join(products_reviews_cte, products_reviews_cte.c.id == Product.id)
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Category, Category.id == Product.category_id)
            .where(
                and_(
                    products_reviews_cte.c.product_reviews > 2,
                    products_reviews_cte.c.product_avg_rate > 4
                )
            )
            .group_by(Product.id, Product.name, Category.name)
            .order_by(column("total_revenue"))
            .limit(10)
        )

        top_products = session.execute(query).scalars().all()

        print(top_products)


def get_top_products__with_reviews___with_having() -> None:
    with manager.session() as session:
        session: Session

        products_reviews_with_conditions_cte = (
            select(Product.id)
            .join(Review, Review.product_id == Product.id)
            .group_by(Product.id)
            .having(
                and_(
                    func.count() > 5,
                    func.avg(Review.rating) > 2
                )
            )
            .cte("products_reviews_with_conditions")
        )

        query = (
            select(Category.name, Product.name, func.sum(OrderItem.quantity*Product.price).label("total_revenue"))
            .join(Category, Product.category_id == Category.id)
            .join(OrderItem, Product.id == OrderItem.product_id)
            .where(Product.id.in_(select(products_reviews_with_conditions_cte)))
            .group_by(Product.id, Category.name, Product.name)
            .order_by(desc(column("total_revenue")))
            .limit(10)
        )

        top_products = session.execute(query).scalars().all()

        print(top_products)


if __name__ == "__main__":
    manager = SessionManager("postgresql+psycopg2://postgres:postgres@localhost/shop_db")

    # get_top_5_users__in_most_popular_category()
    # get_top_5_users__logged_most_frequently_with_filters()
    get_top_products__with_reviews()
    # get_top_products__with_reviews___with_having()
