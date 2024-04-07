from django.db import models
from django.urls import reverse
from django.utils import timezone

from JeuxOlympiques.settings import AUTH_USER_MODEL
from accounts.models import CustomUser


# Create your models here.

class Ticket(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
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
        return reverse('ticket', kwargs={'slug': self.slug})


class Order(models.Model):
    # Relation un à plusieurs. Un utilisatateur peut commander plusieurs billets
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    # date de commande des billets
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.ticket.name} - ({self.quantity})"


class Cart(models.Model):
    # Un utilisateur peut avoir un seul panier
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # une commande peut avoir plusieurs billets
    orders = models.ManyToManyField(Order)

    def __str__(self):
        # On affiche le nom d'utilisateur
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            # Méthode qui permet d'afficher la date par rapport au fuseau horaire
            order.ordered_date = timezone.now()
            order.save()

        # On garde nos articles commandé mais casse la relation avec le panier pour le vider
        self.orders.clear()
        # On ne remplace pas la méthode delete mais on la surcharge
        super().delete(*args, **kwargs)



