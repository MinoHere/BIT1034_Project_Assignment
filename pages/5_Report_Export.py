from datetime import datetime

import pandas as pd
import streamlit as st

from database.database import get_connection


st.set_page_config(
    page_title="Report Export",
    page_icon="📤",
    layout="wide",
)

st.title("📤 Report Export")

st.write(
    "Generate and download student performance reports "
    "from the SQLite database."
)


@st.cache_data
def load_data():
    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT *
        FROM students
        ORDER BY id
        """,
        connection,
    )

    connection.close()

    return dataframe


try:
    df = load_data()

    if df.empty:
        st.warning("No student records are available.")
        st.stop()

    st.subheader("Report Filters")

    column1, column2, column3 = st.columns(3)

    selected_gender = column1.multiselect(
        "Gender",
        options=sorted(df["gender"].unique().tolist()),
        default=sorted(df["gender"].unique().tolist()),
    )

    selected_age = column2.multiselect(
        "Age",
        options=sorted(df["age"].unique().tolist()),
        default=sorted(df["age"].unique().tolist()),
    )

    selected_grade = column3.multiselect(
        "Final Grade",
        options=sorted(df["final_grade"].unique().tolist()),
        default=sorted(df["final_grade"].unique().tolist()),
    )

    filtered_df = df[
        df["gender"].isin(selected_gender)
        & df["age"].isin(selected_age)
        & df["final_grade"].isin(selected_grade)
    ]

    st.write(f"Selected records: {len(filtered_df):,}")

    if filtered_df.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Records",
        f"{len(filtered_df):,}",
    )

    metric2.metric(
        "Average Attendance",
        f"{filtered_df['attendance'].mean():.2f}%",
    )

    metric3.metric(
        "Average Exam Score",
        f"{filtered_df['exam_score'].mean():.2f}",
    )

    metric4.metric(
        "Average Final Grade",
        f"{filtered_df['final_grade'].mean():.2f}",
    )

    st.subheader("Report Preview")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    filename = (
        "student_performance_report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )

except Exception as error:
    st.error(f"Unable to generate report: {error}")