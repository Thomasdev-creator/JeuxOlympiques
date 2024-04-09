from django import forms

from store.models import Order


class OrderForm(forms.ModelForm):
    # On boucle sur un nombre de 1 à 10
    quantity = forms.ChoiceField(choices=[(i, i) for i in range(1, 11)])
    delete = forms.BooleanField(initial=False,
                                required=False,
                                label="Supprimer")

    # On lie notre formulaire au modèle order
    class Meta:
        model = Order
        fields = ['quantity']

    def save(self, *args, **kwargs):
        if self.cleaned_data["delete"]:
            self.instance.delete()
            # Article, de l'utilisateur dans son panier de sa commande
            if self.instance.user.cart.orders.count() == 0:
                self.instance.user.cart.delete()
            return True
        return super().save(*args, **kwargs)
    # cleaned_data = dictionnaire des données après que le formulaire est été validé
