from django.urls import path
from gce_app import views as v

app_name = 'gce_app'

urlpatterns = [
    path('', v.index, name = 'index')
]