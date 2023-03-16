from django.test import TestCase
from tasks.models import Projects
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):  #  доступность стартовой страницы
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get("http://127.0.0.1:8000/")
        self.assertEqual(response.status_code, 200)


class APITestCase(TestCase):  # тест APi
    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов"""
        cls.user = User.objects.create(
            username="test", first_name="test", last_name="test", email="test@gmail.com"
        )
        cls.project = Projects.objects.create(
            title="My test project",
            owner=cls.user,
            description="Test description",
            completed=False,
        )

    def test_api_response(self):  # ответ api
        """The index page loads properly"""
        response = self.client.get("http://127.0.0.1:8000/api/project/")
        self.assertEqual(response.status_code, 200)

    def test_api_project(self):  # данные о проекте
        """The index page loads properly"""
        response = self.client.get("http://127.0.0.1:8000/api/project/")
        self.assertEqual(response.json()["results"][0]["title"], "My test project")
