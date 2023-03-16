from rest_framework import serializers
from .models import Projects, User


class ProjectSerializer(serializers.ModelSerializer):
    #    owner = User.objects.get(id=2).username

    class Meta:
        model = Projects
        fields = ("id", "title", "owner")
