import pandas as pd
import streamlit as st

from database.database import get_connection


st.set_page_config(
    page_title="Database Manager",
    page_icon="🗄️",
    layout="wide",
)

st.title("🗄️ Database Manager")
st.write(
    "Manage student records stored in the SQLite database."
)


def get_student_by_id(student_id):
    connection = get_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()

    connection.close()

    return student


def add_student(student_data):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO students (
            study_hours,
            attendance,
            resources,
            extracurricular,
            motivation,
            internet,
            gender,
            age,
            learning_style,
            online_courses,
            discussions,
            assignment_completion,
            exam_score,
            edutech,
            stress_level,
            final_grade
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        student_data,
    )

    connection.commit()
    connection.close()


def update_student(student_id, student_data):
    connection = get_connection()

    connection.execute(
        """
        UPDATE students
        SET
            study_hours = ?,
            attendance = ?,
            resources = ?,
            extracurricular = ?,
            motivation = ?,
            internet = ?,
            gender = ?,
            age = ?,
            learning_style = ?,
            online_courses = ?,
            discussions = ?,
            assignment_completion = ?,
            exam_score = ?,
            edutech = ?,
            stress_level = ?,
            final_grade = ?
        WHERE id = ?
        """,
        (*student_data, student_id),
    )

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )

    connection.commit()
    connection.close()


def get_recent_students():
    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 20
        """,
        connection,
    )

    connection.close()

    return dataframe


def student_form(prefix, default_values=None):
    if default_values is None:
        default_values = {
            "study_hours": 0,
            "attendance": 0,
            "resources": 0,
            "extracurricular": 0,
            "motivation": 0,
            "internet": 0,
            "gender": 0,
            "age": 18,
            "learning_style": 0,
            "online_courses": 0,
            "discussions": 0,
            "assignment_completion": 0,
            "exam_score": 0,
            "edutech": 0,
            "stress_level": 0,
            "final_grade": 0,
        }

    column1, column2 = st.columns(2)

    study_hours = column1.number_input(
        "Study Hours",
        min_value=0,
        max_value=24,
        value=int(default_values["study_hours"]),
        key=f"{prefix}_study_hours",
    )

    attendance = column2.number_input(
        "Attendance",
        min_value=0,
        max_value=100,
        value=int(default_values["attendance"]),
        key=f"{prefix}_attendance",
    )

    resources = column1.selectbox(
        "Resources",
        options=[0, 1],
        index=int(default_values["resources"]),
        key=f"{prefix}_resources",
    )

    extracurricular = column2.selectbox(
        "Extracurricular",
        options=[0, 1],
        index=int(default_values["extracurricular"]),
        key=f"{prefix}_extracurricular",
    )

    motivation = column1.selectbox(
        "Motivation",
        options=[0, 1],
        index=int(default_values["motivation"]),
        key=f"{prefix}_motivation",
    )

    internet = column2.selectbox(
        "Internet Access",
        options=[0, 1],
        index=int(default_values["internet"]),
        key=f"{prefix}_internet",
    )

    gender = column1.selectbox(
        "Gender",
        options=[0, 1],
        index=int(default_values["gender"]),
        key=f"{prefix}_gender",
    )

    age = column2.number_input(
        "Age",
        min_value=15,
        max_value=100,
        value=int(default_values["age"]),
        key=f"{prefix}_age",
    )

    learning_style = column1.number_input(
        "Learning Style",
        min_value=0,
        value=int(default_values["learning_style"]),
        key=f"{prefix}_learning_style",
    )

    online_courses = column2.number_input(
        "Online Courses",
        min_value=0,
        value=int(default_values["online_courses"]),
        key=f"{prefix}_online_courses",
    )

    discussions = column1.selectbox(
        "Discussions",
        options=[0, 1],
        index=int(default_values["discussions"]),
        key=f"{prefix}_discussions",
    )

    assignment_completion = column2.number_input(
        "Assignment Completion",
        min_value=0,
        max_value=100,
        value=int(default_values["assignment_completion"]),
        key=f"{prefix}_assignment_completion",
    )

    exam_score = column1.number_input(
        "Exam Score",
        min_value=0,
        max_value=100,
        value=int(default_values["exam_score"]),
        key=f"{prefix}_exam_score",
    )

    edutech = column2.selectbox(
        "EduTech Usage",
        options=[0, 1],
        index=int(default_values["edutech"]),
        key=f"{prefix}_edutech",
    )

    stress_level = column1.number_input(
        "Stress Level",
        min_value=0,
        value=int(default_values["stress_level"]),
        key=f"{prefix}_stress_level",
    )

    final_grade = column2.number_input(
        "Final Grade",
        min_value=0,
        value=int(default_values["final_grade"]),
        key=f"{prefix}_final_grade",
    )

    return (
        study_hours,
        attendance,
        resources,
        extracurricular,
        motivation,
        internet,
        gender,
        age,
        learning_style,
        online_courses,
        discussions,
        assignment_completion,
        exam_score,
        edutech,
        stress_level,
        final_grade,
    )


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "➕ Add",
        "✏️ Update",
        "🗑️ Delete",
        "📋 Recent Records",
    ]
)


with tab1:
    st.subheader("Add New Student Record")

    with st.form("add_student_form"):
        new_student_data = student_form("add")

        submitted = st.form_submit_button(
            "Add Student",
            use_container_width=True,
        )

        if submitted:
            add_student(new_student_data)
            st.success("Student record added successfully.")


with tab2:
    st.subheader("Update Student Record")

    update_id = st.number_input(
        "Enter Student Record ID",
        min_value=1,
        step=1,
        key="update_id",
    )

    if st.button("Load Student", key="load_student"):
        student = get_student_by_id(update_id)

        if student is None:
            st.error("Student record was not found.")
        else:
            st.session_state["student_to_update"] = dict(student)

    if "student_to_update" in st.session_state:
        selected_student = st.session_state["student_to_update"]

        st.info(
            f"Editing student record ID: {selected_student['id']}"
        )

        with st.form("update_student_form"):
            updated_student_data = student_form(
                "update",
                selected_student,
            )

            submitted = st.form_submit_button(
                "Update Student",
                use_container_width=True,
            )

            if submitted:
                update_student(
                    selected_student["id"],
                    updated_student_data,
                )

                st.success("Student record updated successfully.")

                del st.session_state["student_to_update"]


with tab3:
    st.subheader("Delete Student Record")

    delete_id = st.number_input(
        "Enter Student Record ID",
        min_value=1,
        step=1,
        key="delete_id",
    )

    student_to_delete = get_student_by_id(delete_id)

    if student_to_delete is None:
        st.warning("No student record found for this ID.")
    else:
        st.write("Selected record:")
        st.dataframe(
            pd.DataFrame([dict(student_to_delete)]),
            use_container_width=True,
        )

        confirmation = st.checkbox(
            "I confirm that I want to delete this record."
        )

        if st.button(
            "Delete Student",
            type="primary",
            disabled=not confirmation,
        ):
            delete_student(delete_id)
            st.success("Student record deleted successfully.")
            st.rerun()


with tab4:
    st.subheader("Most Recent Student Records")

    recent_students = get_recent_students()

    st.dataframe(
        recent_students,
        use_container_width=True,
        hide_index=True,
    )