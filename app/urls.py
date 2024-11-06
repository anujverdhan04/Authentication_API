from django.urls import path
from .views import SignUpView, LoginView, VerifyEmailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]
