from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Person, Testing, Trying, Answer, Question


class QuestionListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = ('text',)


class QuestionDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = ('text', 'correct_answer')


class QuestionCreateOrUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = ('text', 'correct_answer', 'test')


class TestingListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Testing
		fields = ('title',)

	def update(self, instance, validated_data):
		validated_data['slug'] = validated_data.get('title').strip().replace(' ', '-').lower()
		return super().update(instance, validated_data)


class TestingDetailSerializer(serializers.ModelSerializer):
	questions = QuestionListSerializer(many=True)

	class Meta:
		model = Testing
		fields = ('title', 'questions')


class TestingCreateSerializer(serializers.ModelSerializer):
	"""For create Test instance with slug field"""

	class Meta:
		model = Testing
		fields = ('title',)

	def create(self, validated_data):
		validated_data.setdefault('slug', validated_data.get('title').strip().replace(' ', '-'))
		return super().create(validated_data)


class AnswerDetailSerializer(serializers.ModelSerializer):
	question = QuestionDetailSerializer()

	class Meta:
		model = Answer
		fields = ('question', 'answer')


class AnswerListSerializer(serializers.ModelSerializer):
	question = QuestionListSerializer()

	class Meta:
		model = Answer
		fields = ('question', 'answer')


class AnswerUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ('answer', )


class AnswerCreateSerializer(serializers.ModelSerializer):
	# trying = TryingIDSerializer()
	# question = QuestionIDSerializer()

	class Meta:
		model = Answer
		fields = ('trying', 'question', 'answer', )

	def validate(self, attrs):
		if not attrs.get('question'):
			raise ValidationError('Question not found')
		if not attrs.get('trying'):
			raise ValidationError('Trying not found')
		if attrs.get('question').test != attrs.get('trying').test:
			raise ValidationError('Question is not from Test')
		return attrs


class PersonListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'username')


class PersonUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'username', 'age', 'sex', '_password')


class PersonCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'username', 'age', 'sex', 'password')
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def create(self, validated_data):
		person = Person.objects.create_user(**validated_data)
		return person


class TryingListSerializer(serializers.ModelSerializer):
	test = TestingListSerializer()

	class Meta:
		model = Trying
		fields = ('test', 'submit_time')


class TryingDetailSerializer(serializers.ModelSerializer):
	test = TestingListSerializer(read_only=True)
	answers = AnswerListSerializer(many=True, read_only=True)

	class Meta:
		model = Trying
		fields = ('test', 'submit_time', 'answers')


class TryingDetailRevealAnswersSerializer(TryingDetailSerializer):
	answers = AnswerDetailSerializer(many=True, read_only=True)


class TryingCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Trying
		fields = ('test', )


class PersonDetailSerializer(serializers.ModelSerializer):
	tryings = TryingListSerializer(many=True, read_only=True)

	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'username', 'age', 'sex', 'tryings')