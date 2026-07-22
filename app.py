import streamlit as st

from database.database import get_connection


st.set_page_config(
    page_title="Student Performance System",
    page_icon="🎓",
    layout="wide",
)


def get_summary():
    connection = get_connection()

    total_students = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    average_grade = connection.execute(
        "SELECT AVG(final_grade) FROM students"
    ).fetchone()[0]

    average_attendance = connection.execute(
        "SELECT AVG(attendance) FROM students"
    ).fetchone()[0]

    average_exam_score = connection.execute(
        "SELECT AVG(exam_score) FROM students"
    ).fetchone()[0]

    connection.close()

    return (
        total_students,
        average_grade,
        average_attendance,
        average_exam_score,
    )


st.title("🎓 Student Performance Analysis System")

st.write(
    "This system analyses student performance data stored in "
    "an SQLite database."
)

try:
    (
        total_students,
        average_grade,
        average_attendance,
        average_exam_score,
    ) = get_summary()

    column1, column2, column3, column4 = st.columns(4)

    column1.metric("Total Records", f"{total_students:,}")
    column2.metric("Average Final Grade", f"{average_grade:.2f}")
    column3.metric("Average Attendance", f"{average_attendance:.2f}%")
    column4.metric("Average Exam Score", f"{average_exam_score:.2f}")

    st.success("Database connected successfully.")

except Exception as error:
    st.error(f"Unable to load database: {error}")