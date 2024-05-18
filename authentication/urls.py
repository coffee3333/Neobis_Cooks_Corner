from django.urls import path
from authentication.views import RegisterView, LoginView, ProfileView, ProfileUpdateView, LogoutView, TokenRefreshView, ProfilesList


urlpatterns = [
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profiles/', ProfilesList.as_view(), name='profiles'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
]