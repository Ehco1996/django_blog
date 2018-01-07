from django.conf.urls import url
from . import views


app_name = 'earimg'
urlpatterns = [
    url(r'^$', views.index, name='era_index'),
]
