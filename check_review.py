import sqlite3
import os

DATABASE = os.path.join("instance", "skillbridge.db")

connection = sqlite3.connect(DATABASE)
connection.row_factory = sqlite3.Row

print("\nQUALIFICATION REVIEW RECORDS")

records = connection.execute("""
    SELECT
        qualifications.id,
        users.full_name,
        qualifications.qualification_name,
        qualifications.verification_status,
        qualifications.reviewer_notes,
        qualifications.reviewed_at
    FROM qualifications
    JOIN users
        ON qualifications.user_id = users.id
    ORDER BY qualifications.id DESC
""").fetchall()

for record in records:
    print("\n-----------------------------")
    print("Applicant:", record["full_name"])
    print("Qualification:", record["qualification_name"])
    print("Status:", record["verification_status"])
    print("Review Notes:", record["reviewer_notes"])
    print("Reviewed At:", record["reviewed_at"])

print("\nVERIFICATION AUDIT HISTORY")

history = connection.execute("""
    SELECT
        verification_status,
        decided_at,
        qualification_id,
        admin_id
    FROM certificate_verification_history
    ORDER BY id DESC
""").fetchall()

for item in history:
    print(dict(item))

connection.close()
