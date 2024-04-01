from django.contrib import admin

from store.models import Ticket, Order, Cart

# Register your models here.

admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(Cart)
