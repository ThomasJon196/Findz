# SOURCE: https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3
# Dont forget to commit changes!!! connection.commit()!!!

import sqlite3

# Create connection with sqlite database

connection = sqlite3.connect('findz.db')

print(connection.total_changes)

# Create table

users_table = """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        email VARCHAR(100) NOT NULL,
        picture VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (email)
    )
    """
cursor = connection.cursor()
cursor.execute(users_table)


cursor = connection.cursor()
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")

# Insert data

cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
email = "test@mail"
cursor.execute(f"INSERT INTO users (email, picture) VALUES ('{email}', 'dummy')")

# Select data

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

target_fish_name = "Jamie"
rows = cursor.execute(
    "SELECT name, species, tank_number FROM fish WHERE name = ?",
    (target_fish_name,),
).fetchall()
print(rows)

rows = cursor.execute("SELECT * FROM users").fetchall()
print(rows)


# MODIFY DATA

# Update data

new_tank_number = 2
moved_fish_name = "Sammy"
cursor.execute(
    "UPDATE fish SET tank_number = ? WHERE name = ?",
    (new_tank_number, moved_fish_name)
)

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

# Delete data

released_fish_name = "Sammy"
cursor.execute(
    "DELETE FROM fish WHERE name = ?",
    (released_fish_name,)
)

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

cursor.close()
# Automatic cleanup
# 
# Connection & Cursor objects should be close when working with them.

from contextlib import closing

with closing(sqlite3.connect("aquarium.db")) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        print(rows)

# Example user database:

"""
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (email)
);

CREATE TABLE friendlists (
  friendlist_id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  friend_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (friend_id) REFERENCES users(user_id),
  UNIQUE (user_id, friend_id)
);

CREATE TABLE groups (
  group_id INTEGER PRIMARY KEY,
  group_name VARCHAR(50) NOT NULL,
  admin_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (admin_id) REFERENCES users(user_id)
);

CREATE TABLE group_members (
  group_id INTEGER NOT NULL,
  member_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (group_id) REFERENCES groups(group_id),
  FOREIGN KEY (member_id) REFERENCES users(user_id),
  UNIQUE (group_id, member_id)
);



"""