from create_database import create
from db import engine
from generate_initial_data import generate_data, insert_data


def main():
    with engine.connect() as conn:
        create()
        users, products, orders = generate_data()
        insert_data(conn, users, products, orders)


if __name__ == "__main__":
    main()
