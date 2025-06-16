from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, ProfileView, ContentViewSet, SearchContentView,
    InteractionViewSet, RecommendationViewSet, AdminContentViewSet, AdminUserViewSet
)

router = DefaultRouter()
router.register(r'contents', ContentViewSet, basename='content')
router.register(r'interactions', InteractionViewSet, basename='interaction')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')
router.register(r'admin/contents', AdminContentViewSet, basename='admin-content')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('contents/search/', SearchContentView.as_view(), name='search-content'),
    path('', include(router.urls)),
]