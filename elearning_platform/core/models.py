from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def add_content(self, title, description, category, content_type):
        content_classes = {
            'course': Course,
            'video': Video,
            'article': Article
        }
        content_class = content_classes.get(content_type)
        if content_class:
            return content_class.objects.create(
                title=title,
                description=description,
                category=category,
                created_at=timezone.now()
            )
        raise ValueError("Invalid content type")

    def update_content(self, content_id, title=None, description=None, category=None):
        content = Content.objects.get(id=content_id)
        if title:
            content.title = title
        if description:
            content.description = description
        if category:
            content.category = category
        content.save()

    def delete_content(self, content_id):
        content = Content.objects.get(id=content_id)
        content.delete()

    def manage_users(self, user_id, action):
        user = User.objects.get(id=user_id)
        if action == 'delete':
            user.delete()
        # Add other user management actions as needed

class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def get_details(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at
        }

class Course(Content):
    pass

class Video(Content):
    pass

class Article(Content):
    pass

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')
    rating = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save_interaction(self):
        self.save()

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')
    score = models.FloatField()

    @classmethod
    def generate_recommendations(cls, user_id):
        # Placeholder for recommendation logic (to be implemented with Scikit-learn)
        pass

    @classmethod
    def get_recommendations(cls, user_id):
        return cls.objects.filter(user_id=user_id).order_by('-score')