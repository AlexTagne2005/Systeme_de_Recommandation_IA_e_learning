from django.urls import path
from . import views

urlpatterns = [
    # Template-based views
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # API views
    path('api/register/', views.APIRegisterView.as_view(), name='api-register'),
    path('api/login/', views.APILoginView.as_view(), name='api-login'),
    path('api/profile/', views.APIProfileView.as_view(), name='api-profile'),
    path('api/contents/', views.ContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='content-list'),
    path('api/contents/<int:pk>/', views.ContentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='content-detail'),
    path('api/contents/search/', views.SearchContentView.as_view(), name='search-content'),
    path('api/interactions/', views.InteractionViewSet.as_view({'get': 'list', 'post': 'create'}), name='interaction-list'),
    path('api/interactions/<int:pk>/', views.InteractionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='interaction-detail'),
    path('api/recommendations/', views.RecommendationViewSet.as_view({'get': 'list'}), name='recommendation-list'),
    path('api/recommendations/generate/', views.GenerateRecommendationView.as_view(), name='generate-recommendation'),
    path('api/admin/contents/', views.AdminContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-content-list'),
    path('api/admin/contents/<int:pk>/', views.AdminContentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-content-detail'),
    path('api/admin/users/', views.AdminUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-user-list'),
    path('api/admin/users/<int:pk>/', views.AdminUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-user-detail'),
]