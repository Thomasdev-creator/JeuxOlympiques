import qrcode
import base64
import secrets
from io import BytesIO
from PIL import Image

from django.core.files import File

from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from JeuxOlympiques import settings
from JeuxOlympiques.settings import AUTH_USER_MODEL


# from accounts.models import CustomUser


# Create your models here.

class Ticket(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    # valeur par default est 0.0
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    # Image chargé depuis le fichier Tickets, ne peut pas être null en base de données
    thumbnail = models.ImageField(upload_to='Tickets', blank=True, null=True)
    type_of_ticket = models.CharField(max_length=50)
    start_validity = models.DateField(blank=True, null=True)
    end_validity = models.DateField(blank=True, null=True)
    # Stock l'identifiant de stripe
    stripe_id = models.CharField(max_length=90, blank=True)

    def __str__(self):
        # On retourne une instance qui sera le nom du produit
        return self.name

    def get_absolute_url(self):
        # On passe en argument à la fonction reverse le nom indiqué dans le ficher urls.py
        # Dans un paramètre kwargs on lui passe un dictionnaire avec les différents éléments de l'url
        # C'est donc le slug de l'instance du ticket
        # Et on le passe au paramètre slug que l'on retrouve dans le fichier urls
        return reverse('store:ticket', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Si un slug existe on l'utilise sinon on en créer un nouveau à partir du nom
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

    # On gère le cas ou aucune image n'est ajouté à thumbnail
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else static("img/default.jpg")


class Order(models.Model):
    # Relation un à plusieurs. Un utilisatateur peut commander plusieurs billets
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    # date de commande des billets
    ordered_date = models.DateTimeField(blank=True, null=True)
    key_after_success_payment = models.CharField(max_length=32, blank=True, null=True)
    combined_key = models.CharField(max_length=60, blank=True, null=True)
    qr_code_thumbnail = models.ImageField(upload_to='QRCode', blank=True, null=True)

    def __str__(self):
        return f"{self.ticket.name} - ({self.quantity})"


class Cart(models.Model):
    # Un utilisateur peut avoir un seul panier
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # une commande peut avoir plusieurs billets
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f"Panier de l'utilisateur {self.user.email}"

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            # Méthode qui permet d'afficher la date par rapport au fuseau horaire
            order.ordered_date = timezone.now()
            order.save()

            if not order.key_after_success_payment:
                key = secrets.token_urlsafe(16)
                order.key_after_success_payment = key
                order.save()

            # On récupère auth key de l'utilisateur depuis la vue complete order
            auth_key = kwargs.pop('auth_key', None)
            key_after_success_payment = order.key_after_success_payment
            # Concaténation des deux clefs
            combined_key = f"{auth_key}:{key_after_success_payment}"
            if auth_key and key_after_success_payment:
                order.combined_key = combined_key
                order.save()

                # Créer le QR code et sa version miniaturisée
                if order.combined_key:
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(order.combined_key)
                    qr.make(fit=True)

                    img = qr.make_image(fill_color="black", back_color="white")

                    # Génération de la version miniaturisée
                    thumbnail = img.copy()
                    thumbnail.thumbnail((100, 100))  # Redimensionnement de l'image
                    thumbnail_buffer = BytesIO()
                    thumbnail.save(thumbnail_buffer, format='PNG')
                    thumbnail_buffer.seek(0)

                    # Sauvegarde de la version miniaturisée
                    thumbnail_filename = f'qr_code_thumbnail_{order.pk}.png'
                    order.qr_code_thumbnail.save(thumbnail_filename, File(thumbnail_buffer), save=False)
                    order.save()

                    # Obtenez l'URL de l'image du QR code à partir de la vue qui sert les fichiers statiques
                    """qr_code_url = reverse('qr_code_thumbnail', kwargs={'pk': order.pk})
                    order.qr_code_url = qr_code_url  # Stockez l'URL dans votre modèle
                    order.save()"""

        # On garde nos articles commandé mais casse la relation avec le panier pour le vider
        self.orders.clear()
        # On ne remplace pas la méthode delete mais on la surcharge
        super().delete(*args, **kwargs)
