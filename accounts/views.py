import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import UserForm
from accounts.models import ShippingAddress
import secrets

# On récupère la fonction get user model
User = get_user_model()


# Create your views here.

def create_auth_key(user):
    auth_key = secrets.token_urlsafe(16)  # Génère une clé aléatoire sécurisée
    user.auth_key = auth_key
    user.save()


def signup(request):
    # Si la requête est de type post, on récupère les données de notre formulaire dans des variables
    # On utilise le name cité dans les inputs
    # Si la requête n'est pas de type post on renvoie vers notre formulaire
    if request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST["firstname"]
        email = request.POST["email"]
        password = request.POST["password"]
        # On créer un utilisateur à partir de User en récupérant les données envoyées
        User = get_user_model()
        user = User.objects.create_user(email=email,
                                        password=password,
                                        first_name=first_name)
        # On connecte notre utilisateur crée avec la fonction login ci-dessous qui prend en paramètre la requête et le
        # nom d'utilisateur
        login(request, user)

        # Générer une clé d'authentification et l'associer à l'utilisateur
        create_auth_key(user)

        return redirect('index')

    return render(request, 'accounts/signup.html')


def login_user(request):
    if request.method == 'POST':
        # Connecter l'utilisateur
        username = request.POST.get("username")
        password = request.POST.get("password")

        # On utilise la fonction authenticate pour vérifier si l'utillisateur est présent en base de donnée
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html')


def logout_user(request):
    # Django connaît l'utilisateur connecter avec la requête et peut donc le déconnecter automatiquement
    logout(request)
    return redirect('index')


@login_required()
def profile(request):
    if request.method == 'POST':
        is_valid = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        if is_valid:
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()
        else:
            # On importe le module message
            messages.add_message(request, messages.ERROR, "Le mot de passe n'est pas valide")

        return redirect('accounts:profile')

    # transforme un model en dictionnaire
    # form = UserForm(initial=model_to_dict(request.user, exclude='password'))

    form = UserForm(instance=request.user)
    addresses = request.user.addresses.all()
    # qrcode = get_object_or_404(Order, user=request.user)
    # qrcode = order.qr_code_thumbnail

    return render(request, "accounts/profile.html", context={"form": form, "addresses": addresses})


@login_required
def delete_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    address.delete()
    return redirect('accounts:profile')
