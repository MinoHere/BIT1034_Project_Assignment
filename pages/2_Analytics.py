import pandas as pd
import plotly.express as px
import streamlit as st

from database.database import get_connection


st.set_page_config(
    page_title="Performance Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Performance Analytics")
st.write(
    "This page presents statistical summaries and visualisations "
    "based on student performance records."
)


@st.cache_data
def load_student_data():
    """Load all student records from SQLite into a DataFrame."""
    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT
            id,
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
        FROM students
        """,
        connection,
    )

    connection.close()

    return dataframe


try:
    df = load_student_data()

    if df.empty:
        st.warning("No student records were found in the database.")
        st.stop()

    average_study_hours = df["study_hours"].mean()
    highest_exam_score = df["exam_score"].max()
    lowest_exam_score = df["exam_score"].min()
    average_assignment = df["assignment_completion"].mean()

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Average Study Hours",
        f"{average_study_hours:.2f}",
    )

    metric2.metric(
        "Highest Exam Score",
        f"{highest_exam_score}",
    )

    metric3.metric(
        "Lowest Exam Score",
        f"{lowest_exam_score}",
    )

    metric4.metric(
        "Average Assignment Completion",
        f"{average_assignment:.2f}%",
    )

    st.divider()

    st.subheader("Filters")

    filter1, filter2, filter3 = st.columns(3)

    selected_gender = filter1.multiselect(
        "Gender",
        options=sorted(df["gender"].unique().tolist()),
        default=sorted(df["gender"].unique().tolist()),
    )

    selected_age = filter2.multiselect(
        "Age",
        options=sorted(df["age"].unique().tolist()),
        default=sorted(df["age"].unique().tolist()),
    )

    selected_stress = filter3.multiselect(
        "Stress Level",
        options=sorted(df["stress_level"].unique().tolist()),
        default=sorted(df["stress_level"].unique().tolist()),
    )

    filtered_df = df[
        df["gender"].isin(selected_gender)
        & df["age"].isin(selected_age)
        & df["stress_level"].isin(selected_stress)
    ]

    st.write(f"Filtered records: {len(filtered_df):,}")

    if filtered_df.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("Final Grade Distribution")

        grade_counts = (
            filtered_df["final_grade"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        grade_counts.columns = [
            "Final Grade",
            "Number of Students",
        ]

        grade_chart = px.bar(
            grade_counts,
            x="Final Grade",
            y="Number of Students",
            title="Number of Students by Final Grade",
        )

        st.plotly_chart(
            grade_chart,
            use_container_width=True,
        )

    with chart2:
        st.subheader("Stress Level Distribution")

        stress_counts = (
            filtered_df["stress_level"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        stress_counts.columns = [
            "Stress Level",
            "Number of Students",
        ]

        stress_chart = px.pie(
            stress_counts,
            names="Stress Level",
            values="Number of Students",
            title="Students by Stress Level",
            hole=0.4,
        )

        st.plotly_chart(
            stress_chart,
            use_container_width=True,
        )

    chart3, chart4 = st.columns(2)

    with chart3:
        st.subheader("Attendance and Exam Score")

        attendance_analysis = (
            filtered_df.groupby(
                "attendance",
                as_index=False,
            )["exam_score"]
            .mean()
            .sort_values("attendance")
        )

        attendance_chart = px.line(
            attendance_analysis,
            x="attendance",
            y="exam_score",
            markers=True,
            title="Average Exam Score by Attendance",
            labels={
                "attendance": "Attendance",
                "exam_score": "Average Exam Score",
            },
            render_mode="svg",
        )

        st.plotly_chart(
            attendance_chart,
            use_container_width=True,
        )

    with chart4:
        st.subheader("Study Hours and Exam Score")

        study_analysis = (
            filtered_df.groupby(
                "study_hours",
                as_index=False,
            )["exam_score"]
            .mean()
            .sort_values("study_hours")
        )

        study_chart = px.line(
            study_analysis,
            x="study_hours",
            y="exam_score",
            markers=True,
            title="Average Exam Score by Study Hours",
            labels={
                "study_hours": "Study Hours",
                "exam_score": "Average Exam Score",
            },
            render_mode="svg",
        )

        st.plotly_chart(
            study_chart,
            use_container_width=True,
        )

        st.subheader("Average Exam Score by Age")

        age_analysis = (
            filtered_df.groupby(
                "age",
                as_index=False,
            )["exam_score"]
            .mean()
            .sort_values("age")
        )

        age_chart = px.line(
            age_analysis,
            x="age",
            y="exam_score",
            markers=True,
            title="Average Exam Score by Student Age",
            labels={
                "age": "Age",
                "exam_score": "Average Exam Score",
            },
        )

        st.plotly_chart(
            age_chart,
            use_container_width=True,
        )

        st.subheader("Correlation Matrix")

        correlation_columns = [
            "study_hours",
            "attendance",
            "age",
            "online_courses",
            "discussions",
            "assignment_completion",
            "exam_score",
            "stress_level",
            "final_grade",
        ]

        correlation_matrix = filtered_df[
            correlation_columns
        ].corr()

        correlation_chart = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            aspect="auto",
            title="Correlation Between Performance Variables",
        )

        st.plotly_chart(
            correlation_chart,
            use_container_width=True,
        )

except Exception as error:
    st.error(f"Unable to load analytics: {error}")