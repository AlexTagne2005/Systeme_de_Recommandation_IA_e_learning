from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('contents/', views.ContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='content-list'),
    path('contents/<int:pk>/', views.ContentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='content-detail'),
    path('contents/search/', views.SearchContentView.as_view(), name='search-content'),
    path('interactions/', views.InteractionViewSet.as_view({'get': 'list', 'post': 'create'}), name='interaction-list'),
    path('interactions/<int:pk>/', views.InteractionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='interaction-detail'),
    path('recommendations/', views.RecommendationViewSet.as_view({'get': 'list'}), name='recommendation-list'),
    path('recommendations/generate/', views.GenerateRecommendationView.as_view(), name='generate-recommendation'),
    path('admin/contents/', views.AdminContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-content-list'),
    path('admin/contents/<int:pk>/', views.AdminContentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-content-detail'),
    path('admin/users/', views.AdminUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='admin-user-list'),
    path('admin/users/<int:pk>/', views.AdminUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin-user-detail'),
]