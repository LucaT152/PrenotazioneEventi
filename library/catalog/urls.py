from django.urls import path
from . import views
#possibile import mancante

urlpatterns = [ path('' , views.index , name='index' ), 
               path('authors/', views.AuthorListView.as_view(), name='author-list'), 
               path('books/',views.BookListView.as_view(), name='book-list'), path('resetlogin/<path:next>', views.resetlogin, name='resetlogin') ] # "Se sei nella stanza catalog, questa è la home page"

urlpatterns += [path('book/<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
                path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'), 
                path('loaned_books/', views.AllLoanedBooksListView.as_view(),name='all-loaned-books'),
                path('book/<uuid:pk>/renew/',views.renew_book_librarian,name='renew-book-librarian'),
                path('signup/<path:next>', views.user_signup, name='signup')] #il name serve per far riferimento alla pagina con quel nome e quindi non ci interessa dell'url lo possimo cambiare senza fare casino nel nostro sito
