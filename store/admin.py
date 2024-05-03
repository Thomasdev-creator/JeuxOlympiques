from django.contrib import admin
from django.db.models import Sum
from store.models import Ticket, Order, Cart


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ticket', 'quantity', 'ordered', 'ordered_date']
    search_fields = ['ticket__ticket_type']  # Champ de recherche pour le type de billet
    list_filter = ['ticket', 'ordered']  # Filtre pour le type de billet

    def get_ticket_count(self, obj):
        ticket_count = Order.objects.filter(ticket=obj.ticket, ordered=True).aggregate(total=Sum('quantity'))['total']
        return ticket_count if ticket_count else 0

    get_ticket_count.short_description = 'Afficher le nombre de tickets vendus'


admin.site.register(Ticket)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
