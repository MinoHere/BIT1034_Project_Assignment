from database.database import get_connection
from utils.prediction_model import MODEL_PATH


def test_database_connection():
    connection = get_connection()

    result = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()

    connection.close()

    assert result is not None
    assert result[0] > 0


def test_students_table_exists():
    connection = get_connection()

    result = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'students'
        """
    ).fetchone()

    connection.close()

    assert result is not None


def test_model_exists():
    assert MODEL_PATH.exists()


if __name__ == "__main__":
    tests = [
        test_database_connection,
        test_students_table_exists,
        test_model_exists,
    ]

    passed = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError:
            print(f"FAIL: {test.__name__}")
        except Exception as error:
            print(f"ERROR: {test.__name__} - {error}")

    print(f"\nTesting completed: {passed}/{len(tests)} tests passed.")