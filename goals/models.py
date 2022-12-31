from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    def __str__(self):
        return self.title


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет', choices=Priority.choices, default=Priority.medium)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='goals', on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    due_date = models.DateField(verbose_name='Дата выполнения', null=True)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', related_name='goals', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)
    text = models.TextField(verbose_name='Текст')
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.PROTECT)


# class Question(models.Model):
#     text = models.TextField()
#     # ...
#
# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     # ...
#
#     class Meta:
#         order_with_respect_to = 'question'