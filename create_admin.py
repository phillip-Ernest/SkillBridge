import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "instance",
    "skillbridge.db"
)

connection = sqlite3.connect(DATABASE)
connection.row_factory = sqlite3.Row

email = input("Enter administrator email: ").strip().lower()
password = input("Create administrator password: ")

if not email or len(password) < 8:
    print("Enter a valid email and password of at least 8 characters.")
else:
    user = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if user:
        connection.execute("""
            UPDATE users
            SET role = 'admin',
                password = ?
            WHERE email = ?
        """, (
            generate_password_hash(password),
            email
        ))

        connection.commit()
        print("Administrator account created successfully.")

    else:
        print("User not found. Register this user first.")

connection.close()
