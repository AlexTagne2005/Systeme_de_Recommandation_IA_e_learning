from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from core.models import User, Course, Video, Article, Interaction
import random

class Command(BaseCommand):
    help = 'Populate the database with initial test data'

    def handle(self, *args, **kwargs):
        # Créer des utilisateurs
        users = []
        for i in range(5):
            username = f"user{i+1}"
            email = f"user{i+1}@example.com"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'password': 'password123'}
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            users.append(user)

        # Créer des contenus
        courses = [
            {'title': 'Python for Beginners', 'description': 'Learn Python programming basics', 'category': 'Programming'},
            {'title': 'Data Science with Python', 'description': 'Explore data analysis and ML', 'category': 'Data Science'},
        ]
        videos = [
            {'title': 'Django Tutorial', 'description': 'Build web apps with Django', 'category': 'Web Development'},
            {'title': 'Machine Learning Intro', 'description': 'Introduction to ML concepts', 'category': 'Data Science'},
        ]
        articles = [
            {'title': 'How to Learn Python', 'description': 'Guide to mastering Python', 'category': 'Programming'},
            {'title': 'AI Trends 2025', 'description': 'Latest trends in AI', 'category': 'Artificial Intelligence'},
        ]

        for course_data in courses:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={'description': course_data['description'], 'category': course_data['category']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))

        for video_data in videos:
            video, created = Video.objects.get_or_create(
                title=video_data['title'],
                defaults={'description': video_data['description'], 'category': video_data['category']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created video: {video.title}'))

        for article_data in articles:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={'description': article_data['description'], 'category': article_data['category']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created article: {article.title}'))

        # Créer des interactions
        content_types = {
            'course': ContentType.objects.get_for_model(Course),
            'video': ContentType.objects.get_for_model(Video),
            'article': ContentType.objects.get_for_model(Article),
        }
        contents = list(Course.objects.all()) + list(Video.objects.all()) + list(Article.objects.all())
        for user in users:
            for content in random.sample(contents, k=min(3, len(contents))):
                content_type = content_types[content.__class__.__name__.lower()]
                Interaction.objects.get_or_create(
                    user=user,
                    content_type=content_type,
                    content_id=content.id,
                    defaults={'rating': random.randint(1, 5), 'comment': f'Comment for {content.title}'}
                )
                self.stdout.write(self.style.SUCCESS(f'Created interaction for {user.username} on {content.title}'))