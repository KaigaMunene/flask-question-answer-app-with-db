import json
import unittest

from app import app
from app.routes import generate_id


class TestQuestionRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.path = "/api/v1"
        self.headers = {"Content-Type": "application/json"}

    def post_a_question(self, info):
        self.client.post(
            f"{self.path}/question", data=json.dumps(info), headers=self.headers
        )

    def test_post_a_question(self):
        response = self.client.post(
            f"{self.path}/question",
            data=json.dumps({"title": "Animals", "question": "Species of animals"}),
            headers=self.headers,
        )
        response_data = json.loads(response.get_data())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["message"], "Question posted successfully")

    def test_post_question_without_title(self):
        data = {"title": "", "question": "What is a server"}
        response = self.client.post(
            f"{self.path}/question", data=json.dumps(data), headers=self.headers
        )
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(res_data["message"], "Invalid title enter a valid title")

    def test_post_question_without_question_field(self):
        data = {"title": "Coding", "question": ""}
        response = self.client.post(
            f"{self.path}/question", data=json.dumps(data), headers=self.headers
        )
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            res_data["message"],
            "Invalid question, enter a valid question",
        )

    def test_get_all_questions(self):
        # get all questions currently existing
        res = self.client.get(f"{self.path}/question", headers=self.headers)
        res_data = json.loads(res.data)
        questions = res_data["question"]
        previous_count = len(questions)

        # post question
        self.post_a_question({"title": "name", "question": "what is your name"})

        # get all questions after adding a question
        response = self.client.get(f"{self.path}/question", headers=self.headers)
        response_data = json.loads(response.data)
        questions = response_data["question"]

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(questions, list)
        self.assertEqual(len(questions), previous_count + 1)

    def test_get_one_question(self):
        posted_question = {"title": "Program", "question": "what is a program"}
        self.post_a_question(posted_question)

        generated_id = generate_id(posted_question["title"])

        response = self.client.get(
            f"{self.path}/question/{generated_id}", headers=self.headers
        )

        res_data = json.loads(response.data)
        question = res_data["question"]

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(question, dict)
        self.assertEqual(question["title"], posted_question["title"])
        self.assertEqual(question["question"], posted_question["question"])

    def test_get_one_question_without_question_id(self):
        response = self.client.get(f"{self.path}/question/1", headers=self.headers)
        res_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_data["message"], "Question not found")

    def test_update_question(self):
        posted_question = {
            "title": "python",
            "question": "What is python programming language?",
        }
        self.post_a_question(posted_question)

        generated_id = generate_id(posted_question["title"])

        response = self.client.put(
            f"{self.path}/question/{generated_id}",
            data=json.dumps(posted_question),
            headers=self.headers,
        )
        res_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_data["message"], "question updated successfully")

    def test_for_update_question_with_invalid_question_id(self):
        data = {"title": "why?", "question": "What was the lesson of the day"}

        response = self.client.put(
            f"{self.path}/question/1",
            data=json.dumps(data),
            headers=self.headers,
        )
        res_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_data["message"], "Question not found")

    def test_for_update_question_with_no_title(self):
        data = {"title": "What", "question": "What was the lesson of the day"}
        self.post_a_question(data)

        generated_id = generate_id(data["title"])

        response = self.client.put(
            f"{self.path}/question/{generated_id}",
            data=json.dumps({"title": "", "question": "Because"}),
            headers=self.headers,
        )

        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(res_data["message"], "Invalid title enter a valid title")

    def test_update_question_with_no_question_field(self):
        data = {"title": "Tests", "question": "What are the various types of tests?"}
        self.post_a_question(data)

        generated_id = generate_id(data["title"])

        response = self.client.put(
            f"{self.path}/question/{generated_id}",
            data=json.dumps(
                {
                    "title": "Unit Testing",
                    "question": "",
                }
            ),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)
        res_data = json.loads(response.data)
        self.assertEqual(
            res_data["message"], "Invalid question, enter a valid question"
        )

    def test_delete_question(self):
        posted_question = {"title": "Exam", "question": "When are the exams?"}
        self.post_a_question(posted_question)

        generated_id = generate_id(posted_question["title"])

        response = self.client.delete(
            f"{self.path}/question/{generated_id}", headers=self.headers
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_question_with_invalid_question(self):
        data = {"title": "APIs?", "question": "What are APIs ?"}

        response = self.client.delete(
            f"{self.path}/question/1",
            data=json.dumps(data),
            headers=self.headers,
        )
        res_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_data["message"], "Question not found")
