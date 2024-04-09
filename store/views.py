from os import environ
from pprint import pprint

import environ
import stripe
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from JeuxOlympiques import settings
from accounts.models import CustomUser, ShippingAddress
from store.forms import OrderForm
# Permet de récupérer les produits dans la base de données
from store.models import Ticket, Cart, Order

stripe.api_key = settings.STRIPE_API_KEY
env = environ.Env()

environ.Env.read_env()


# Create your views here.
# On passe en paramètre la requête de l'utilisateur pour récupérer une page web
# On va ensuite retourner des informations pour retourner un fichier html
def index(request):
    # Manager qui me permet de récupérer les tickets
    tickets = Ticket.objects.all()
    # On prend en premier paramètre la requête puis on retourne notre ficbier html
    # Context = clé/valeur
    return render(request, 'tickets/index.html', context={'tickets': tickets})


def ticket_detail(request, slug):
    # On importe la fonction get_object_or_404/ On peut lui donner un modèle et si rien n'est affiché on aura une erreur
    ticket = get_object_or_404(Ticket, slug=slug)
    # On a une variable ticket que l'on passe à notre dictionnaire à la clé ticket.
    # On peut ensuite utiliser cette clé dans notre fichier html
    return render(request, 'tickets/ticket_detail.html', context={'ticket': ticket})


def add_to_cart(request, slug):
    # On récupère notre utilisateur que l'on stock dans la variable user
    # user = instance de custom user
    user: CustomUser = request.user
    user.add_to_cart(slug=slug)
    # On redirige vers la page du produit
    return redirect(reverse('store:ticket', kwargs={'slug': slug}))


@login_required(login_url='accounts:login')
def cart(request):
    """if request.user.is_anonymous:
        return redirect('index')"""
    # Récupérer toutes les commandes non ordonnées de l'utilisateur connecté
    orders = Order.objects.filter(user=request.user, ordered=False)

    # Vérifier si le panier est vide
    if not orders.exists():
        return redirect("index")

    # Créer un formulaire pour afficher les articles du panier
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)

    # Retourner le template avec les articles du panier
    return render(request, 'tickets/cart.html', context={'forms': formset})


"""orders = Order.objects.filter(user=request.user)
    if orders.count() == 0:
        return redirect("index")
    # Un récupère la requête de l'utilisateur que l'on ajoute au parmètre user sur le modèle Cart,
    # On créer une (class) orderformset, à partir de modelformsetfactory
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)

    # On retourne le template puis on récupère tout les éléments du panier
    return render(request, 'tickets/cart.html', context={'forms': formset})"""


def update_quantitites(request):
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    # On récupère le formulaire, si il est valide on le sauvegarde
    formset = OrderFormSet(request.POST, queryset=Order.objects.filter(user=request.user))
    if formset.is_valid():
        formset.save()

    return redirect('store:cart')


def create_checkout_session(request):
    cart = get_object_or_404(Cart, user=request.user)

    # On récupère le prix et la quantité que l'on ajoute à notre session de payment avec line_items
    line_items = [{"price": order.ticket.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    session = stripe.checkout.Session.create(
        locale='fr',
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        customer_email=request.user.email,
        shipping_address_collection={"allowed_countries": ["FR", "US", "CA"]},
        success_url=request.build_absolute_uri(reverse('store:checkout-success')),
        cancel_url='http://127.0.0.1.8000',
    )
    # Code 303 est le code de redirection
    return redirect(session.url, code=303)


def checkout_success(request):
    return render(request, 'tickets/success.html')


def delete_cart(request):
    # On vérifie que le panier puis on l'assigne dans la variable cart
    if cart := request.user.cart:
        # On utilise la méthode delet créer dans le modèle, la logique du modèle sera appliqué
        cart.delete()

    return redirect('index')


@csrf_exempt
# Authentifie les informations envoyés par stipe
def stripe_webhook(request):
    # On récupère le corps de la requête que l'on retourne avec un print et un status 200
    payload = request.body
    # Clé obtenu après exécution de la commande stripe listen --forward-to 127.0.0.1:localhost/stripe-webhook/
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = env('ENDPOINT_SECRET')
    event = None
    # On construit un évènement stripe avec try puis on renvoie un status
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Payload invalide
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Signature invalide
        return HttpResponse(status=400)

    # On vérifie que le client est authentifié et que le paiement est accepté
    # Si l'évènement type de notre dictionnaire est égale à checkout.session.completed on retourne la fonction
    if event['type'] == 'checkout.session.completed':
        data = event['data']['object']
        try:
            user = get_object_or_404(CustomUser, email=data['customer_details']['email'])
        except KeyError:
            return HttpResponse("Invalid email", status=404)

        complete_order(data=data, user=user)
        save_shipping_adress(data=data, user=user)
        return HttpResponse(status=200)

    # Signature correcte
    return HttpResponse(status=200)


def complete_order(data, user):
    # pprint(data)
    user.stripe_id = data['payment_intent']
    user.cart.delete()
    user.save()
    # Effacer le contenu du panier après la commande
    return HttpResponse(status=200)


def save_shipping_adress(data, user):
    """
    "shipping_details": {
        "address": {
            "city": "Paris",
            "country": "FR",
            "line1": "1 Rue de Tombouctou",
            "line2": null,
            "postal_code": "75018",
            "state": ""
        },
        "name": "Tom"
    },
    """
    try:
        address = data['shipping_details']['address']
        name = data['shipping_details']['name']
        city = address['city']
        country = address['country']
        line1 = address['line1']
        line2 = address['line2']
        zip_code = address['postal_code']
    except KeyError:
        return HttpResponse(status=400)

    ShippingAddress.objects.get_or_create(user=user,
                                          name=name,
                                          city=city,
                                          country=country.lower(),
                                          address_1=line1,
                                          address_2=line2 or "",
                                          zip_code=zip_code)

    return HttpResponse(status=200)
