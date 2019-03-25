from rest_framework import serializers
from .models import Subject,Topic,Chapter,Question
from  general.fields import Base64ImageField

class SubjectSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model=Subject
        fields='__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields='__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chapter
        fields='__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'