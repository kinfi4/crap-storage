from sqlalchemy import create_engine, Engine, Connection, text


def execute_raw_sql(engine: Engine, raw_query: str) -> None:
    with engine.connect() as connection:
        connection: Connection

        statement = text(raw_query)

        result = connection.execute(statement)

        for row in result:
            order_id, user_id, total_items_sold = row
            print(f"Order {order_id} of user {user_id}, total items: {total_items_sold}")


if __name__ == "__main__":
    manager = create_engine("postgresql+psycopg2://postgres:postgres@localhost/shop_db")

    get_orders_sql = """
        SELECT o.id, o.user_id, sum(oi.quantity) AS total_item_sold FROM "order" o
            JOIN "order_item" oi ON o.id = oi.order_id
        GROUP BY o.id, o.user_id
    """

    execute_raw_sql(manager, get_orders_sql)
