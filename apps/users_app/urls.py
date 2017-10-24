from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login_process', views.login_process),
    url(r'^logout$', views.logout),
]