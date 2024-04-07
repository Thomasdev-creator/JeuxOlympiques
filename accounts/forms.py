from django import forms

from accounts.models import CustomUser


class UserForm(forms.ModelForm):
    # password input pour cacher notre mot de passe lors de la saisie
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
