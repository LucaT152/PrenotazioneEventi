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
from django.contrib.admin.views.decorators import staff_member_required


class IndexView(generic.ListView):
    model = Evento
    template_name = 'index.html'
    context_object_name = 'eventi'
    paginate_by = 5

    def get_queryset(self):
        return Evento.objects.filter(
            data__gt=timezone.now()
        ).order_by('data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_visits = self.request.session.get('num_visits', 0) + 1
        self.request.session['num_visits'] = num_visits
        context['num_visits'] = num_visits
        return context

class EventoListView(generic.ListView):
    model = Evento
    template_name = 'events/evento_list.html'
    context_object_name = 'eventi'
    paginate_by = 5

    def get_queryset(self):
        queryset = Evento.objects.filter(data__gte=timezone.now())

        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')

        if from_date:
            queryset = queryset.filter(data__date__gte=from_date)

        if to_date:
            queryset = queryset.filter(data__date__lte=to_date)

        return queryset.order_by('data')

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

    if evento.posti_disponibili <= 0:
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
        return render(request, 'events/signup.html', {'form': form})

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
            return render(request, 'events/signup.html', {'form': form})
        
def resetlogin(request, next):
    request.session['num_visits'] = 0
    request.session.modified = True
    return HttpResponseRedirect(reverse('login') + "?next=" + next)

@login_required
def mie_prenotazioni(request):
    prenotazioni = Prenotazione.objects.filter(
        utente=request.user
    ).select_related('evento')

    return render(request, 'events/mie_prenotazioni.html', {
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


@staff_member_required
def prenotazioni_eventi(request):
    eventi = Evento.objects.filter(
        data__gt=timezone.now()
    ).order_by('data')

    return render(request, 'events/prenotazioni_eventi.html', {
        'eventi': eventi
    })