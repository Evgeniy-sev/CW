from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Tasks, Projects, Sprint, Status
from django.forms.widgets import SelectDateWidget


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["surname", "name", "patronymic", "birth_date", "email", "number"]


class CreatTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "user"]


class CreatProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ["title", "description", "owner"]


class CreatSprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ["title", "description", "project"]


class CreatStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["title", "parent"]


class UpdateSprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = [
            "is_active",
            "title",
            "project",
            "description",
            "start_date",
            "end_date",
            "completed",
        ]
        widgets = {
            "start_date": SelectDateWidget(),
            "end_date": SelectDateWidget(),
        }


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "sprint", "status", "executor", "completed"]


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ["title", "description", "completed"]
