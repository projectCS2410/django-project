from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('films/', views.home, name='films'),
    path('films/<slug:slug>/', views.film_detail, name='film_detail'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('api/comments/<int:pk>/', views.comment_api, name='comment_api'),
    path('signup/', views.signup, name='signup'),
    path(
        'login/',
        views.ForcedHomeLoginView.as_view(),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
