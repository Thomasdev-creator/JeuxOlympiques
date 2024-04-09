from django.test import TestCase

from accounts.models import CustomUser
from store.models import Ticket


class UserTest(TestCase):
    def setUp(self):
        Ticket.objects.create(
            name='Offre solo',
            price='10',
            quantity='10',
            description='Offre solo'
        )
        self.user: CustomUser = CustomUser.objects.create_user(
            email='tom@test.com',
            password='12345678'
        )

    def test_add_to_cart(self):
        self.user.add_to_cart(slug='offre-solo')
        # On vérifie que le slug est bon et que le panier contient un article
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().ticket.slug, 'offre-solo')
        # Vérifie ensuite que la quantité est la bonne
        self.user.add_to_cart(slug='offre-solo')
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().quantity, 2)
