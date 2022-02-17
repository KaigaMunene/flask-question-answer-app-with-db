from app import app
import hashlib

from flask import jsonify, request


from . import app
from app.queries import (
    add_question,
    delete_answer,
    delete_question,
    retrieve_all_answers,
    retrieve_all_answers_for_a_question,
    retrieve_an_answer,
    retrieve_one_question,
    retrieve_all_questions,
    update_an_answer,
    update_question,
    add_an_answer,
)


path = "/api/v1"


def generate_id(message):
    """
    function to generate a hash given a string.
    """
    hash = hashlib.sha256(message.encode("utf-8")).hexdigest()
    return hash[:10]


path = "/api/v1/"


@app.route(f"{path}")
def hello():
    return "Hello World"


@app.route(f"{path}/question", methods=["POST"])
def post_question():
    data = request.get_json()
    title = data.get("title")
    question = data.get("question")
    if not title:
        return jsonify({"message": "Invalid title enter a valid title"}), 400
    if not question:
        return jsonify({"message": "Invalid question, enter a valid question"}), 400

    auto_generated_id = generate_id(title)

    if retrieve_one_question(auto_generated_id):
        return (
            jsonify({"message": "The question already exists, check the answers"}),
            303,
        )

    add_question(auto_generated_id, title, question)
    return jsonify({"message": "Question posted successfully"}), 201


@app.route(f"{path}/question/<string:question_id>", methods=["GET"])
def get_question(question_id):
    question = retrieve_one_question(question_id)
    if not question:
        return jsonify({"message": "Question not found"}), 404

    return jsonify(question), 200


@app.route(f"{path}/question", methods=["GET"])
def get_all_questions():
    questions = retrieve_all_questions()
    return jsonify(questions), 200


@app.route(f"{path}/question/<string:question_id>", methods=["PUT"])
def update_a_question(question_id):
    data = request.get_json()

    title = data.get("title")
    question = data.get("question")

    if retrieve_one_question(question_id) is None:
        return jsonify({"message": "Question not found"}), 404

    if not title:
        return jsonify({"message": "Invalid title enter a valid title"}), 400

    if not question:
        return jsonify({"message": "Invalid question, enter a valid question"}), 400

    update_question(title, question, question_id)
    return jsonify({"message": "question updated successfully"}), 200


@app.route(f"{path}/question/<string:question_id>", methods=["DELETE"])
def delete_a_question(question_id):
    if retrieve_one_question(question_id) is None:
        return jsonify({"message": "Question not found"}), 404

    delete_question(question_id)
    return jsonify({"message": "Question successfully deleted"}), 204


@app.route(f"{path}/answer", methods=["POST"])
def add_answer():
    data = request.get_json()
    question_id = data.get("question_id")
    answer = data.get("answer")
    generated_answer_id = generate_id(answer)
    if not retrieve_one_question(question_id):
        return (
            jsonify({"message": "Question doesnt exist"}),
            404,
        )
    if retrieve_an_answer(generated_answer_id):
        return jsonify({"message": "answer already exists check the answers"}), 400
    if not answer:
        return jsonify({"message": "Invalid answer, enter a valid answer"}), 400
    add_an_answer(question_id, generated_answer_id, answer)
    return jsonify({"message": "Answer posted successfully"}), 201


@app.route(f"{path}/answer/<string:answer_id>", methods=["GET"])
def get_an_answer(answer_id):
    answer = retrieve_an_answer(answer_id)
    if answer is None:
        return jsonify({"message": "answer not found"}), 404
    return jsonify({"answer": answer}), 200


@app.route(f"{path}/answers", methods=["GET"])
def get_all_answers():
    answers = retrieve_all_answers()
    return jsonify({"answer": answers})

@app.route(f"{path}/answers/<string:question_id>", methods=["GET"])
def get_all_answers_to_a_question(question_id):
    answers = retrieve_all_answers_for_a_question(question_id)
    return jsonify({"answer": answers})

@app.route(f"{path}/answer/<string:answer_id>", methods=["PUT"])
def update_answer(answer_id):
    data = request.get_json()
    answer = data.get("answer")
    if retrieve_an_answer(answer_id) is None:
        return jsonify({"message": "Answer not found"}), 404
    update_an_answer(answer_id, answer)
    return jsonify({"message": "answer updated successfully"}), 200


@app.route(f"{path}/answer/<string:answer_id>", methods=["DELETE"])
def delete_an_answer(answer_id):
    if retrieve_an_answer(answer_id) is None:
        return jsonify({"message": "Answer not found"}), 404
    delete_answer(answer_id)
    return jsonify({"message": "Question successfully deleted"}), 204
