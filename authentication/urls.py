from django.urls import path
from authentication.views import RegisterView, LoginView, ProfileView, ProfileUpdateView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
]