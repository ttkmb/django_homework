from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from users.views import RegisterUserView, LoginUserView, LogoutUserView, ProfileUserView, VerifyEmailView, \
    UserPasswordChangeView, generate_password

app_name = 'users'

urlpatterns = [
    path('', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('verify/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/generate/', generate_password, name='password_generate'),
    path('password_reset/generate/done/', TemplateView.as_view(template_name='users/password_generate_done.html'),
         name='password_generate_done'),
]
