from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(
        'users/verify.html',
        context=context,
    )
    email = EmailMessage(
        'Verify email',
        message,
        to=[user.email],
    )
    email.send()


def generate_random_password():
    password = get_random_string(15)
    try:
        validate_password(password, password_validators=get_default_password_validators())
        return password
    except ValidationError as e:
        return e