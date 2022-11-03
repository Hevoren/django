import datetime
from os.path import splitext
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.dispatch import Signal
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


class AdvUser(AbstractUser):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False, validators=[
        RegexValidator(
            regex='^[А-Яа-я -]*$',
            message='Имя пользователя должно состоять из кириллицы',
            code='invalid_username'
        ),
    ])
    surname = models.CharField(max_length=200, verbose_name='Фамилия', blank=False, validators=[
        RegexValidator(
            regex='^[А-Яа-я -]*$',
            message='Фамилия пользователя должно состоять из кириллицы',
            code='invalid_username'
        ),
    ])
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False, validators=[
        RegexValidator(
            regex='^[A-Za-z -]*$',
            message='Имя пользователя должно состоять только из латиницы',
            code='invalid_username'
        ),
    ])
    avatar = models.ImageField(models.ImageField(max_length=200, upload_to=get_timestamp_path, blank=False, null=True,
                                                 validators=[FileExtensionValidator(
                                                     allowed_extensions=['png', 'jpg', 'jpeg'])]))
    email = models.EmailField(max_length=200, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=200, verbose_name='Пароль', blank=False)

    USERNAME_FIELD = 'username'

    def delete(self, *args, **kwargs):
        for question in self.question_set.all():
            question.delete()
        for avatar in self.avatar_set.all():
            avatar.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)

    class Meta:
        ordering = ['name']


user_registrated = Signal()
