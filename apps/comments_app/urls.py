from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^profile/(?P<num>[0-9]+)$', views.profile),
    url(r'^add_friend/(?P<num1>[0-9]+)/(?P<num2>[0-9]+)$', views.add_friend),
    url(r'^remove_friend/(?P<num>[0-9]+)$', views.remove),
    url(r'^other_profile/(?P<num>[0-9]+)$', views.other_profile),
]