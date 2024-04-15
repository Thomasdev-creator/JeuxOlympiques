from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Sports(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=128, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='Sports', blank=True, null=True)

    def __str__(self):
        # On retourne une instance qui sera le nom du sport
        return self.name

    def get_absolute_url(self):
        # On passe en argument à la fonction reverse le nom indiqué dans le ficher urls.py
        # Dans un paramètre kwargs on lui passe un dictionnaire avec les différents éléments de l'url
        # C'est donc le slug de l'instance du sport
        # Et on le passe au paramètre slug que l'on retrouve dans le fichier urls
        return reverse('sports:sport-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Si un slug existe on l'utilise sinon on en créer un nouveau à partir du nom
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)