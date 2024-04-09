from django.urls import path

from store.views import ticket_detail, add_to_cart, cart, delete_cart, create_checkout_session, checkout_success
from store.views import stripe_webhook, update_quantitites

app_name = 'store'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('cart/update_quantities/', update_quantitites, name='update-quantities'),
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/success', checkout_success, name='checkout-success'),
    path('cart/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('cart/delete', delete_cart, name='delete-cart'),
    path('ticket/<str:slug>/', ticket_detail, name='ticket'),
    path('ticket/<str:slug>/add-to-cart/', add_to_cart, name='add-to-cart'),
]