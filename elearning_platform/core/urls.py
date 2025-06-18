from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contents', views.ContentViewSet, basename='content')
router.register(r'interactions', views.InteractionViewSet, basename='interaction')
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')
router.register(r'admin/contents', views.AdminContentViewSet, basename='admin-content')
router.register(r'admin/users', views.AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('contents/search/', views.SearchContentView.as_view(), name='search-content'),
    path('recommendations/generate/', views.GenerateRecommendationView.as_view(), name='generate-recommendation'),
]