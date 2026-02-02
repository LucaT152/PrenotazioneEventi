#QUI DEFINISCO LE CLASSI

from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=True)
    data = models.DateTimeField()
    posti_totali = models.PositiveIntegerField()
    creatore = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titolo
    
class Prenotazione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)  
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField()

    class Meta:
        unique_together = ('evento', 'utente')

    def __str__(self):
        return f"{self.utente.username} → {self.evento.titolo}"  