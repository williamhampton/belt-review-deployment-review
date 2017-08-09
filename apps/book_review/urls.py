from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add, name = 'add'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^books$', views.books_route, name = 'books'),
    url(r'^books/add$', views.newbook, name = 'newbook'),
    url(r'^books/create$', views.createbook, name = 'createbook'),
    url(r'^books/newreview2/(?P<id>\d+)$', views.newreview2, name = 'newreview'),
    url(r'^users/(?P<id>\d+)$',views.user_display, name = 'user_display'),
    url(r'^book/(?P<id>\d+)$',views.book_reviews, name = 'book_reviews'),
    url(r'^reviews/destroy/(?P<id>\d+)$',views.destroy, name = 'destroy'),
    url(r'^logout$', views.logout, name= 'logout'),
    url(r'^game$', views.game, name= 'game'),
    url(r'^books/(?P<letter>([a-zA-Z]+))$', views.alphabetizedbook),
    url(r'^books/author/(?P<letter>([a-zA-Z]+))$', views.alphabetizedauthor),
    url(r'^author/(?P<id>\d+)$',views.authordisplay),
    url(r'^books/newreviewfrombook/(?P<id>\d+)$', views.newreview2),
    url(r'^booksearch$', views.booksearch),
    url(r'^',views.silly),
]
