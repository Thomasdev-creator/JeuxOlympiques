from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from iso3166 import countries


# Create your models here.
class CustomUserManager(BaseUserManager):
    # Les kwargs prennent en paramètre tout le reste des paramètres disponibles dans baseusermanager
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("L'adresse email est obligatoire")

        email = self.normalize_email(email)
        # On créer une instance de CustomUser
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        kwargs['is_active'] = True

        return self.create_user(email=email, password=password, **kwargs)
        # On retourne à notre fonction les paramètres


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    stripe_id = models.CharField(max_length=90, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


ADDRESS_FORMAT = """
{name}
{address_1}
{address_2}
{city}, {zip_code}
{country}
"""


class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=240)
    address_1 = models.CharField(max_length=240, help_text="Adresse et numéro de rue.")
    address_2 = models.CharField(max_length=240, blank=True, null=True, help_text="Bâtiment, étage...")
    city = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=32)
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries])

    def __str__(self):
        # On passe notre dictionnaire dict à format qui prend en valeur une instance de class
        # On unpack ce dictionnaire avec les deux **
        # format qui nous permet de passer des informations
        # .strip enlève les élèments au début et à la fin du chaîne de caractère
        # get_country_display retourne le nom du pays au complet
        # Je créer un nouveau dictionnaire de mes attributs d'instance avec .copy
        data = self.__dict__.copy()
        data.update(country=self.get_country_display().upper())
        return ADDRESS_FORMAT.format(**data).strip("\n")
