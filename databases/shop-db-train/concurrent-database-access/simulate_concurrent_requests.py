import threading

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from alchemy.session_manager import SessionManager
from alchemy.tables import Product


def increment_product_price__select_for_update(product_id: int) -> None:
    with manager.session() as session:
        session: Session
        # this works fine
        product = session.query(Product).with_for_update().where(Product.id == product_id).first()
        product.price += 1

        query = insert(Product).values(product.as_dict())
        query = query.on_conflict_do_update(
            index_elements=["id"],
            set_={"price": product.price}
        )

        session.execute(query)


def increment_product_price(product_id: int) -> None:
    with manager.session() as session:
        session: Session
        product = session.query(Product).where(Product.id == product_id).first()
        product.price += 1

        query = insert(Product).values(product.as_dict())
        query = query.on_conflict_do_update(
            index_elements=["id"],
            set_={"price": product.price}
        )

        session.execute(query)


def make_concurrent_requests(threads_number: int) -> None:
    threads = []
    for _ in range(threads_number):
        thread = threading.Thread(target=increment_product_price, args=(1,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    manager = SessionManager(
        "postgresql+psycopg2://postgres:postgres@localhost/shop_db",
        isolation_level="SERIALIZABLE",
    )

    make_concurrent_requests(100)
