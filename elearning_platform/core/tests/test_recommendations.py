import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from core.models import User, Course, Video, Article, Interaction, Recommendation
from core.recommendation_engine import save_recommendations
from django.utils import timezone

@pytest.fixture
def user():
    """Crée un utilisateur de test."""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="test123"
    )

@pytest.fixture
def another_user():
    """Crée un deuxième utilisateur pour simuler des interactions multiples."""
    return User.objects.create_user(
        username="anotheruser", email="another@example.com", password="test123"
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

@pytest.fixture
def interactions(user, another_user, contents):
    """Crée des interactions avec des ratings pour deux utilisateurs."""
    course, video, article = contents
    interactions = [
        Interaction(
            user=user,
            content_type=ContentType.objects.get_for_model(Course),
            content_id=course.id,
            rating=4.5,
            timestamp=timezone.now(),
        ),
        Interaction(
            user=user,
            content_type=ContentType.objects.get_for_model(Video),
            content_id=video.id,
            rating=3.0,
            timestamp=timezone.now(),
        ),
        Interaction(
            user=another_user,
            content_type=ContentType.objects.get_for_model(Course),
            content_id=course.id,
            rating=5.0,
            timestamp=timezone.now(),
        ),
        Interaction(
            user=another_user,
            content_type=ContentType.objects.get_for_model(Article),
            content_id=article.id,
            rating=4.0,
            timestamp=timezone.now(),
        ),
    ]
    for interaction in interactions:
        interaction.save()
    return interactions

@pytest.mark.django_db
def test_save_recommendations_success(user, contents, interactions):
    """Teste que save_recommendations génère et sauvegarde des recommandations."""
    course, video, article = contents
    
    # Générer des recommandations
    save_recommendations(user.id)
    
    # Vérifier que des recommandations existent pour l'utilisateur
    recommendations = Recommendation.objects.filter(user=user)
    assert recommendations.exists(), "Aucune recommandation n'a été générée"
    
    # Vérifier que les scores sont positifs
    for rec in recommendations:
        assert rec.score > 0, f"Le score de la recommandation {rec.id} est négatif ou nul"
    
    # Vérifier que les recommandations incluent des contenus non notés par l'utilisateur
    recommended_content_ids = set(rec.content_id for rec in recommendations)
    assert article.id in recommended_content_ids, "L'article non noté n'est pas recommandé"

@pytest.mark.django_db
def test_save_recommendations_no_interactions(user):
    """Teste save_recommendations avec aucune interaction."""
    save_recommendations(user.id)
    
    # Vérifier qu'aucune recommandation n'est générée
    recommendations = Recommendation.objects.filter(user=user)
    assert not recommendations.exists(), "Des recommandations ont été générées sans interactions"

@pytest.mark.django_db
def test_generate_recommendations_endpoint_success(user, contents, interactions):
    """Teste l'endpoint /api/recommendations/generate/."""
    # Créer un client API et authentifier l'utilisateur
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    # Appeler l'endpoint
    response = client.post(reverse("generate-recommendation"))
    
    # Vérifier la réponse
    assert response.status_code == 200, f"Échec de l'endpoint: {response.data}"
    
    # Vérifier que les recommandations sont sauvegardées
    recommendations = Recommendation.objects.filter(user=user)
    assert recommendations.exists(), "Aucune recommandation sauvegardée"
    
    # Vérifier que les données retournées incluent des scores positifs
    for rec in response.data:
        assert rec["score"] > 0, f"Le score de la recommandation {rec['id']} est négatif ou nul"

@pytest.mark.django_db
def test_generate_recommendations_endpoint_unauthenticated(contents):
    """Teste l'endpoint sans authentification."""
    client = APIClient()
    response = client.post(reverse("generate-recommendation"))
    
    # Vérifier que l'accès est refusé
    assert response.status_code == 401, "L'endpoint n'a pas rejeté une requête non authentifiée"

@pytest.mark.django_db
def test_generate_recommendation_url_exists():
    """Teste que l'URL generate-recommendation est correctement définie."""
    try:
        url = reverse("generate-recommendation")
        assert url == "/api/recommendations/generate/", "L'URL générée ne correspond pas au chemin attendu"
    except NoReverseMatch:
        pytest.fail("L'URL 'generate-recommendation' n'est pas définie dans urls.py")