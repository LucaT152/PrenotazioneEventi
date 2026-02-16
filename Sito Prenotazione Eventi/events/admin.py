#REGISTRO LE CLASSI
from django.contrib import admin
from .models import Evento, Prenotazione


class EventoAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'data', 'posti_totali', 'creatore')
    list_filter = ('data',)
    search_fields = ('titolo',)
    ordering = ('data',)


class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('evento', 'utente', 'data_prenotazione')
    list_filter = ('evento',)
    search_fields = ('evento__titolo', 'utente__username')

admin.site.register(Evento, EventoAdmin)
admin.site.register(Prenotazione, PrenotazioneAdmin)