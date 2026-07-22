from database.database import get_connection


def get_all_students():
    connection = get_connection()

    query = """
    SELECT *
    FROM students
    ORDER BY id
    """

    data = connection.execute(query).fetchall()

    connection.close()

    return data


def search_students(keyword):

    connection = get_connection()

    query = """
    SELECT *
    FROM students
    WHERE
    age LIKE ?
    """

    data = connection.execute(
        query,
        (f"%{keyword}%",)
    ).fetchall()

    connection.close()

    return data


def delete_student(student_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    connection.commit()

    connection.close()


def get_total_students():

    connection = get_connection()

    total = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    connection.close()

    return total