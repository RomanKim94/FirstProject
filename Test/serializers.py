from rest_framework import serializers
from .models import Person, Testing, Trying, Answer, Question


class QuestionListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = ('text', )


class QuestionDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = ('text', 'correct_answer')


class TestingListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Testing
		fields = ('title', 'slug')


class TestingDetailSerializer(serializers.ModelSerializer):
	questions = QuestionListSerializer(many=True)

	class Meta:
		model = Testing
		fields = ('title', 'slug', 'questions')


class AnswerSerializer(serializers.ModelSerializer):
	question = QuestionListSerializer(read_only=True)

	class Meta:
		model = Answer
		fields = ('question', 'answer')


class TryingListSerializer(serializers.ModelSerializer):
	test = TestingListSerializer(read_only=True)

	class Meta:
		model = Trying
		fields = ('test', 'id', 'submit_time')


class TryingDetailSerializer(serializers.ModelSerializer):
	test = TestingListSerializer(read_only=True)
	answers = AnswerSerializer(many=True, read_only=True)

	class Meta:
		model = Trying
		fields = ('test', 'submit_time', 'answers')


class PersonDetailSerializer(serializers.ModelSerializer):
	tryings = TryingListSerializer(many=True, read_only=True)

	class Meta:
		model = Person
		fields = ('full_name', 'age', 'sex', 'tryings')

	def validate(self, attrs):
		if attrs.get('slug') is None:
			attrs['slug'] = attrs['full_name'].replace(' ', '-').lower() + '-' + str(attrs['age'])
		return attrs


class PersonListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Person
		fields = ('full_name', 'slug', 'age', 'sex')
