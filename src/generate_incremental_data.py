from db import engine

from generate_initial_data import insert_data, generate_data
from sqlalchemy import text
import schedule


def generate_incremental_data(n_orders=5, n_users=3, n_products=2):
    with engine.connect() as conn:
        new_users, new_products, new_orders = generate_data(
            n_orders=n_orders, n_users=n_users, n_products=n_products
        )

        existing_users = conn.execute(
            text("SELECT id, name, email, password FROM sales.users")
        ).fetchall()
        existing_users = set((user[1], user[2], user[3]) for user in existing_users)

        existing_products = conn.execute(
            text("SELECT id, name, price FROM sales.products")
        ).fetchall()
        existing_products = set(
            (product[1], product[2]) for product in existing_products
        )

        existing_orders = conn.execute(
            text(
                "SELECT user_id, product_id, quantity FROM sales.orders "
                "WHERE created_at IS NULL"
            )
        ).fetchall()
        existing_orders = set((order[0], order[1]) for order in existing_orders)

        new_users = [
            user
            for user in new_users
            if (user["name"], user["email"], user["password"]) not in existing_users
        ]
        new_products = [
            product
            for product in new_products
            if (product["name"], product["price"]) not in existing_products
        ]
        new_orders = [
            order
            for order in new_orders
            if (order["user_id"], order["product_id"]) not in existing_orders
        ]

        insert_data(conn, new_users, new_products, new_orders)


if __name__ == "__main__":
    manual = False

    if manual:
        generate_incremental_data(n_orders=1, n_users=1, n_products=1)
    else:
        schedule.every(5).minutes.do(
            generate_incremental_data, n_orders=1, n_users=1, n_products=1
        )

        while True:
            schedule.run_pending()
