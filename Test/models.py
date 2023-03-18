from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models

from Test.managers import CustomUserManager


class Person(AbstractUser, PermissionsMixin):
    SEX = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    age = models.IntegerField()
    sex = models.CharField(max_length=1, blank=False, choices=SEX)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'


class Trying(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='tryings')
    test = models.ForeignKey('Testing', on_delete=models.DO_NOTHING)
    submit_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    mark_percents = models.FloatField()
    is_complete = models.BooleanField()

    objects = models.Manager()

    class Meta:
        verbose_name = 'Прохождение'
        verbose_name_plural = 'Прохождения'

    def __str__(self):
        return (
            f'Время начала: {self.submit_time.strftime("%H:%M %d.%m.%Y")}. '
            f'Время последнего обновления: {self.update_time.strftime("%H:%M %d.%m.%Y")}'
        )


class Testing(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='SLUG', blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    test = models.ForeignKey('Testing', on_delete=models.CASCADE, related_name='questions')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    trying = models.ForeignKey('Trying', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    answer_time = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(blank=True)

    objects = models.Manager()

    class Meta:
        unique_together = (('trying', 'question'), )
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.answer
