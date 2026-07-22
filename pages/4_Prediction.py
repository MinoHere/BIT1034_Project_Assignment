import streamlit as st

from utils.prediction_model import MODEL_PATH, predict_grade


st.set_page_config(
    page_title="Grade Prediction",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Student Grade Prediction")

st.write(
    "Enter the student's learning and performance information "
    "to predict the expected final grade."
)

if not MODEL_PATH.exists():
    st.error(
        "Prediction model not found. "
        "Run `py -m utils.prediction_model` in the terminal first."
    )
    st.stop()


with st.form("prediction_form"):
    column1, column2, column3 = st.columns(3)

    study_hours = column1.number_input(
        "Study Hours",
        min_value=0,
        max_value=24,
        value=5,
    )

    attendance = column2.number_input(
        "Attendance (%)",
        min_value=0,
        max_value=100,
        value=80,
    )

    age = column3.number_input(
        "Age",
        min_value=15,
        max_value=100,
        value=20,
    )

    resources = column1.selectbox(
        "Learning Resources",
        options=[0, 1],
        format_func=lambda value: "Available" if value == 1 else "Not Available",
    )

    extracurricular = column2.selectbox(
        "Extracurricular Activities",
        options=[0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )

    motivation = column3.selectbox(
        "Motivation",
        options=[0, 1],
        format_func=lambda value: "High" if value == 1 else "Low",
    )

    internet = column1.selectbox(
        "Internet Access",
        options=[0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )

    gender = column2.selectbox(
        "Gender",
        options=[0, 1],
        format_func=lambda value: "Category 1" if value == 1 else "Category 0",
    )

    learning_style = column3.number_input(
        "Learning Style Code",
        min_value=0,
        value=1,
    )

    online_courses = column1.number_input(
        "Online Courses",
        min_value=0,
        value=2,
    )

    discussions = column2.selectbox(
        "Participates in Discussions",
        options=[0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )

    assignment_completion = column3.number_input(
        "Assignment Completion (%)",
        min_value=0,
        max_value=100,
        value=80,
    )

    exam_score = column1.number_input(
        "Exam Score",
        min_value=0,
        max_value=100,
        value=70,
    )

    edutech = column2.selectbox(
        "Uses Educational Technology",
        options=[0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )

    stress_level = column3.number_input(
        "Stress Level",
        min_value=0,
        value=1,
    )

    submitted = st.form_submit_button(
        "Predict Final Grade",
        use_container_width=True,
    )


if submitted:
    student_data = {
        "study_hours": study_hours,
        "attendance": attendance,
        "resources": resources,
        "extracurricular": extracurricular,
        "motivation": motivation,
        "internet": internet,
        "gender": gender,
        "age": age,
        "learning_style": learning_style,
        "online_courses": online_courses,
        "discussions": discussions,
        "assignment_completion": assignment_completion,
        "exam_score": exam_score,
        "edutech": edutech,
        "stress_level": stress_level,
    }

    try:
        predicted_grade, confidence = predict_grade(student_data)

        result1, result2 = st.columns(2)

        result1.metric(
            "Predicted Final Grade",
            predicted_grade,
        )

        result2.metric(
            "Prediction Confidence",
            f"{confidence * 100:.2f}%",
        )

        if predicted_grade <= 1:
            st.error("Risk level: High")
        elif predicted_grade == 2:
            st.warning("Risk level: Moderate")
        else:
            st.success("Risk level: Low")

    except Exception as error:
        st.error(f"Prediction failed: {error}")