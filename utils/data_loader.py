from pathlib import Path

import pandas as pd

from database.database import create_students_table, get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "student_performance.csv"


COLUMN_MAPPING = {
    "StudyHours": "study_hours",
    "Attendance": "attendance",
    "Resources": "resources",
    "Extracurricular": "extracurricular",
    "Motivation": "motivation",
    "Internet": "internet",
    "Gender": "gender",
    "Age": "age",
    "LearningStyle": "learning_style",
    "OnlineCourses": "online_courses",
    "Discussions": "discussions",
    "AssignmentCompletion": "assignment_completion",
    "ExamScore": "exam_score",
    "EduTech": "edutech",
    "StressLevel": "stress_level",
    "FinalGrade": "final_grade",
}


def load_and_clean_dataset():
    """Read and validate the student-performance dataset."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

    dataframe = pd.read_csv(CSV_PATH)

    missing_columns = [
        column for column in COLUMN_MAPPING
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    dataframe = dataframe[list(COLUMN_MAPPING.keys())].copy()

    before_cleaning = len(dataframe)

    dataframe = dataframe.drop_duplicates()
    dataframe = dataframe.dropna()

    numeric_columns = list(COLUMN_MAPPING.keys())

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe = dataframe.dropna()
    dataframe = dataframe.astype(int)

    dataframe = dataframe.rename(columns=COLUMN_MAPPING)

    removed_rows = before_cleaning - len(dataframe)

    print(f"Original rows: {before_cleaning}")
    print(f"Clean rows: {len(dataframe)}")
    print(f"Removed rows: {removed_rows}")

    return dataframe


def import_dataset():
    """Import the cleaned CSV records into SQLite."""
    create_students_table()
    dataframe = load_and_clean_dataset()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students")

    dataframe.to_sql(
        name="students",
        con=connection,
        if_exists="append",
        index=False,
    )

    connection.commit()

    total_records = cursor.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    connection.close()

    print(f"Successfully imported {total_records} records into SQLite.")


if __name__ == "__main__":
    try:
        import_dataset()
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Import failed: {error}")