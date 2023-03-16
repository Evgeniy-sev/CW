from django.db import models
from django.utils import timezone
from tasks.managers import AnnotatedManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import logging
from .telegram import telegram_bot_sendtext


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile = Profile.objects.create(
            user=instance,
            email=instance.email,
            surname=instance.last_name,
            name=instance.first_name,
        )
    instance.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=256, unique=False, blank=True, null=True, verbose_name="Имя"
    )
    patronymic = models.CharField(
        max_length=256, unique=False, blank=True, null=True, verbose_name="Отчество"
    )
    surname = models.CharField(
        max_length=256, unique=False, blank=True, null=True, verbose_name="Фамилия"
    )
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    email = models.EmailField(
        max_length=256, blank=True, null=True, verbose_name="Email"
    )
    number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )

    def __str__(self):
        return "Profile for user {}".format(self.user.username)

    class Meta:
        verbose_name = "Профиль"


class Projects(models.Model):

    objects = AnnotatedManager()
    title = models.CharField(
        max_length=256, null=False, help_text="(Наименование проекта)"
    )
    description = models.TextField()

    owner = models.ForeignKey(
        User,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        help_text="(ID создателя)",
    )

    created_time = models.DateTimeField(
        auto_now_add=True, help_text="(Время создания проекта)"
    )
    completed = models.BooleanField(
        default=False, null=False, help_text="(Отметка о выполнении)"
    )
    completed_time = models.DateTimeField(
        default=None, blank=True, null=True, help_text="(Время завершения проекта)"
    )

    def save(self, *args, **kwargs) -> None:
        """Переопределение сохранения.
        ставится дата завершения задачи, если есть отметка о завершении.
        """
        if self.completed:
            self.completed_time = timezone.now()
            logger.info("Project ('%s') id=%s  is completed.", self.title, self.pk)
        else:
            self.completed_time = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Sprint(models.Model):

    objects = AnnotatedManager()
    title = models.CharField(
        max_length=256, null=False, help_text="(Наименование спринта)"
    )
    description = models.TextField()

    owner = models.ForeignKey(
        User,
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="(ID создателя)",
    )

    created_time = models.DateTimeField(
        auto_now_add=True, help_text="(Время создания спринта)"
    )
    completed = models.BooleanField(
        default=False, null=False, help_text="(Отметка о выполнении)"
    )
    completed_time = models.DateTimeField(
        default=None, blank=True, null=True, help_text="(Время завершения спринта)"
    )

    project = models.ForeignKey(
        Projects,
        default=None,
        on_delete=models.CASCADE,
        blank=True,
        help_text="(Проект)",
    )

    start_date = models.DateTimeField(
        auto_now_add=False, blank=True, null=True, help_text="(Время старта спринта)"
    )

    end_date = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
        help_text="(Время завершения спринта)",
    )
    is_active = models.BooleanField(
        default=False, null=False, help_text="(Спринт в работе)"
    )

    def save(self, *args, **kwargs) -> None:
        """Переопределение сохранения.
        ставится дата завершения задачи, если есть отметка о завершении.
        """
        if self.completed:
            self.completed_time = timezone.now()
            logger.info("Sprint ('%s') id=%s  is completed.", self.title, self.pk)
        else:
            self.completed_time = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(
        max_length=256, null=False, unique=True, help_text="(Статус задачи)"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.title


class Tasks(models.Model):

    objects = AnnotatedManager()
    title = models.CharField(
        max_length=256, null=False, help_text="(Наименование задачи)"
    )
    description = models.TextField(
        default="description of task", help_text="(Описание задачи)"
    )

    created_time = models.DateTimeField(
        auto_now_add=True, help_text="(Время создания задачи)"
    )
    completed = models.BooleanField(
        default=False, null=False, help_text="(Отметка о выполнении)"
    )
    completed_time = models.DateTimeField(
        default=None, blank=True, null=True, help_text="(Время завершения задачи)"
    )
    task_start_time = models.DateTimeField(
        default=None, blank=True, null=True, help_text="(Время начала решения задачи)"
    )
    user = models.ForeignKey(
        User,
        related_name="owner_tasks_set",
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="(ID создателя)",
    )
    executor = models.ForeignKey(
        User,
        related_name="executor_tasks_set",
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="(исполнитель)",
    )
    status = models.ForeignKey(
        Status,
        related_name="task_status",
        max_length=56,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="(Статус задачи)",
    )
    sprint = models.ForeignKey(
        Sprint,
        related_name="sprint_set",
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="(Спринт)",
    )

    def save(self, *args, **kwargs) -> None:
        """Переопределение сохранения.
        ставится дата завершения задачи, если есть отметка о завершении.
        """
        # self.executor = User.objects.get(username=self.user)
        if self.completed:
            self.completed_time = timezone.now()
            logger.info("Task ('%s') id=%s  is completed.", self.title, self.pk)
            self.status_id = Status.objects.get(title="completed").id
        else:
            self.completed_time = None

        if (str(self.status) == "in_work") & (not self.task_start_time):
            logger.info("Task ('%s') id=%s in work.", self.title, self.pk)
            self.task_start_time = timezone.now()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Tasks)
def update_task(sender, instance, **kwargs):
    executor = "None"
    if instance.executor:
        executor = str(User.objects.get(username=instance.executor))
    owner = str(instance.user)
    telegram_bot_sendtext(
        owner
        + " - автор, "
        + executor
        + " - исполнитель"
        + ', Ваша задача "'
        + instance.title
        + '" изменена.'
    )


@receiver(pre_save, sender=Tasks)
def update_task(sender, instance, **kwargs):
    if Tasks.objects.filter(id=instance.pk).count() > 0:
        send_field = str(
            Tasks.objects.select_related("executor").get(id=instance.pk).executor
        )
        ins_field = str(instance.executor)
        if send_field != ins_field:
            logger.info(
                "Task '%s' id=%s is updating, old executor is  %s, new - %s",
                str(instance.title),
                instance.pk,
                send_field,
                ins_field,
            )

        send_field = str(Tasks.objects.get(id=instance.pk).status)
        ins_field = str(instance.status)
        if send_field != ins_field:
            logger.info(
                "Task '%s' id=%s is updating, old status is '%s', new - '%s'",
                str(instance.title),
                instance.pk,
                send_field,
                ins_field,
            )


class User_Project(models.Model):

    objects = AnnotatedManager()

    owner = models.ForeignKey(
        User,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        help_text="(ID пользователя)",
    )
    owner_project = models.ForeignKey(
        Projects,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        help_text="(ID открытого проекта)",
    )

    def __str__(self):
        return self.owner
