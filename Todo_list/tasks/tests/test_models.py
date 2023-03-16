from django.test import TestCase
from tasks.models import Profile, Projects, Sprint
from django.contrib.auth.models import User
from datetime import datetime


class ProfileTests(TestCase):
    """Тесты для модели Profile"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""

        cls.user = User.objects.create(
            username="test", first_name="test", last_name="test", email="test@gmail.com"
        )

        # print(Profile.objects.get(name="test").email)

    def test_verbose_name(self):
        real_verbose_name = Profile._meta.get_field("email").verbose_name
        expected_verbose_name = "Email"

        self.assertEqual(real_verbose_name, expected_verbose_name)

    def test_max_length(self):
        """Тест параметра max_length"""

        real_max_length = Profile._meta.get_field("email").max_length

        self.assertEqual(real_max_length, 256)

    def test_unique(self):
        """Тест параметра unique"""

        real_unique = Profile._meta.get_field("email").unique

        self.assertEqual(real_unique, False)

    def test_model_verbose_name(self):

        self.assertEqual(Profile._meta.verbose_name, "Профиль")


class ProjectTest(TestCase):
    """тест для модели Project (метод save)"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        cls.user = User.objects.create(
            username="test", first_name="test", last_name="test", email="test@gmail.com"
        )

    def test_project_complet(self):  #  проект завершен
        project = Projects.objects.create(
            title="My test project",
            owner=self.user,
            description="Test description",
            completed=True,
        )

        project.save()
        self.assertEqual(project.completed_time.year, datetime.now().year)

    def test_project_not_complet(self):  #  проект не завершен
        project = Projects.objects.create(
            title="My test project",
            owner=self.user,
            description="Test description",
            completed=False,
        )

        project.save()
        self.assertEqual(project.completed_time, None)


class SprintTest(TestCase):
    """тест для модели Sprint (метод save)"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        cls.user = User.objects.create(
            username="test", first_name="test", last_name="test", email="test@gmail.com"
        )
        cls.project = Projects.objects.create(
            title="My test project",
            owner=cls.user,
            description="Test description",
            completed=True,
        )

    def test_project_complet(self):  #  спринт завершен
        sprint = Sprint.objects.create(
            title="My test spint",
            owner=self.user,
            project=self.project,
            description="Test description",
            completed=True,
        )

        sprint.save()
        self.assertEqual(sprint.completed_time.year, datetime.now().year)
