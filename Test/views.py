from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Person, Answer, Trying, Testing

from .serializers import (
	PersonListSerializer, PersonDetailSerializer,
	TryingDetailSerializer, TryingListSerializer,
	AnswerSerializer,
	TestingListSerializer, TestingDetailSerializer
)


class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonListSerializer
	lookup_field = 'slug'

	def get_serializer_class(self, *args, **kwargs):
		if self.action == 'retrieve':
			return PersonDetailSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		qs = super().get_queryset()
		if self.action == 'retrieve':
			return qs.prefetch_related('tryings')
		return qs

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data.get('slug') is None:
			serializer.validated_data['slug'] = serializer.validated_data['full_name'].replace(' ', '-').lower() + '-' + str(serializer.validated_data['age'])
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
