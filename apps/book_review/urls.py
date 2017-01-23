from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^books$', views.books_route, name = 'books'),
    url(r'^books/add$', views.newbook, name = 'newbook'),
    url(r'^books/create$', views.createbook, name = 'createbook'),
    url(r'^books/newreview/(?P<id>\d+)$', views.newreview, name = 'newreview'),
    url(r'^users/(?P<id>\d+)$',views.user_display, name = 'user_display'),
    url(r'^books/(?P<id>\d+)$',views.book_reviews, name = 'book_reviews'),
    url(r'^reviews/destroy/(?P<id>\d+)$',views.destroy, name = 'destroy'),



]
