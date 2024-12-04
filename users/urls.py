from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import RegisterView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='catalog:index'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
