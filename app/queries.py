from app import get_connection


def add_question(question_id, title, question):
    connection = get_connection()
    query = """
    INSERT INTO questions(
        id, title, question
    ) VALUES (?,?,?)
    """
    connection.execute(query, (question_id, title, question))

    connection.commit()  # save changes made

    connection.close()
    return "Question posted successfully"


def retrieve_one_question(question_id):
    connection = get_connection()
    query = "SELECT * FROM questions WHERE id=?"

    question = connection.execute(query, (question_id,)).fetchone()

    qs = None

    if question:
        qs = {"question_id": question[0], "title": question[1], "question": question[2]}

    connection.close()

    return qs


def retrieve_all_questions():
    connection = get_connection()
    query = "SELECT * FROM questions"

    questions = connection.execute(query).fetchall()

    all_questions = []
    for question in questions:
        qs = {
            "question_id": question[0],
            "title": question[1],
            "question": question[2],
        }
        all_questions.append(qs)
    return all_questions


def update_question(title, question, question_id):
    connection = get_connection()
    query = """UPDATE questions SET title=?, question=? WHERE id=?"""

    connection.execute(query, (title, question, question_id))

    connection.commit()

    connection.close()
    return "Question updated successfully"


def delete_question(question_id):
    connection = get_connection()
    query = "DELETE FROM questions WHERE id=?"

    connection.execute(query, (question_id,))
    connection.commit()
    connection.close()
    return "Question deleted successfully"
