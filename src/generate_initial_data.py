from faker import Faker
import faker_commerce
from sqlalchemy import text

from db import engine

fake = Faker("pt_BR")
fake.add_provider(faker_commerce.Provider)


def generate_data(n_users=10, n_products=20, n_orders=50):
    # Generate Users
    users = []
    for _ in range(n_users):  # Generate 10 users
        users.append(
            {
                "name": fake.name(),
                "email": fake.email(),
                "password": fake.password(),
            }
        )

    products = []
    for _ in range(n_products):  # Generate 20 products
        products.append(
            {
                "name": fake.ecommerce_name(),
                "price": round(fake.random.uniform(10, 100), 2),
            }
        )

    # Generate Orders
    orders = []
    for _ in range(n_orders):  # Generate 50 orders
        orders.append(
            {
                "user_id": fake.random.randint(1, len(users)),
                "product_id": fake.random.randint(1, len(products)),
                "quantity": fake.random.randint(1, 5),
            }
        )

    return users, products, orders


def insert_data(conn, users, products, orders):
    """Inserts fake data into the database tables.

    Args:
        conn: The database connection object.
        users: List of dictionaries containing user data.
        products: List of dictionaries containing product data.
        orders: List of dictionaries containing order data.
    """

    # Insert Users
    for user in users:
        sql = text(
            """
      INSERT INTO sales.users (name, email, password)
      VALUES (:name, :email, :password);
    """
        )
        conn.execute(sql, user)

    # Insert Products
    for product in products:
        sql = text(
            """
      INSERT INTO sales.products (name, price)
      VALUES (:name, :price);
    """
        )
        conn.execute(sql, product)

    # Insert Orders
    for order in orders:
        sql = text(
            """
      INSERT INTO sales.orders (user_id, product_id, quantity)
      VALUES (:user_id, :product_id, :quantity);
    """
        )
        conn.execute(sql, order)

    # Commit changes to the database
    conn.commit()
    print("Fake data inserted successfully!")


# Example usage
if __name__ == "__main__":
    with engine.connect() as conn:
        users, products, orders = generate_data()
        insert_data(conn, users, products, orders)
