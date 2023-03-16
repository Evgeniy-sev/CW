from django.db.models import Manager

from django.db.models import QuerySet


class AnnotatedManager(Manager):
    def get_queryset(self) -> QuerySet:
        """Переопределение метода get_queryset.

        Метод будет вызываться при каждой выборке из таблицы.
        """
        qs = super().get_queryset()
        # заполучить исходный QuerySet, как будто его еще не переопределили.

        return qs
