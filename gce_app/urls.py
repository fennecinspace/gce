from django.urls import path
from django.contrib.auth.decorators import login_required
from gce_app.views import MainView, AnnonceView, StudentProfileView, SaisirView, NotesView
## ajax only views
from gce_app.views import notification_state_changer, search_suggestion_feeder, search_result_feeder

app_name = 'gce_app'

urlpatterns = [
    path('', MainView.as_view(), name = 'home'),
    path('notification_state_changer_VIEW/', notification_state_changer, name='notification_state_changer'),
    path('search_suggestions_VIEW/', search_suggestion_feeder, name='search_suggestion_feeder'),
    path('search_result_VIEW/', search_result_feeder, name='search_result_feeder'),
    path('etuds/<slug:pk>/', login_required(StudentProfileView.as_view()), name='profile'),
    path('annonces/', login_required(AnnonceView.as_view()), name='annonces'),
    path('saisir/', login_required(SaisirView.as_view()), name='saisir'),
    path('notes/', login_required(NotesView.as_view()), name='notes'),
]