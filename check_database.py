from database.database import get_connection


connection = get_connection()

tables = connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

total_students = connection.execute(
    "SELECT COUNT(*) FROM students"
).fetchone()[0]

first_five = connection.execute(
    "SELECT * FROM students LIMIT 5"
).fetchall()

print("Tables:", [row[0] for row in tables])
print("Total records:", total_students)

print("\nFirst 5 records:")

for record in first_five:
    print(dict(record))

connection.close()