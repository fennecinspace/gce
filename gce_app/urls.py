from django.urls import path
from gce_app.views import mainView, testpage

app_name = 'gce_app'

urlpatterns = [
    path('testpage/', testpage, name = 'testpage'),
    path('', mainView.as_view(), name = 'home'),
]