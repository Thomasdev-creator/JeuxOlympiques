from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from store.models import Ticket


class StoreTest(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            name='Offre solo',
            price=48,
            quantity=6,
            description='Offre solo description',
        )

    # client de TestCase nous permet de faire de requêtre vers notre site
    def test_tickets_are_shown_on_index_page(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        # On vérifie que le type de ticket est présent dans la page html
        self.assertIn(self.ticket.type_of_ticket, str(response.content))
        self.assertIn(self.ticket.thumbnail_url(), str(response.content))

    # On test si le bouton de connexion est affiché si l'utilisateur n'est pas connecté
    def test_connexion_link_shown_when_user_not_connected(self):
        response = self.client.get(reverse('index'))
        self.assertIn("Connexion", str(response.content))

    # On test la redirection vers la page de login
    def test_redirect_when_anonymous_user_access_cart_view(self):
        response = self.client.get(reverse('store:cart'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("accounts:login")}?next={reverse("store:cart")}', status_code=302)


# On vérifie la redirection quand les données utilisateurs sont valides ou non
"""class StoreLoggedInTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="",
            first_name="tom",
            last_name="smith",
            password=""
        )

    def test_valid_login(self):
        data = {'email': '', 'password': ''}
        response = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('index'))
        self.assertIn("Adresse de livraison", str(response.content))

    def test_invalid_login(self):
        data = {'email': '', 'password': ''}
        response = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    # On connecte notre utilisateur
    def test_profile_change(self):
        self.client.login(email="", password="")

        data = {'email': '', 'password': '', 'first_name': 'tom', 'last_name': 'john'}

        response = self.client.post(reverse('accounts:profile'), data=data)
        self.assertEqual(response.status_code, 302)
        tom = CustomUser.objects.get(email="")
        self.assertEqual(tom.last_name, "john")"""
