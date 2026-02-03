from .models import Evento, Prenotazione
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import SignupForm
from django.contrib import messages
from django.utils import timezone


def index(request):
    eventi = Evento.objects.filter(data__gt=timezone.now()).order_by('data')


    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits

    return render(request, 'index.html', {
        'eventi': eventi,
        'num_visits': num_visits
    })

class EventoListView(generic.ListView):
    model = Evento
    paginate_by = 5

class EventoDetailView(generic.DetailView):
    model = Evento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['gia_prenotato'] = Prenotazione.objects.filter(
                evento=self.object,
                utente=self.request.user
            ).exists()
        return context

@login_required
def prenota_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    # Controllo evento prenotabile
    if evento.data <= timezone.now():
        messages.error(request, "Evento non più prenotabile.")
        return redirect('evento-detail', pk=pk)

    if evento.posti_disponibili() <= 0:
        messages.error(request, "Evento completo.")
        return redirect('evento-detail', pk=pk)

    prenotazione, created = Prenotazione.objects.get_or_create(
        utente=request.user,
        evento=evento,
    )

    if created:
        messages.success(request, "Prenotazione effettuata con successo!")
    else:
        messages.warning(request, "Hai già prenotato questo evento.")

    return redirect('evento-detail', pk=pk)

def signup(request, next):

    if request.method != 'POST':
        form = SignupForm()
        return render(request, 'catalog/signup.html', {'form': form})

    else:
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            auth_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, auth_user)

            gruppo_utenti = Group.objects.get(name='Utenti')
            auth_user.groups.add(gruppo_utenti)

            if not next or 'signup' in next or 'login' in next:
                next = reverse('index')
                
            return HttpResponseRedirect(next)

        else:
            return render(request, 'catalog/signup.html', {'form': form})
        
def resetlogin(request, next):
    request.session['num_visits'] = 0
    request.session.modified = True
    return HttpResponseRedirect(reverse('login') + "?next=" + next)

@login_required
def mie_prenotazioni(request):
    prenotazioni = Prenotazione.objects.filter(
        utente=request.user
    ).select_related('evento')

    return render(request, 'catalog/mie_prenotazioni.html', {
        'prenotazioni': prenotazioni
    })

@login_required
def disdici_prenotazione(request, pk):
    prenotazione = get_object_or_404(
        Prenotazione,
        pk=pk,
        utente=request.user
    )

    prenotazione.delete()
    messages.success(request, "Prenotazione annullata con successo.")

    return redirect('mie-prenotazioni')