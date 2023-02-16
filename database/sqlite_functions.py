from contextlib import closing
import sqlite3

DB_NAME = 'findz.db'


def add_new_user(email):
    """
    Adds new user to user table.
    """
    query = f""" \
        INSERT INTO users (email, picture) \
        VALUES ('{email}', 'dummy') \
    """
    execute_sql_statement(query)


def get_user_id(identifier):
    # TODO: Try except Already exsists error

    query = f"SELECT user_id FROM users WHERE email = '{identifier}'"
    id = retrieve_sql_query(query)
    return id


def add_new_friend(friends_email, user_email):
    """
    Adds new friend to a user.

    Returns error if friends email does not exists in our user database.
    TODO: Here we could send an email in the future with invitation link.
    """
    friends_id = get_user_id(friends_email)
    user_id = get_user_id(user_email)

    query = f"""
        INSERT INTO friendlists
        VALUES ({user_id}, {friends_id})
    """
    execute_sql_statement(query)


def execute_sql_statement(statement):
    """
    Execute the given sql statement. (Use for CREATE, INSERT, UPDATE, DELETE)
    """
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute(statement)
            print(rows)


def retrieve_sql_query(statement):
    """
    Execute the given sql statement. (Use for SELECT statement)
    """
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute(statement).fetchall()
            print(rows)
    return rows


def tables_exist():
    """
    Return True if all tables exist. (Currently only 3.)
    """
    query = """
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name='users' OR name='friendlists'
        OR name='groups' OR name='group_members'
    """

    tables = retrieve_sql_query(query)
    if len(tables) == 3:
        return True
    else:
        return False


def initialize_database():
    """
    Create tables if they dont exist already.
    TODO: Should I use an index here?
    """
    users_table = """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        email VARCHAR(100) NOT NULL,
        picture VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (email)
    )
    """
    friendlists_table = """
    CREATE TABLE friendlists (
        friendlist_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        friend_id INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (friend_id) REFERENCES users(user_id),
        UNIQUE (user_id, friend_id)
    )
    """
    groups_table = """
    CREATE TABLE groups (
        group_id INTEGER PRIMARY KEY,
        group_name VARCHAR(50) NOT NULL,
        admin_id INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (admin_id) REFERENCES users(user_id)
    )
    """

    group_members_table = """
    CREATE TABLE group_members (
        group_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(group_id),
        FOREIGN KEY (member_id) REFERENCES users(user_id),
        UNIQUE (group_id, member_id)
    )
    """

    if not tables_exist():
        execute_sql_statement(users_table)
        execute_sql_statement(friendlists_table)
        execute_sql_statement(groups_table)
        execute_sql_statement(group_members_table)
    else:
        print("Tables already exist.")


if __name__ == '__main__':
    SHOW_TABLE = 'SELECT * FROM users'

    initialize_database()
    add_new_user("test@mail")
    retrieve_sql_query(SHOW_TABLE)
    