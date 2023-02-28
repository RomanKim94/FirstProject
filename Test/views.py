from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonListSerializer
	lookup_field = 'slug'

	def get_serializer_class(self, *args, **kwargs):
		if self.action == 'retrieve':
			return PersonDetailSerializer
		# elif self.action == 'list':
		return super().get_serializer_class()

	def get_queryset(self):
		qs = super().get_queryset()
		if self.action == 'retrieve':
			return qs.prefetch_related('tryings')
		# elif self.action == 'list':
		return qs


class TestViewSet(viewsets.ModelViewSet):
	queryset = Testing.objects.all()
	serializer_class = TestingListSerializer
	lookup_field = 'slug'

	def get_serializer_class(self):
		if self.action != 'list':
			return TestingDetailSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		qs = super().get_queryset()
		if self.action != 'list':
			return qs.prefetch_related('questions')
		return qs


class TryingViewSet(viewsets.ModelViewSet):
	queryset = Trying.objects.all().select_related('test')
	serializer_class = TryingListSerializer

	def get_serializer_class(self):
		if self.action != 'list':
			return TryingDetailSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		qs = super().get_queryset()
		if self.action != 'list':
			return qs.prefetch_related('test', 'answers')
		return qs


class AnswerViewSet(viewsets.ModelViewSet):
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer
