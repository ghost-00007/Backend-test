from django.urls import path
from .views import UserLogin, PasswordResetView, UserCreateView, UserEmailConfirmation

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('reset_password/', PasswordResetView.as_view(), name='password-reset'),
    path('create_user/', UserCreateView.as_view(), name='create-user'),
    path('create_user/<int:pk>/', UserCreateView.as_view(), name='get-user-by-id'),
    path('verify_email/', UserEmailConfirmation.as_view(), name='verify-email'),

    # path('api/token/', include('rest_framework_simplejwt.urls')),
]