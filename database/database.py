import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "student_performance.db"


def get_connection():
    """Return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_students_table():
    """Create the students table using the dataset columns."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_hours INTEGER NOT NULL,
            attendance INTEGER NOT NULL,
            resources INTEGER NOT NULL,
            extracurricular INTEGER NOT NULL,
            motivation INTEGER NOT NULL,
            internet INTEGER NOT NULL,
            gender INTEGER NOT NULL,
            age INTEGER NOT NULL,
            learning_style INTEGER NOT NULL,
            online_courses INTEGER NOT NULL,
            discussions INTEGER NOT NULL,
            assignment_completion INTEGER NOT NULL,
            exam_score INTEGER NOT NULL,
            edutech INTEGER NOT NULL,
            stress_level INTEGER NOT NULL,
            final_grade INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_students_table()
    print("Database and students table created successfully.")
    print(f"Database location: {DATABASE_PATH}")