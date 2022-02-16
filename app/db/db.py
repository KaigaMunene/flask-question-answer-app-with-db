from app import get_connection


def create_tables():
    connection = get_connection()
    try:

        with open("app/db/schema.sql") as f:
            connection.executescript(f.read())

    except Exception as e:
        raise Exception(f"Creating tables: {e}")

    finally:
        if connection:
            connection.close()
