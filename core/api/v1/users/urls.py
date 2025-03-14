from django.urls import path
from core.api.v1.users.views import UserRegistrationView, UserDetailView, PhoneTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user-signup'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    path('login/', PhoneTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
