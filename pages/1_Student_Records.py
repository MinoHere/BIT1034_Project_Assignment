import pandas as pd
import streamlit as st

from utils.database_helper import (
    get_all_students,
    search_students
)

st.title("👨‍🎓 Student Records")

search = st.text_input(
    "Search by Age"
)

if search:

    students = search_students(search)

else:

    students = get_all_students()

students = [dict(row) for row in students]

df = pd.DataFrame(students)

st.dataframe(
    df,
    use_container_width=True
)

st.write(f"Total Records : {len(df)}")