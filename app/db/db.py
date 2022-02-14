from app import get_connection


def create_tables():
    connection = get_connection()
    try:

        with open("schema.sql") as f:
            connection.executescript(f.read())

    except Exception as e:
        print(e)

    finally:
        if connection:
            connection.close()
