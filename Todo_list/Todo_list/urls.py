from django.contrib import admin
from django.urls import path, include
from tasks import views
from django.contrib.auth import views as auth_views
from tasks.views import (
    TasksListView,
    TasksCreateView,
    TasksDeleteView,
    TaskUpdateView,
    TasksCompleteListView,
    ProjectsCreateView,
    SprintCreateView,
    SprintsListView,
    SprintUpdateView,
    SprintDeleteView,
    ProjectViewSet,
    TasksListAllView,
    StatusCreateView,
    ProjectOpenView,
    ProjectDeleteView,
)

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"project", ProjectViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("uncompleted_tasks/", TasksListView.as_view(), name="tasksList"),
    path("uncompleted_tasks_all/", TasksListAllView.as_view(), name="tasksList"),
    path("uncompleted_sprints/", SprintsListView.as_view(), name="sprintList"),
    path("add_tasks/", TasksCreateView.as_view()),
    path("add_sprint/", SprintCreateView.as_view()),
    path("add_project/", ProjectsCreateView.as_view()),
    path("add_status/", StatusCreateView.as_view()),
    path("open_project/<int:pk>", ProjectOpenView.as_view(), name="open_project"),
    path("delete_project/<int:pk>", ProjectDeleteView.as_view(), name="delete"),
    path("delete_tasks/<int:pk>", TasksDeleteView.as_view(), name="delete"),
    path("update_tasks/<int:pk>", TaskUpdateView.as_view(), name="update"),
    path("update_sprint/<int:pk>", SprintUpdateView.as_view(), name="update_sprint"),
    path("delete_sprint/<int:pk>", SprintDeleteView.as_view(), name="delete_sprint"),
    path("completed_tasks/", TasksCompleteListView.as_view()),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path("api/", include(router.urls)),
]
