from .models import Evento, Prenotazione
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm

def index(request):
    eventi = Evento.objects.all().order_by('data')

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

    # evita doppia prenotazione
    Prenotazione.objects.get_or_create(
        evento=evento,
        utente=request.user
    )

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