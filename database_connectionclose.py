import psycopg2
from config import *
from database_connection import *
from queringsql_tables import *


def connection_close():
    try:
        print("Database connection is not in use")

    finally:
     #closing database connection.
            if(connection):
              cursor.close()
              connection.close()
              print("PostgreSQL connection is closed")
