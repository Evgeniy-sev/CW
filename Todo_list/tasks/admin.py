from django.contrib import admin
from .models import Tasks
from .models import Profile, Projects, Sprint


# admin.site.register(Profile)
# admin.site.register(Projects)
# admin.site.register(Sprint)


@admin.register(Tasks)
class TestAdmin(admin.ModelAdmin):
    def time_create(self, obj):
        return obj.created_time.strftime("%m-%d-%Y %H:%M:%S")

    def time_complete(self, obj):
        try:
            return obj.completed_time.strftime("%m-%d-%Y %H:%M:%S")
        except:
            return None

    def task_start(self, obj):
        try:
            return obj.task_start_time.strftime("%m-%d-%Y %H:%M:%S")
        except:
            return None

    time_create.admin_order_field = "timefield"
    time_create.short_description = "created_time"
    time_complete.admin_order_field = "timefield"
    time_complete.short_description = "completed_time"
    task_start.admin_order_field = "timefield"
    task_start.short_description = "time_task_start"

    readonly_fields = ("created_time", "completed_time", "task_start_time")
    list_display = (
        "title",
        "description",
        "status",
        "time_create",
        "time_complete",
        "task_start",
        "completed",
        "executor",
    )
    search_fields = ["title"]
    list_filter = (
        "completed",
        "task_start_time",
    )


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    def time_create(self, obj):
        return obj.created_time.strftime("%m-%d-%Y %H:%M:%S")

    def time_complete(self, obj):
        try:
            return obj.completed_time.strftime("%m-%d-%Y %H:%M:%S")
        except:
            return None

    def date_start(self, obj):
        try:
            return obj.start_date.strftime("%m-%d-%Y %H:%M:%S")
        except:
            return None

    def date_end(self, obj):
        try:
            return obj.end_date.strftime("%m-%d-%Y %H:%M:%S")
        except:
            return None

    time_create.admin_order_field = "timefield"
    time_create.short_description = "created_time"
    time_complete.admin_order_field = "timefield"
    time_complete.short_description = "completed_time"
    date_start.admin_order_field = "timefield"
    date_start.short_description = "start_time"
    date_end.admin_order_field = "timefield"
    date_end.short_description = "end_time"

    readonly_fields = ("created_time", "completed_time")
    list_display = (
        "title",
        "description",
        "project",
        "is_active",
        "time_create",
        "time_complete",
        "date_start",
        "date_end",
        "completed",
    )
    search_fields = ["title"]
    list_filter = (
        "completed",
        "is_active",
    )


@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    def time_create(self, obj):
        return obj.created_time.strftime("%m-%d-%Y %H:%M:%S")

    def time_complete(self, obj):
        try:
            return obj.completed_time.strftime("%m-%d-%Y %H:%M:%S")
        except:
            return None

    time_create.admin_order_field = "timefield"
    time_create.short_description = "created_time"
    time_complete.admin_order_field = "timefield"
    time_complete.short_description = "completed_time"

    readonly_fields = ("created_time", "completed_time")
    list_display = (
        "title",
        "description",
        "owner",
        "time_create",
        "time_complete",
        "completed",
    )
    search_fields = ["title"]
    list_filter = (
        "completed",
        "created_time",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def time_birth(self, obj):
        try:
            return obj.birth_date.strftime("%m-%d-%Y")
        except:
            return None

    time_birth.admin_order_field = "timefield"
    time_birth.short_description = "birth_time"

    list_display = (
        "user",
        "name",
        "patronymic",
        "surname",
        "time_birth",
        "email",
        "number",
    )
    search_fields = ("surname", "email")
    list_filter = (
        "surname",
        "user",
    )
