from django.shortcuts import render, redirect
from tasks.models import Tasks, Profile, Sprint, Projects, User_Project, Status
from django.contrib.auth.models import User
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    View,
    DeleteView,
    UpdateView,
)
from .forms import (
    UserRegisterForm,
    ProfileEditForm,
    CreatTaskForm,
    CreatProjectsForm,
    TaskUpdateForm,
    CreatSprintForm,
    UpdateSprintForm,
    CreatStatusForm,
    ProjectUpdateForm,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializers import ProjectSerializer
from rest_framework import viewsets
from django import forms
import logging
from .telegram import telegram_bot_sendtext
from django_filters.rest_framework import DjangoFilterBackend


logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")


def register(request):
    instance = request
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            User.profile.email = email
            messages.success(request, f"Создан аккаунт {username}!")
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f"Профиль изменен!")
            return redirect("/")
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, "profile.html", {"profile_form": profile_form})


def ProjectOpen(request, pk):  # запись связки юзер - открытый проект
    print(User.objects.get(username=request.user))
    print(Projects.objects.get(id=pk))

    w2 = User_Project.objects.filter(owner=User.objects.get(username=request.user))
    w2.delete()
    w2 = User_Project(
        owner=User.objects.get(username=request.user),
        owner_project=Projects.objects.get(id=pk),
    )
    w2.save()


class TasksListView(ListView):  # список незавершенных задач
    model = Tasks
    context_object_name = "tasks_"
    template_name = "uncompleted.html"

    def get_queryset(self):
        res = Tasks.objects.filter(
            completed=False, user=User.objects.get(username=self.request.user)
        ) | Tasks.objects.filter(
            completed=False, executor=User.objects.get(username=self.request.user)
        )

        return res


class TasksListAllView(ListView):  # список незавершенных задач
    model = Tasks
    context_object_name = "tasks_"
    template_name = "uncompleted.html"

    def get_queryset(self):
        return Tasks.objects.select_related("user", "executor", "sprint").filter(
            completed=False
        )


class TasksCompleteListView(ListView):  # список завершенных задач
    model = Tasks
    context_object_name = "tasks_compl_"
    template_name = "completed.html"

    def get_queryset(self):
        return Tasks.objects.filter(completed=True)


class TasksCreateView(CreateView):  # создание новой задачи
    form_class = CreatTaskForm
    template_name = "task_create.html"

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.user = User.objects.get(username=self.request.user)
        fields.executor = User.objects.get(username=self.request.user)
        logger.info("Task '%s'  is created", str(fields.title))
        # Наконец сохраняем в БД
        fields.save()
        return redirect("/uncompleted_tasks/")


class SprintCreateView(CreateView):  # создание новой задачи
    form_class = CreatSprintForm
    template_name = "sprint_create.html"

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.owner = User.objects.get(username=self.request.user)
        # Наконец сохраняем в БД
        fields.save()
        return redirect("/")


class ProjectsCreateView(CreateView):  # создание нового проекта
    form_class = CreatProjectsForm
    template_name = "projects_create.html"

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.owner = User.objects.get(username=self.request.user)
        # Наконец сохраняем в БД
        fields.save()
        return redirect("/")


class TaskUpdateView(UpdateView):  # редактирование задачи
    form_class = TaskUpdateForm
    template_name = "task_update.html"

    def form_valid(self, form):
        fields = form.save(commit=False)
        executor = form.cleaned_data.get("executor")
        stasus = form.cleaned_data.get("status")
        if str(executor) == "None":
            if not ((str(stasus) == "plan") | (str(stasus) == "None")):
                form.add_error(
                    "executor",
                    forms.ValidationError(
                        "Задача не может выполняться без исполнителя."
                    ),
                )
                return super(TaskUpdateView, self).form_invalid(form)
        w2 = Tasks.objects.filter(completed=False, executor=executor).count()
        if (
            (str(executor) != "None")
            & (w2 != 0)
            & (not ((str(stasus) == "plan") | (str(stasus) == "None")))
        ):
            if (w2 > 0) & (
                Tasks.objects.get(completed=False, executor=executor).pk != fields.pk
            ):
                logger.warning(
                    "Task id=%s is updating, executor %s is busy",
                    fields.pk,
                    str(executor),
                )
                form.add_error(
                    "executor",
                    forms.ValidationError(
                        "Данный исполнитель уже занят решением задачи"
                    ),
                )
                return super(TaskUpdateView, self).form_invalid(form)
        fields.executor = executor
        fields.status = stasus
        logger.info(
            "Task ('%s') id=%s  is update successfully.", fields.title, fields.pk
        )
        fields.save()
        return redirect("/uncompleted_tasks/")

    def get_queryset(self):
        return Tasks.objects.all()


class TasksDeleteView(DeleteView):  # удаление задачи
    model = Tasks
    template_name = "task_delete.html"
    success_url = "/uncompleted_tasks/"

    def get_queryset(self):
        return Tasks.objects.filter(completed=False)


class SprintsListView(ListView):  # список незавершенных спринтовч
    model = Sprint
    context_object_name = "sprint_"
    template_name = "uncompleted_sprint.html"

    def get_queryset(self):
        return Sprint.objects.filter(completed=False)


class SprintUpdateView(UpdateView):  # редактирование задачи
    form_class = UpdateSprintForm
    template_name = "sprint_update.html"

    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        # fields.owner = User.objects.get(username=self.request.user)
        # Наконец сохраняем в БД
        fields.save()
        return redirect("/uncompleted_sprints/")

    def get_queryset(self):
        return Sprint.objects.filter(completed=False)


class SprintDeleteView(DeleteView):  # удаление задачи
    model = Tasks
    template_name = "sprint_delete.html"
    success_url = "/uncompleted_sprints/"

    def get_queryset(self):
        return Sprint.objects.filter(completed=False)


class StatusCreateView(CreateView):  # создание нового статуса
    form_class = CreatStatusForm
    template_name = "status_create.html"

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.save()
        return redirect("/")


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class ProjectOpenView(UpdateView):
    form_class = ProjectUpdateForm
    template_name = "uncompleted_project.html"

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.save()
        return redirect("/")

    def get_queryset(self):
        return Projects.objects.all()


class ProjectDeleteView(DeleteView):  # удаление проекта
    model = Projects
    template_name = "Project_delete.html"
    success_url = "/"

    def get_queryset(self):
        return Projects.objects.all()
