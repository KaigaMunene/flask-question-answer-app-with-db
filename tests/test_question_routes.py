import json
import pytest

from app.routes import generate_id

PATH = "/api/v1"
HEADERS = {"Content-Type": "application/json"}


def post_a_question(client, info):
    client.post(f"{PATH}/question", data=json.dumps(info), headers=HEADERS)


@pytest.mark.parametrize(
    "data, expected_status_code, expected_msg",
    [
        [
            {"title": "Animals", "question": "Species of animals"},
            201,
            "Question posted successfully",
        ],  # valid data
        [
            {"title": "", "question": "What is a server"},
            400,
            "Invalid title enter a valid title",
        ],  # missing title
        [
            {"title": "Coding", "question": ""},
            400,
            "Invalid question, enter a valid question",
        ],  # missing question
        [
            {"title": "Animals", "question": "Species of animals"},
            303,
            "The question already exists, check the answers",
        ],  # if question already exists
    ],
)
def test_post_a_question(client, data, expected_status_code, expected_msg):
    response = client.post(
        f"{PATH}/question",
        data=json.dumps(data),
        headers=HEADERS,
    )
    response_data = json.loads(response.get_data(client))

    assert response.status_code == expected_status_code
    assert response_data["message"] == expected_msg


def test_get_one_question(client):
    posted_question = {"title": "Program", "question": "what is a program"}
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    response = client.get(f"{PATH}/question/{generated_id}", headers=HEADERS)

    question = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(question, dict) == True
    assert question["title"] == posted_question["title"]
    assert question["question"] == posted_question["question"]


def test_get_one_question_without_question_id(client):
    response = client.get(f"{PATH}/question/1", headers=HEADERS)
    res_data = json.loads(response.data)

    assert response.status_code == 404
    assert res_data["message"] == "Question not found"

def test_update_question(client):
    posted_question = {
        "title": "python",
        "question": "What is python programming language?",
    }
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    response = client.put(
        f"{PATH}/question/{generated_id}",
        data=json.dumps(posted_question),
        headers=HEADERS,
    )
    res_data = json.loads(response.data)

    assert response.status_code == 200
    assert res_data["message"] == "question updated successfully"

def test_for_update_question_with_invalid_question_id(client):
    data = {"title": "why?", "question": "What was the lesson of the day"}

    response = client.put(
        f"{PATH}/question/1",
        data=json.dumps(data),
        headers=HEADERS,
    )
    res_data = json.loads(response.data)

    assert response.status_code == 404 
    assert res_data["message"] == "Question not found"

def test_for_update_question_with_no_title(client):
    data = {"title": "What", "question": "What was the lesson of the day"}
    post_a_question(client, data)

    generated_id = generate_id(data["title"])

    response = client.put(
        f"{PATH}/question/{generated_id}",
        data=json.dumps({"title": "", "question": "Because"}),
        headers=HEADERS,
    )

    res_data = json.loads(response.data)
    assert response.status_code == 400
    assert res_data["message"] == "Invalid title enter a valid title"

def test_update_question_with_no_question_field(client):
    data = {"title": "Tests", "question": "What are the various types of tests?"}
    post_a_question(client, data)

    generated_id = generate_id(data["title"])

    response = client.put(
        f"{PATH}/question/{generated_id}",
        data=json.dumps(
            {
                "title": "Unit Testing",
                "question": "",
            }
        ),
        headers=HEADERS,
    )
    assert response.status_code == 400
    res_data = json.loads(response.data)
    assert res_data["message"] == "Invalid question, enter a valid question"
    
def test_delete_question(client):
    posted_question = {"title": "Exam", "question": "When are the exams?"}
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    response = client.delete(
        f"{PATH}/question/{generated_id}", headers=HEADERS
    )

    assert response.status_code == 204

def test_delete_question_with_invalid_question(client):
    data = {"title": "APIs?", "question": "What are APIs ?"}

    response = client.delete(
        f"{PATH}/question/1",
        data=json.dumps(data),
        headers=HEADERS,
    )
    res_data = json.loads(response.data)

    assert response.status_code == 404
    assert res_data["message"] == "Question not found"