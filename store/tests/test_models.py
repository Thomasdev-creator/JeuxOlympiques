from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from store.models import Ticket, Cart, Order


class TicketTest(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            name='Offre solo',
            price=48,
            quantity=6,
            description='Offre solo description', )

    # Permet de vérifier si le slug du billet est créer automatiquement
    def test_ticket_slug_is_automatically_generated(self):
        self.assertEqual(self.ticket.slug, 'offre-solo')

    # On s'assure que l'url retouné n'est pas modifié
    def test_ticket_absolute_url(self):
        self.assertEqual(self.ticket.get_absolute_url(), reverse("store:ticket", kwargs={"slug": self.ticket.slug}))

    # On vérifie que les éléments de la commande sont modifiés si on supprime le panier


class CartTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            email="tom@test.com",
            password="12345678"
        )
        ticket = Ticket.objects.create(
            name='Offre solo'
        )
        self.cart = Cart.objects.create(
            user=user,
        )
        order = Order.objects.create(
            user=user,
            ticket=ticket
        )
        self.cart.orders.add(order)
        self.cart.save()

    # On test si la commande est modifié lors de la suppression du panier
    def test_orders_changed_when_cart_is_deleted(self):
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.delete()
        for order_pk in orders_pk:
            order = Order.objects.get(pk=order_pk)
            self.assertIsNotNone(order.ordered_date)
            self.assertTrue(order.ordered)
