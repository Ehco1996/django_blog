from django.conf.urls import url
from . import views


app_name = 'jumpgame'
urlpatterns = [
    url(r'^$', views.index, name='jump'),
]
