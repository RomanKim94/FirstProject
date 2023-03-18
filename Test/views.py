from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Person, Answer, Trying, Testing, Question
from .permissions import (
	IsOwnerOrAdminOrCreateAnswerPermission,
	IsOwnerOrAdminOrCreatePersonPermission,
	IsOwnerOrAdminTryingPermission, IsAdminQuestionPermission
)


from .serializers import (
	PersonListSerializer, PersonDetailSerializer, PersonCreateSerializer,
	TryingDetailSerializer, TryingListSerializer, TryingCreateSerializer,
	AnswerListSerializer, AnswerCreateSerializer,
	TestingListSerializer, TestingDetailSerializer, TestingCreateSerializer,
	QuestionCreateOrUpdateSerializer, QuestionDetailSerializer, QuestionListSerializer, AnswerDetailSerializer,
	PersonUpdateSerializer, AnswerUpdateSerializer, TryingDetailRevealAnswersSerializer
)


class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonListSerializer
	lookup_field = 'username'
	permission_classes = [IsOwnerOrAdminOrCreatePersonPermission]

	def get_serializer_class(self, *args, **kwargs):
		if self.action in ['retrieve', 'destroy']:
			return PersonDetailSerializer
		elif self.action in ['update', 'partial_update']:
			return PersonUpdateSerializer
		elif self.action == 'create':
			return PersonCreateSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		if self.request.user and self.request.user.is_staff:
			qs = super().get_queryset()
		else:
			qs = super().get_queryset().filter(username=self.request.user.username)
		if self.action in ['retrieve', 'destroy']:
			return qs.prefetch_related('tryings')
		return qs

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(PersonDetailSerializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)


class TestViewSet(viewsets.ModelViewSet):
	queryset = Testing.objects.all()
	serializer_class = TestingListSerializer
	lookup_field = 'slug'

	def get_serializer_class(self):
		if self.action in ['retrieve', 'destroy']:
			return TestingDetailSerializer
		elif self.action == 'create':
			return TestingCreateSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		qs = super().get_queryset()
		if self.action in ['retrieve', 'destroy']:
			return qs.prefetch_related('questions')
		return qs


class TryingViewSet(viewsets.ModelViewSet):
	queryset = Trying.objects.all().select_related('test')
	serializer_class = TryingListSerializer
	permission_classes = [IsOwnerOrAdminTryingPermission]

	def perform_create(self, serializer):
		serializer.save(person=self.request.user, mark_percents=0.0, is_complete=False)

	def get_serializer_class(self):
		if self.action == 'retrieve':
			if self.get_object().is_complete:
				return TryingDetailRevealAnswersSerializer
			return TryingDetailSerializer
		if self.action in ['update', 'partial_update', 'destroy']:
			return TryingDetailSerializer
		elif self.action == 'create':
			return TryingCreateSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		show_for_all = False
		if show_for_all or self.request.user and self.request.user.is_staff:
			qs = super().get_queryset()
		else:
			qs = super().get_queryset().filter(person=self.request.user)
		# code above for Trying instance showed to owner only or to all
		if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
			return qs.select_related('test').prefetch_related('test__questions', 'answers')
		elif self.action == 'create':
			return qs.select_related('test')
		return qs


class AnswerViewSet(viewsets.ModelViewSet):
	queryset = Answer.objects.all()
	serializer_class = AnswerListSerializer
	permission_classes = [IsOwnerOrAdminOrCreateAnswerPermission]

	def get_serializer_class(self):
		if self.action in ['retrieve', 'destroy']:
			return AnswerDetailSerializer
		if self.action in ['update', 'partial_update']:
			return AnswerUpdateSerializer
		if self.action == 'create':
			return AnswerCreateSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		show_for_all = False
		if show_for_all or self.request.user and self.request.user.is_staff:
			qs = super().get_queryset()
		else:
			qs = super().get_queryset().filter(trying__person=self.request.user)
		if self.action in ['update', 'partial_update']:
			return qs
		if self.action == 'list':
			return qs.select_related('question')
		elif self.action in ['retrieve', 'create', 'destroy']:
			return qs.select_related('question', 'trying')
		return qs

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		trying = serializer.validated_data.get('trying')
		trying.mark_percents = int(sum([i.is_correct for i in trying.answers.all()])/len(trying.answers.all()) * 100)
		trying.is_complete = bool(len(trying.answers.all()) == len(trying.test.questions.all()))
		trying.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		correct_answer = serializer.validated_data.get('question').correct_answer.lower()
		answer = serializer.validated_data.get('answer').strip().lower()

		serializer.save(is_correct=bool(answer == correct_answer))


class QuestionViewSet(viewsets.ModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionListSerializer
	permission_classes = [IsAdminQuestionPermission]

	def get_serializer_class(self):
		if self.action in ['retrieve']:
			return QuestionDetailSerializer
		elif self.action in ['create', 'update', 'partial_update', 'destroy']:
			return QuestionCreateOrUpdateSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		qs = super().get_queryset()
		if self.action in ['retrieve', 'update', 'partial_update', 'create', 'destroy']:
			return qs.select_related('test')
		return qs
