from rest_framework import serializers
from .models import User, Course, Video, Article, Interaction, Recommendation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data.get('password')
        )
        return user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'user', 'content_type', 'content_id', 'rating', 'comment', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'content_type', 'content_id', 'score']
        read_only_fields = ['id', 'user', 'score']