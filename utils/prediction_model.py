from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from database.database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "student_grade_model.pkl"


FEATURE_COLUMNS = [
    "study_hours",
    "attendance",
    "resources",
    "extracurricular",
    "motivation",
    "internet",
    "gender",
    "age",
    "learning_style",
    "online_courses",
    "discussions",
    "assignment_completion",
    "exam_score",
    "edutech",
    "stress_level",
]

TARGET_COLUMN = "final_grade"


def load_training_data():
    """Load model features and target values from SQLite."""
    connection = get_connection()

    dataframe = pd.read_sql_query(
        f"""
        SELECT
            {", ".join(FEATURE_COLUMNS)},
            {TARGET_COLUMN}
        FROM students
        """,
        connection,
    )

    connection.close()

    return dataframe


def train_model():
    """Train and save a Random Forest classification model."""
    MODEL_DIR.mkdir(exist_ok=True)

    dataframe = load_training_data()

    if dataframe.empty:
        raise ValueError("No student records are available for training.")

    dataframe = dataframe.dropna()

    features = dataframe[FEATURE_COLUMNS]
    target = dataframe[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42,
        stratify=target,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(model, MODEL_PATH)

    print(f"Training records: {len(x_train):,}")
    print(f"Testing records: {len(x_test):,}")
    print(f"Model accuracy: {accuracy:.4f}")
    print(f"Model saved at: {MODEL_PATH}")

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    return model, accuracy


def load_model():
    """Load the trained prediction model."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "The trained model was not found. Run the training script first."
        )

    return joblib.load(MODEL_PATH)


def predict_grade(student_data):
    """Predict the final grade for one student record."""
    model = load_model()

    input_dataframe = pd.DataFrame(
        [student_data],
        columns=FEATURE_COLUMNS,
    )

    prediction = model.predict(input_dataframe)[0]
    probabilities = model.predict_proba(input_dataframe)[0]

    confidence = probabilities.max()

    return int(prediction), float(confidence)


if __name__ == "__main__":
    try:
        train_model()
    except Exception as error:
        print(f"Model training failed: {error}")