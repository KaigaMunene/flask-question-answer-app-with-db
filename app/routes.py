from app import app
import hashlib

from flask import jsonify, request


from . import app
from app.queries import (
    add_question,
    delete_question,
    retrieve_one_question,
    retrieve_all_questions,
    update_question,
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
            jsonify({"message": "The question exists, please check out the answers"}),
            201,
        )

    add_question(auto_generated_id, title, question)
    return jsonify({"message": "Question posted successfully"}), 201


@app.route(f"{path}/question/<string:question_id>", methods=["GET"])
def get_question(question_id):
    question = retrieve_one_question(question_id)
    if not question:
        return jsonify({"message": "Question doesnt exist"}), 404

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