from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.travel_index),
    url(r'^add$', views.add),
    url(r'^add_trip$', views.add_trip),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip),
    url(r'^destination/(?P<id>\d+)$', views.destination)
]