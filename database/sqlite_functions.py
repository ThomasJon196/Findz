from contextlib import closing
import sqlite3

DB_NAME = 'findz.db'


def require_unique(function):  # sqlite IntegrityError.
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            return f"An error occurred: {e}"
    return wrapper


@require_unique
def add_new_user(email):
    """
    Adds new user to user table.
    """
    query = f"INSERT INTO users (email, picture) VALUES ('{email}', 'dummy')"
    execute_sql_statement(query)
    print('Added new user')


def get_user_id(identifier):
    # TODO: Try except Already exsists error

    query = f"SELECT user_id FROM users WHERE email = '{identifier}'"
    id = retrieve_sql_query(query)
    return id[0][0]


@require_unique
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
    INSERT INTO friendlists (user_id, friend_id) \
    VALUES ({user_id}, {friends_id}) \
    """
    execute_sql_statement(query)
    print('Added friend')


@require_unique
def add_new_group(admin, groupname):
    """
    Adds new friend to a user.

    Returns error if friends email does not exists in our user database.
    TODO: Here we could send an email in the future with invitation link.
    TODO: Exception handling
    """
    user_id = get_user_id(admin)

    query = f""" \
    INSERT INTO groups (group_name, admin_id) \
    VALUES ('{groupname}', {user_id}) \
    """
    execute_sql_statement(query)
    print(f'Created group: {groupname}.')


@require_unique
def add_new_group_members(admin, groupname, new_users):
    """
    Adds new friend to a user.

    Returns error if friends email does not exists in our user database.
    TODO: Here we could send an email in the future with invitation link.
    TODO: Exception handling
    """
    admin_id = get_user_id(admin)

    query_group = f""" \
    SELECT group_id FROM groups \
    WHERE admin_id == {admin_id} \
    """
    group_id = retrieve_sql_query(query_group)[0][0]
    user_ids = tuple([get_user_id(new_user) for new_user in new_users])
    if len(user_ids) == 1:
        user_ids = f"({user_ids[0]})"
    sql_params = [(group_id, user_id) for user_id in user_ids]
    
    query = "INSERT INTO group_members (group_id, member_id) VALUES (?, ?)"
    execute_sql_statement(query, sql_params)

    print(f'Added {new_users} to group {groupname}.')


def get_friendlist(email):
    user_id = get_user_id(email)
    query_friends = f""" \
    SELECT friend_id FROM friendlists \
    WHERE user_id == '{user_id}' \
    """
    friendlist_ids = retrieve_sql_query(query_friends)
    friendlist_ids = concat_query_result(friendlist_ids)

    if len(friendlist_ids) == 1:
        friendlist_ids = f"({friendlist_ids[0]})"

    query_mails = f""" \
    SELECT email FROM users \
    WHERE user_id IN {friendlist_ids} \
    """

    friendlist_mails = retrieve_sql_query(query_mails)
    friendlist_mails = concat_query_result(friendlist_mails)

    return friendlist_mails


def get_grouplist(admin_mail):
    admin_id = get_user_id(admin_mail)

    query_mails = f""" \
    SELECT group_name FROM groups \
    WHERE admin_id = {admin_id} \
    """

    friendlist_mails = retrieve_sql_query(query_mails)
    friendlist_mails = concat_query_result(friendlist_mails)
    return friendlist_mails


def get_group_memberlist(admin_mail, group_name):
    admin_id = get_user_id(admin_mail)

    query_members = f""" \
    SELECT email FROM users \
    WHERE user_id IN ( \
        SELECT member_id FROM group_members \
        WHERE group_id = ( \
            SELECT group_id FROM groups \
            WHERE admin_id = {admin_id} \
            AND group_name = '{group_name}' \
        )) \
    """

    friendlist_mails = retrieve_sql_query(query_members)
    friendlist_mails = concat_query_result(friendlist_mails)
    return friendlist_mails


def concat_query_result(tuple_list):
    tuple = ()
    for tpl in tuple_list:
        tuple += tpl
    return tuple


def execute_sql_statement(statement, additional_params=None):
    """
    Execute the given sql statement. (Use for CREATE, INSERT, UPDATE, DELETE)
    """
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            if additional_params:
                cursor.executemany(statement, additional_params)
            else:
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
        UNIQUE (group_name, admin_id)
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
    SHOW_GROUPS = 'SELECT * FROM groups'

    initialize_database()

    email = "master@mail"
    friend_mail = "cat@mail"
    friend_mail_2 = "dog@mail"

    # Add users to database
    add_new_user(email)
    add_new_user(friend_mail)
    add_new_user(friend_mail_2)
    retrieve_sql_query(SHOW_USERS)

    # Retrieve users from database
    id = get_user_id(email)

    email_1 = 'jonas.thomas196@gmail.com'
    get_user_id(email)

    # Add friends

    add_new_friend(friend_mail, email)
    # add_new_friend(friend_mail_2, email)
    retrieve_sql_query(SHOW_FRIENDS)

    # Get Friendlist
    get_friendlist(email)

    # Create new group
    add_new_group(admin=email, groupname="Meat")
    retrieve_sql_query(SHOW_GROUPS)

    # Add group members
    add_new_group_members(admin=email, groupname="dummyGroup",
                          new_users=[friend_mail, friend_mail_2])
