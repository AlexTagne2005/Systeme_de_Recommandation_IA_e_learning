import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from core.models import User, Course, Video, Article
from core.serializers import CourseSerializer, VideoSerializer, ArticleSerializer

@pytest.fixture
def user_data():
    """Données pour créer un utilisateur."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    }

@pytest.fixture
def user():
    """Crée un utilisateur de test."""
    return User.objects.create_user(
        username="existinguser", email="existing@example.com", password="test123"
    )

@pytest.fixture
def contents():
    """Crée des contenus de test (cours, vidéo, article)."""
    course = Course.objects.create(
        title="Python Course", description="Learn Python", category="Programming"
    )
    video = Video.objects.create(
        title="Django Tutorial", description="Django basics", category="Programming"
    )
    article = Article.objects.create(
        title="AI Introduction", description="AI concepts", category="Technology"
    )
    return course, video, article

@pytest.mark.django_db
def test_register_success(user_data):
    """Teste l'inscription d'un nouvel utilisateur."""
    client = APIClient()
    response = client.post(reverse("register"), user_data)
    
    assert response.status_code == 201, f"Échec de l'inscription: {response.data}"
    assert "token" in response.data, "Aucun token retourné"
    assert "user" in response.data, "Aucune donnée utilisateur retournée"
    assert User.objects.filter(username=user_data["username"]).exists(), "Utilisateur non créé"
    assert Token.objects.filter(user__username=user_data["username"]).exists(), "Token non créé"

@pytest.mark.django_db
def test_register_duplicate_username(user_data):
    """Teste l'inscription avec un nom d'utilisateur existant."""
    User.objects.create_user(**user_data)
    client = APIClient()
    response = client.post(reverse("register"), user_data)
    
    assert response.status_code == 400, "L'inscription avec un doublon n'a pas été rejetée"
    assert "username" in response.data, "Erreur de doublon non signalée"

@pytest.mark.django_db
def test_login_success(user):
    """Teste la connexion avec des identifiants valides."""
    client = APIClient()
    login_data = {"username": "existinguser", "password": "test123"}
    response = client.post(reverse("login"), login_data)
    
    assert response.status_code == 200, f"Échec de la connexion: {response.data}"
    assert "token" in response.data, "Aucun token retourné"
    assert "user" in response.data, "Aucune donnée utilisateur retournée"
    assert Token.objects.filter(user__username="existinguser").exists(), "Token non créé"

@pytest.mark.django_db
def test_login_invalid_credentials():
    """Teste la connexion avec des identifiants invalides."""
    client = APIClient()
    login_data = {"username": "nonexistent", "password": "wrong"}
    response = client.post(reverse("login"), login_data)
    
    assert response.status_code == 401, "La connexion invalide n'a pas été rejetée"
    assert "error" in response.data, "Message d'erreur non retourné"

@pytest.mark.django_db
def test_search_content_success(user, contents):
    """Teste la recherche de contenus avec authentification."""
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    # Recherche sans filtre
    response = client.get(reverse("search-content"))
    assert response.status_code == 200, f"Échec de la recherche: {response.data}"
    assert len(response.data) == 3, "Nombre incorrect de contenus retournés"
    
    # Recherche par type (course)
    response = client.get(reverse("search-content") + "?content_type=course")
    assert response.status_code == 200
    assert len(response.data) == 1, "Nombre incorrect de cours retournés"
    assert response.data[0]["title"] == "Python Course"
    
    # Recherche par requête
    response = client.get(reverse("search-content") + "?q=Python")
    assert response.status_code == 200
    assert len(response.data) == 2, "Nombre incorrect de résultats pour la requête"

@pytest.mark.django_db
def test_search_content_unauthenticated(contents):
    """Teste la recherche sans authentification."""
    client = APIClient()
    response = client.get(reverse("search-content"))
    
    assert response.status_code == 401, "La recherche non authentifiée n'a pas été rejetée"