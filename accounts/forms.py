from django import forms

from accounts.models import CustomUser


class UserForm(forms.ModelForm):
    # password input pour cacher notre mot de passe lors de la saisie
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block w-full ring-1 ring-UIElementBorderAndFocusRings hover:border-HoveredUIElementBorder shadow-sm py-3 px-4 border-UIElementBorderAndFocusRings rounded-md'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full ring-1 ring-UIElementBorderAndFocusRings hover:border-HoveredUIElementBorder shadow-sm py-3 px-4 border-UIElementBorderAndFocusRings rounded-md'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full ring-1 ring-UIElementBorderAndFocusRings hover:border-HoveredUIElementBorder shadow-sm py-3 px-4 border-UIElementBorderAndFocusRings rounded-md'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'block w-full ring-1 ring-UIElementBorderAndFocusRings hover:border-HoveredUIElementBorder shadow-sm py-3 px-4 border-UIElementBorderAndFocusRings rounded-md'}))


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
