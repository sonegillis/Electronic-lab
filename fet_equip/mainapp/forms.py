from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    
    def confirm_login_allowed(self, user):
        if not user.is_active and not user.is_validated:
            raise ValidationError("Error")