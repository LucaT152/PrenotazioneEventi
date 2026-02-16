from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('eventi/', views.EventoListView.as_view(), name='evento-list'),
    path('evento/<int:pk>/', views.EventoDetailView.as_view(), name='evento-detail'),
    path('evento/<int:pk>/prenota/', views.prenota_evento, name='prenota-evento'),
    path('resetlogin/<path:next>', views.resetlogin, name='resetlogin'),
    path('signup/<path:next>/', views.signup, name='signup'),
    path('mie-prenotazioni/', views.mie_prenotazioni, name='mie-prenotazioni'),
    path('prenotazione/<int:pk>/disdici/',views.disdici_prenotazione,name='disdici-prenotazione'),
    path('prenotazioni-eventi/',views.prenotazioni_eventi,name='prenotazioni-eventi'),
    
]