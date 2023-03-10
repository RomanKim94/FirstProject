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


class Testing(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='SLUG')

	def __str__(self):
		return self.title


class Question(models.Model):
	text = models.TextField()
	correct_answer = models.CharField(max_length=255)
	test = models.ForeignKey('Testing', on_delete=models.CASCADE, related_name='questions')

	def __str__(self):
		return self.text


class Answer(models.Model):
	trying = models.ForeignKey('Trying', on_delete=models.CASCADE, related_name='answers')
	question = models.ForeignKey('Question', on_delete=models.CASCADE)
	answer = models.CharField(max_length=255, null=True)

	def __str__(self):
		return self.answer
