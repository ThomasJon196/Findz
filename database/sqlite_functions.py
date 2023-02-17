from contextlib import closing
import sqlite3

DB_NAME = 'findz.db'


def add_new_user(email):
    """
    Adds new user to user table.
    """
    query = f"INSERT INTO users (email, picture) VALUES ('{email}', 'dummy')"
    try:
        execute_sql_statement(query)
        print('Added new user')
    except sqlite3.IntegrityError as e:
        print(e)


def get_user_id(identifier):
    # TODO: Try except Already exsists error

    query = f"SELECT user_id FROM users WHERE email = '{identifier}'"
    id = retrieve_sql_query(query)[0][0]
    return id


def add_new_friend(friends_email, user_email):
    """
    Adds new friend to a user.

    Returns error if friends email does not exists in our user database.
    TODO: Here we could send an email in the future with invitation link.
    TODO: Exception handling
    """
    friends_id = get_user_id(friends_email)
    user_id = get_user_id(user_email)

    query = f""" \
        INSERT INTO friendlists (user_id, friend_id)\
        VALUES ({user_id}, {friends_id}) \
    """
    execute_sql_statement(query)
    print('Added friend')


def get_friendlist(user):
    pass


def execute_sql_statement(statement):
    """
    Execute the given sql statement. (Use for CREATE, INSERT, UPDATE, DELETE)
    """
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(statement)
        connection.commit()


def retrieve_sql_query(statement):
    """
    Execute the given sql statement. (Use for SELECT statement)
    """
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute(statement).fetchall()
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
    if len(tables) >= 4:
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
    SHOW_USERS = 'SELECT * FROM users'
    SHOW_FRIENDS = 'SELECT * FROM friendlists'

    initialize_database()

    email = "test@mail"
    friend_mail = "friend@mail"

    # Add users to database
    add_new_user(email)
    add_new_user(friend_mail)
    retrieve_sql_query(SHOW_USERS)

    # Retrieve users from database
    id = get_user_id(email)

    # Add friends

    # add_new_friend(friend_mail, email)
    retrieve_sql_query(SHOW_FRIENDS)

    email = 'jonas.thomas196@gmail.com'
    get_user_id(email)