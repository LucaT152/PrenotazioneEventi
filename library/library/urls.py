"""
Questa è come se fosse l'ingresso della mia struttura e mi collegada fuori alle pagine interne.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Per la ridirezione
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Mi collego alla pagina admin
    path('catalog/', include('catalog.urls')),  # Tutto quello che inizia con /catalog/ va nella stanza 'catalog'
    path('', RedirectView.as_view(url='catalog/')),  # Se arrivi all'ingresso, vai direttamente nella stanza catalog
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   #servono per poter utilizzare fogli di stile

urlpatterns += [ path('accounts/', include('django.contrib.auth.urls')), ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)