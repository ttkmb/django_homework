from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, TemplateView, FormView
from config import settings
from users.forms import RegisterUserForm, LoginUserForm, UserProfileForm, UserPasswordChangeForm
from users.utils import send_email_for_verify, generate_random_password


class RegisterUserView(FormView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')
    form_class = RegisterUserForm

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        if not user.is_verified:
            send_email_for_verify(self.request, user)
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse('catalog:index')


class LogoutUserView(LogoutView):
    pass


class ProfileUserView(UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


class VerifyEmailView(View):
    template_name = 'users/verify.html'

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('catalog:index')
        else:
            return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        return user


class InvalidVerifyEmailView(TemplateView):
    template_name = 'users/invalid_verify.html'
    success_url = reverse_lazy('users:login')


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


def generate_password(request):
    new_password = generate_random_password()
    send_mail(
        subject='Новый пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse_lazy('users:password_generate_done'))