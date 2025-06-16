from rest_framework import serializers
from .models import User, Admin, Content, Course, Video, Article, Interaction, Recommendation
from django.contrib.contenttypes.models import ContentType

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['id', 'user']

class ContentSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'category', 'created_at', 'content_type']
        read_only_fields = ['id', 'created_at']

    def get_content_type(self, obj):
        return obj.__class__.__name__.lower()

class CourseSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        model = Course

class VideoSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        model = Video

class ArticleSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        model = Article

class InteractionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content_type = serializers.CharField(source='content_type.model', read_only=True)
    content_id = serializers.IntegerField()

    class Meta:
        model = Interaction
        fields = ['id', 'user', 'content_type', 'content_id', 'rating', 'comment', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

class RecommendationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content_type = serializers.CharField(source='content_type.model', read_only=True)
    content_id = serializers.IntegerField()

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'content_type', 'content_id', 'score']
        read_only_fields = ['id', 'user']