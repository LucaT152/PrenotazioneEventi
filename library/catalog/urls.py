from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('eventi/', views.EventoListView.as_view(), name='eventi'),
    path('evento/<int:pk>/', views.EventoDetailView.as_view(), name='evento-detail'),
    path('evento/<int:pk>/prenota/', views.prenota_evento, name='prenota-evento'),
]