from multiprocessing import connection
from webbrowser import get
from app import get_connection


def add_question(question_id, title, question):
    connection = get_connection()
    query = """
    INSERT INTO questions(
        id, title, question
    ) VALUES (?,?,?)
    """
    connection.execute(query, (question_id, title, question))

    connection.commit()  # saves changes made

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


def add_an_answer(question_id, answer_id, answer):
    connection = get_connection()
    query = """
    INSERT INTO answers(question_id, id, answer)
    VALUES (?,?,?)
    """

    connection.execute(query, (question_id, answer_id, answer))

    connection.commit()

    connection.close()
    return "answer added successfully"


def retrieve_an_answer(answer_id):
    connection = get_connection()
    query = "SELECT * FROM answers WHERE id=?"
    answer = connection.execute(query, (answer_id,)).fetchone()

    asw = None
    if answer:
        asw = {
            "answer_id": answer[0],
            "answer": answer[1],
            "question_id": answer[2],
        }

    connection.close()

    return asw


def retrieve_all_answers():
    connection = get_connection()
    query = "SELECT * FROM answers"
    answers = connection.execute(query).fetchall()

    all_answers = []
    for answer in answers:
        asw = {"answer_id": answer[0], "answer": answer[1], "question_id": answer[2]}
        all_answers.append(asw)
    return all_answers

def update_an_answer(answer_id, answer):
    connection = get_connection()
    query = "UPDATE answers SET answer=? WHERE id=?"

    connection.execute(query, (answer, answer_id))
    connection.commit()
    connection.close()
    return "Answer updated successfully"

def delete_answer(answer_id):
    connection = get_connection()
    query = "DELETE FROM answers WHERE id=?"

    connection.execute(query, (answer_id,))
    connection.commit()
    connection.close()
    return "Answer deleted successfully"
