from contextlib import closing
import sqlite3

DB_NAME = 'findz.db'

# TODO: Querries might not be secure against injections yet. FIX


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
    if identifier == 'None':
        print("Bitte neu einloggen Mister 1.0")
        return None
    else:
        query = f"SELECT user_id FROM users WHERE email = '{identifier}'"
        id = retrieve_sql_query(query)
        return id[0][0]


def user_logged_in(email):
    user_id = get_user_id(email)
    query = f"UPDATE users SET loggedIN = 1 WHERE user_id = {user_id}"
    execute_sql_statement(query)


def user_logged_out(email):
    user_id = get_user_id(email)
    query = f"UPDATE users SET loggedIN = 0 WHERE user_id = {user_id}"
    execute_sql_statement(query)


def loggout_all_users():  
    query = "UPDATE users SET loggedIN = 0"
    execute_sql_statement(query)


def get_all_users():
    query = "SELECT email FROM users"
    mails = retrieve_sql_query(query)
    return mails


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
    Adds members to a group
    """
    admin_id = get_user_id(admin)
    print('new users:' + str(new_users))

    query_group = f""" \
    SELECT group_id FROM groups \
    WHERE admin_id = {admin_id} \
    AND group_name = '{groupname}' \
    """

    group_id = retrieve_sql_query(query_group)[0][0]
    user_ids = tuple([get_user_id(new_user) for new_user in new_users])
    print('User IDs: ' + str(user_ids))

    if len(user_ids) == 1:
        user_ids = [user_ids[0]]
    sql_params = [(group_id, user_id) for user_id in user_ids]

    query = "INSERT INTO group_members (group_id, member_id) VALUES (?, ?)"
    print("Add group: sql params: " + str(sql_params))

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


def get_grouplist(user):
    user_id = get_user_id(user)

    query_mails = f""" \
    SELECT group_name FROM groups \
    WHERE group_id IN (
        SELECT group_id FROM group_members \
        WHERE member_id = {user_id} \
    ) \
    """

    friendlist_mails = retrieve_sql_query(query_mails)
    friendlist_mails = concat_query_result(friendlist_mails)
    return friendlist_mails


def get_group_memberlist(user, group_name):
    # TODO: Refactor sql queries. Variables inside are a safety vournability.

    query_members = f""" \
    SELECT email FROM users \
    WHERE user_id IN ( \
        SELECT member_id FROM group_members \
        WHERE group_id = ( \
            SELECT group_id FROM groups \
            WHERE group_name = '{group_name}' \
        )) \
    """

    friendlist_mails = retrieve_sql_query(query_members)
    friendlist_mails = concat_query_result(friendlist_mails)

    print(friendlist_mails)

    return friendlist_mails


def get_group_memberlist_and_location(group_name):
    # TODO: Refactor sql queries. Variables inside are a safety vournability.

    # admin_id = get_user_id(group_admin_mail)

    # query_members = f""" \
    # SELECT email, longitude, latitude FROM users \
    # WHERE user_id IN ( \
    #     SELECT member_id FROM group_members \
    #     WHERE group_id = ( \
    #         SELECT group_id FROM groups \
    #         WHERE admin_id = {admin_id} \
    #         AND group_name = '{group_name}' \
    #     )) \
    # """

    query_members = f""" \
    SELECT email, longitude, latitude FROM users \
    WHERE user_id IN ( \
        SELECT member_id FROM group_members \
        WHERE group_id = ( \
            SELECT group_id FROM groups \
            WHERE group_name = '{group_name}' \
        )) \
    AND loggedIN = 1
    """

    memberlist_locations = retrieve_sql_query(query_members)
    # memberlist_locations = concat_query_result(memberlist_locations)
    # print("memberlist_locations:" + str(memberlist_locations))

    # query_group_admin = f""" \
    # SELECT email, longitude, latitude FROM users \
    # WHERE user_id = {admin_id}\
    # """

    # group_admin_location = retrieve_sql_query(query_group_admin)

    # # print("admin_location:" + str(group_admin_location))

    # memberlist_locations += group_admin_location

    print("Member list:" + str(memberlist_locations))

    return memberlist_locations


def update_location(email, longitute, latitude):

    user_id = get_user_id(email)

    query_update_location = f""" \
    UPDATE users \
    SET longitude = {longitute}, latitude = {latitude} \
    WHERE user_id = {user_id}; \
    """

    execute_sql_statement(query_update_location)


def save_new_point(payload, user, groupname):

    user_id = get_user_id(user)

    query_group = f""" \
    SELECT group_id FROM groups \
    WHERE group_name = '{groupname}' \
    """
    group_id = retrieve_sql_query(query_group)[0][0]

    query = f"""\
        INSERT INTO saved_points (user_id, group_id, title, describtion, longitude, latitude) \
        VALUES ({user_id}, {group_id}, '{payload.get("title")}', \
          '{payload.get("text")}', {payload.get("longitude")}, {payload.get("latitude")}) \
    """

    execute_sql_statement(query)


def get_saved_group_points(group):
    """
    Returns all saved points inside the current group.
    """
    query = f""" \
    SELECT title, describtion, longitude, latitude FROM saved_points \
    WHERE group_id = (
        SELECT group_id FROM groups
        WHERE  group_name = '{group}'
    ) \
    """
    points = retrieve_sql_query(query)
    print("Retrieved points: " + str(points))

    return points


def get_all_groupnames():
    query = 'SELECT group_name FROM groups'
    groups = retrieve_sql_query(query)
    groups = concat_query_result(groups)
    return groups


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
        OR name='saved_points'
    """

    tables = retrieve_sql_query(query)
    print("Current num tables: " + str(len(tables)))
    if len(tables) >= 5:
        return True
    else:
        return False


def initialize_database():
    """
    Create tables if they dont exist already.
    """
    users_table = """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        email VARCHAR(100) NOT NULL,
        longitude REAL,
        latitude REAL,
        picture VARCHAR(255),
        loggedIn BIT DEFAULT 0,
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
        member_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(group_id),
        FOREIGN KEY (member_id) REFERENCES users(user_id),
        UNIQUE (group_id, member_id)
    )
    """

    saved_points_table = """
    CREATE TABLE saved_points (
        point_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        title VARCHAR(50) NOT NULL,
        describtion VARCHAR(50) NOT NULL,
        longitude REAL,
        latitude REAL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES groups(group_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        UNIQUE (group_id, title)
    )
    """

    if not tables_exist():
        print("Creating new tables.")
        execute_sql_statement(users_table)
        execute_sql_statement(friendlists_table)
        execute_sql_statement(groups_table)
        execute_sql_statement(group_members_table)
        execute_sql_statement(saved_points_table)
    else:
        print("Tables already exist.")


if __name__ == '__main__':
    SHOW_USERS = 'SELECT * FROM users'
    SHOW_FRIENDS = 'SELECT * FROM friendlists'
    SHOW_GROUPS = 'SELECT * FROM groups'
    SHOW_MEMBERS = 'SELECT * FROM group_members'
    SHOW_POINTS = 'SELECT * FROM saved_points'

    print("Executing sqlite functions module.")

    initialize_database()

    email = "master@mail"
    friend_mail = "cat@mail"
    friend_mail_2 = "dog@mail"

    # Add users to database
    add_new_user(email)
    add_new_user(friend_mail)
    add_new_user(friend_mail_2)
    retrieve_sql_query(SHOW_USERS)

    # Login user
    user_logged_in(email)
    loggout_all_users()

    # Retrieve users from database
    id = get_user_id(email)

    # Add friends
    add_new_friend(friend_mail, email)
    add_new_friend(friend_mail_2, email)
    retrieve_sql_query(SHOW_FRIENDS)

    # Get Friendlist
    get_friendlist(email)

    # Create new group
    add_new_group(admin=email, groupname="Meat")
    get_grouplist(email)
    retrieve_sql_query(SHOW_GROUPS)

    # Add group members
    add_new_group_members(admin=email, groupname="Meat",
                          new_users=[friend_mail, friend_mail_2])

    # Show groups members
    retrieve_sql_query(SHOW_MEMBERS)
    get_group_memberlist(email, "Meat")

    # Show saved points
    point_payload = {
            "title": 'examplePoint',
            "text": 'kill me please',
            "latitude": 50.79846715949979,
            "longitude": 7.2058313596181565
        }
    save_new_point(point_payload, email, "Meat")
    point_payload = {
            "title": 'examplePoint_2',
            "text": 'kill me please',
            "latitude": 50.79846715949979,
            "longitude": 7.2058313596181565
        }
    save_new_point(point_payload, email, "Meat")
    retrieve_sql_query(SHOW_POINTS)

    get_group_memberlist_and_location('jonasgrop')
