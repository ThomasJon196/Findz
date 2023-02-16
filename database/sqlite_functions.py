from contextlib import closing
import sqlite3


def execute_sql(statement):
    """
    Execute the given sql statement.
    """
    with closing(sqlite3.connect("findz.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute(statement).fetchall()
            print(rows)
