import psycopg2 # PostgreSQL adapter for Python 

import os

def connect():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return connection


if __name__ == '__main__':
    connection = connect()
    print("Connection established")
    connection.close()
    print("Connection closed")
