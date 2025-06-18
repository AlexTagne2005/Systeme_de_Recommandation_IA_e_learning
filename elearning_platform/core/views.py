from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User, Admin, Course, Video, Article, Interaction, Recommendation
from .serializers import (
    UserSerializer, CourseSerializer, VideoSerializer,
    ArticleSerializer, InteractionSerializer, RecommendationSerializer
)
from .recommendation_engine import save_recommendations
import requests

class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        # Appeler l'API pour obtenir les recommandations
        token = Token.objects.get(user=request.user).key
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/recommendations/', headers=headers)
        recommendations = response.json() if response.status_code == 200 else []
        return render(request, 'home.html', {'recommendations': recommendations})

class SearchView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        query = request.GET.get('q', '')
        content_type = request.GET.get('content_type', '')
        # Appeler l'API pour effectuer la recherche
        token = Token.objects.get(user=request.user).key
        headers = {'Authorization': f'Token {token}'}
        params = {'q': query, 'content_type': content_type}
        response = requests.get('http://localhost:8000/api/contents/search/', headers=headers, params=params)
        results = response.json() if response.status_code == 200 else []
        return render(request, 'search.html', {'results': results})

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'profile.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        # Appeler l'API pour mettre à jour le profil
        token = Token.objects.get(user=request.user).key
        headers = {'Authorization': f'Token {token}'}
        data = {'email': request.POST.get('email')}
        response = requests.put('http://localhost:8000/api/profile/', headers=headers, data=data)
        if response.status_code == 200:
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Failed to update profile.')
        return render(request, 'profile.html')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials.')
        return render(request, 'login.html')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'register.html')

    def post(self, request):
        # Appeler l'API pour enregistrer un nouvel utilisateur
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }
        response = requests.post('http://localhost:8000/api/register/', data=data)
        if response.status_code == 201:
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('home')
        messages.error(request, 'Registration failed.')
        return render(request, 'register.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

# API Views (unchanged)
class APIRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APILoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class APIProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        if content_type == 'course':
            return Course.objects.all()
        elif content_type == 'video':
            return Video.objects.all()
        elif content_type == 'article':
            return Article.objects.all()
        return Course.objects.all()

    def get_serializer_class(self):
        content_type = self.request.query_params.get('content_type')
        if content_type == 'course':
            return CourseSerializer
        elif content_type == 'video':
            return VideoSerializer
        elif content_type == 'article':
            return ArticleSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

class SearchContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        content_type = request.query_params.get('content_type', '')
        
        results = []
        if content_type == 'course':
            queryset = Course.objects.all()
            if query:
                queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
            results = CourseSerializer(queryset, many=True).data
        elif content_type == 'video':
            queryset = Video.objects.all()
            if query:
                queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
            results = VideoSerializer(queryset, many=True).data
        elif content_type == 'article':
            queryset = Article.objects.all()
            if query:
                queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
            results = ArticleSerializer(queryset, many=True).data
        else:
            courses = Course.objects.all()
            videos = Video.objects.all()
            articles = Article.objects.all()
            if query:
                courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))
                videos = videos.filter(Q(title__icontains=query) | Q(description__icontains=query))
                articles = articles.filter(Q(title__icontains=query) | Q(description__icontains=query))
            results = (
                CourseSerializer(courses, many=True).data +
                VideoSerializer(videos, many=True).data +
                ArticleSerializer(articles, many=True).data
            )

        return Response(results)

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)

class GenerateRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        save_recommendations(request.user.id)
        recommendations = Recommendation.objects.filter(user_id=request.user.id)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminContentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        if content_type == 'course':
            return Course.objects.all()
        elif content_type == 'video':
            return Video.objects.all()
        elif content_type == 'article':
            return Article.objects.all()
        return Course.objects.all()

    def get_serializer_class(self):
        content_type = self.request.query_params.get('content_type')
        if content_type == 'course':
            return CourseSerializer
        elif content_type == 'video':
            return VideoSerializer
        elif content_type == 'article':
            return ArticleSerializer
        return CourseSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]