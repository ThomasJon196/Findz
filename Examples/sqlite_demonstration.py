import sqlite3

# Create connection with sqlite database

connection = sqlite3.connect('test.db')

print(connection.total_changes)

# Create table

cursor = connection.cursor()
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")

# Insert data

cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")

# Select data

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

target_fish_name = "Jamie"
rows = cursor.execute(
    "SELECT name, species, tank_number FROM fish WHERE name = ?",
    (target_fish_name,),
).fetchall()
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

# Automatic cleanup
# 
# Connection & Cursor objects should be close when working with them.

from contextlib import closing

with closing(sqlite3.connect("aquarium.db")) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        print(rows)