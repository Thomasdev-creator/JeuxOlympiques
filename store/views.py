import stripe
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from JeuxOlympiques import settings
# Permet de récupérer les produits dans la base de données
from store.models import Ticket, Cart, Order

stripe.api_key = settings.STRIPE_API_KEY


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
    user = request.user
    # On récupère le ticket
    ticket = get_object_or_404(Ticket, slug=slug)
    # On essaye de récupérer le panier de l'utilisateur, on le créer si il n'existe pas.
    # Deux éléments sont retouné à droite, d'ou les deux variables
    cart, _ = Cart.objects.get_or_create(user=user)
    # On récupérer les billet si il n'existe pas et on les stock dans order, et created sera égal à False,
    # Si les billets existent dans le panier, on créer le panier et created sera égale à True
    order, created = Order.objects.get_or_create(user=user, ordered=False, ticket=ticket)
    # Si l'élément n'existe pas
    if created:
        cart.orders.add(order)
        cart.save()
    # Si l'élément existe déjà, on le récupère et on incrémente de 1
    else:
        order.quantity += 1
        order.save()

    # On redirige vers la page du produit
    return redirect(reverse('ticket', kwargs={'slug': slug}))


def cart(request):
    # Un récupère la requête de l'utilisateur que l'on ajoute au parmètre user sur le modèle Cart,
    # Si il existe on le récupère puis on le stock dans la variable cart
    cart = get_object_or_404(Cart, user=request.user)

    # On retourne le template puis on récupère tout les éléments du panier
    return render(request, 'tickets/cart.html', context={'orders': cart.orders.all()})


def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        locale='fr',
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1.8000',
        cancel_url='http://127.0.0.1.8000',
    )
    # Code 303 est le code de redirection
    return redirect(session.url, code=303)


def delete_cart(request):
    # On vérifie que le panier puis on l'assigne dans la variable cart
    if cart := request.user.cart:
        # On utilise la méthode delet créer dans le modèle, la logique du modèle sera appliqué
        cart.delete()

    return redirect('index')