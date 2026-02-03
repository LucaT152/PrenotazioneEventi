#QUI DEFINISCO LE CLASSI
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Evento(models.Model):
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=True)
    data = models.DateTimeField()
    posti_totali = models.PositiveIntegerField()
    creatore = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventi"

    def get_absolute_url(self):
        return reverse('evento-detail', args=[str(self.id)])

    def __str__(self):
        return self.titolo
    
    def posti_disponibili(self):
        return self.posti_totali - self.prenotazione_set.count()
    
    def is_prenotabile(self):
        return self.data > timezone.now() and self.posti_disponibili() > 0
    
class Prenotazione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)  
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('evento', 'utente')
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"        

    def __str__(self):
        return f"{self.utente.username} → {self.evento.titolo}"  