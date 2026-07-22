import streamlit as st


st.set_page_config(
    page_title="About System",
    page_icon="ℹ️",
    layout="wide",
)

st.title("ℹ️ About the System")

st.subheader("Student Performance Analysis System")

st.write(
    """
    The Student Performance Analysis System is a Python-based
    application developed to manage, analyse and predict student
    academic performance.
    """
)

st.subheader("System Objectives")

st.write(
    """
    The main objectives of this system are:
    """
)

st.markdown(
    """
    - To store student performance records in an SQLite database.
    - To import and clean student data from a CSV dataset.
    - To provide CRUD operations for managing student records.
    - To analyse performance using statistical summaries and charts.
    - To predict student final grades using machine learning.
    - To allow users to export filtered reports in CSV format.
    """
)

st.subheader("Technologies Used")

technology1, technology2, technology3 = st.columns(3)

technology1.info(
    """
    Python

    Used for application logic, data processing and machine learning.
    """
)

technology2.info(
    """
    SQLite

    Used as the relational database for storing student records.
    """
)

technology3.info(
    """
    Streamlit

    Used to develop the graphical web interface.
    """
)

technology4, technology5, technology6 = st.columns(3)

technology4.info(
    """
    Pandas

    Used for dataset cleaning, transformation and analysis.
    """
)

technology5.info(
    """
    Plotly

    Used to create interactive data visualisations.
    """
)

technology6.info(
    """
    Scikit-learn

    Used to train the Random Forest prediction model.
    """
)

st.subheader("System Modules")

st.markdown(
    """
    1. Dashboard
    2. Student Records
    3. Performance Analytics
    4. Database Manager
    5. Grade Prediction
    6. Report Export
    """
)

st.subheader("Dataset")

st.write(
    """
    The system uses a student performance dataset containing
    information such as study hours, attendance, learning resources,
    motivation, examination scores, stress levels and final grades.
    """
)

st.subheader("Project Information")

st.write(
    """
    Course: BIT1034 Advanced Programming

    Project Type: Group Project

    Application Type: Student Performance Analysis and Prediction System
    """
)