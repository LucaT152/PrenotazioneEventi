from django.shortcuts import render
from .models import Evento, Prenotazione
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

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