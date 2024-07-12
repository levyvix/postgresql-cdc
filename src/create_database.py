from db import engine
from sqlalchemy import text


def create():
    with engine.connect() as conn:
        conn.execute(text("create schema sales;"))

        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS sales.users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                deleted_at TIMESTAMP);
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS sales.products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                deleted_at TIMESTAMP);
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS sales.orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                deleted_at TIMESTAMP);
        """
            )
        )

        conn.commit()


if __name__ == "__main__":
    create()
