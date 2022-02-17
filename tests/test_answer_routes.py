import json
import pytest

from app.routes import generate_id

PATH = "/api/v1"
HEADERS = {"Content-Type": "application/json"}

def post_a_question(client, info):
    client.post(f"{PATH}/question", data=json.dumps(info), headers=HEADERS)

def post_an_answer(client, info):
    client.post( f"{PATH}/answer", data=json.dumps(info), headers=HEADERS)



def test_post_answers(client):
    post_question = {
        "title": "Python",
        "question": "What are the various Datatypes of python",
    }
    post_a_question(client, post_question)

    generated_id = generate_id(post_question["title"])

    response = client.post(
        f"{PATH}/answer",
        data=json.dumps(
            {
                "question_id": generated_id,
                "answer": "The various datatypes are integers,boolean,string,float,dictionary,sets,lists and tuples",
            }
        ),
        headers=HEADERS,
    )

    response_data = json.loads(response.data)
    assert response.status_code == 201
    assert response_data.get("message") == "Answer posted successfully"

def test_post_answer_without_question_id_field(client):
    post_question = {
        "title": "Network",
        "question": "What are network systems?",
    }
    post_a_question(client, post_question)

    answer = {
        "question_id": "",
        "answer": "A network ensure connectivity between users or various devices.",
    }
    response = client.post(
        f"{PATH}/answer", data=json.dumps(answer), headers=HEADERS
    )
    res_data = json.loads(response.data)
    assert response.status_code == 404
    assert res_data["message"] == "Question doesnt exist"
    
def test_post_answer_without_answer_field(client):
    post_question = {
        "title": "Python",
        "question": "What are the various Datatypes of python",
    }
    post_a_question(client, post_question)

    generated_id = generate_id(post_question["title"])
    answer = {"question_id": generated_id, "answer": ""}
    response = client.post(
        f"{PATH}/answer", data=json.dumps(answer), headers=HEADERS
    )
    res_data = json.loads(response.data)
    assert response.status_code == 400
    assert res_data["message"] == "Invalid answer, enter a valid answer"

def test_get_answer_for_one_question(client):
    posted_question = {
        "title": "Django",
        "question": "What is Django and why we use it ?",
    }
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    posted_answer = {
        "question_id": generated_id,
        "answer": "Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.",
    }
    post_an_answer(client, posted_answer)

    generated_answer_id = generate_id(posted_answer["answer"])

    response = client.get(
        f"{PATH}/answer/{generated_answer_id}", headers=HEADERS
    )

    answer = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(answer, dict) == True

def test_get_answer_without_answer_id(client):
    posted_question = {
        "title": "React",
        "question": "What is React and why we use it ?",
    }
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    posted_answer = {
        "question_id": generated_id,
        "answer": "Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.",
    }
    post_an_answer(client, posted_answer)

    response = client.get(f"{PATH}/answer/1", headers=HEADERS)

    res_data = json.loads(response.data)
    assert response.status_code == 404
    assert res_data["message"] == "answer not found"

def test_get_all_answers(client):
    posted_question = {
        "title": "Heroku",
        "question": "What is Heroku and why we use it ?",
    }
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])
    post_an_answer(client,
        {
            "question_id": generated_id,
            "answer": "Heroku is a platform, as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.",
        }
    )

    response = client.get(f"{PATH}/answers", headers=HEADERS)
    res_data = json.loads(response.data)
    answers = res_data["answer"]
    assert response.status_code == 200
    assert isinstance(answers, list)

def test_get_all_answers_to_a_question(client):
    posted_question = {
        "title": "Github",
        "question": "What is github and what it is used for ?",
    }
    post_a_question(client, posted_question)
    generated_question_id = generate_id(posted_question["title"])
    post_an_answer(client,
        {
            "question_id": generated_question_id,
            "answer": "Github is a code hosting platform for version control and collaboration. It lets you and others work together on projects from anywhere.",
        }
    )
    response = client.get(
        f"{PATH}/answers/{generated_question_id}", headers=HEADERS
    )
    res_data = json.loads(response.data)
    answers = res_data["answer"]
    assert response.status_code == 200
    assert isinstance(answers, list)


def test_update_answer(client):
    posted_question = {
        "title": "Docker",
        "question": "What is docker and what is it used for ?",
    }
    post_a_question(client, posted_question)

    generated_question_id = generate_id(posted_question["title"])

    post_answer = {
        "question_id": generated_question_id,
        "answer": "Docker is an open source containerization platform. It enables developers to package applications into containers—standardized executable components combining application source code with the operating system (OS) libraries and dependencies required to run that code in any environment.",
    }
    post_an_answer(client, post_answer)

    generated_answer_id = generate_id(post_answer["answer"])

    response = client.put(
        f"{PATH}/answer/{generated_answer_id}",
        data=json.dumps(post_answer),
        headers=HEADERS,
    )
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data["message"] == "answer updated successfully"



def test_delete_answer(client):
    posted_question = {
        "title": "Politics",
        "question": "What is the political situation in Kenya?",
    }
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    posted_answer = {
        "question_id": generated_id,
        "answer": "It's near the time for elections and tensions are arising",
    }
    post_an_answer(client, posted_answer)
    generated_answer_id = generate_id(posted_answer["answer"])
    response = client.delete(
        f"{PATH}/answer/{generated_answer_id}", headers=HEADERS
    )
    assert response.status_code == 204

def test_delete_answer_which_doesnot_exist(client):
    posted_question = {"title": "Gender", "question": "What is your gender?"}
    post_a_question(client, posted_question)

    generated_id = generate_id(posted_question["title"])

    posted_answer = {"question_id": generated_id, "answer": "My gender is male."}
    post_an_answer(client, posted_answer)
    response = client.delete(
        f"{PATH}/answer/1",
        data=json.dumps(posted_answer),
        headers=HEADERS,
    )

    response_data = json.loads(response.data)
    assert response.status_code == 404
    assert response_data["message"] == "Answer not found"