from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est requis')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Un superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Un superutilisateur doit avoir is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def register(self):
        self.save()

    def login(self):
        # Géré par Django Authentication
        pass

    def update_profile(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def __str__(self):
        return self.username

class Admin(User):
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
        raise ValueError("Type de contenu invalide")

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
        # Ajouter d'autres actions de gestion si nécessaire

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
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')
    rating = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save_interaction(self):
        self.save()

class Recommendation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey('content_type', 'content_id')
    score = models.FloatField()

    @classmethod
    def generate_recommendations(cls, user_id):
        # Cette méthode est appelée depuis views.py pour éviter l'importation circulaire
        pass

    @classmethod
    def get_recommendations(cls, user_id):
        return cls.objects.filter(user_id=user_id).order_by('-score')