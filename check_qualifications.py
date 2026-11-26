import sqlite3
import os

DATABASE = os.path.join("instance", "skillbridge.db")

connection = sqlite3.connect(DATABASE)

columns = connection.execute(
    "PRAGMA table_info(qualifications)"
).fetchall()

print("QUALIFICATIONS TABLE FIELDS:")

for column in columns:
    print(column[1])

connection.close()
