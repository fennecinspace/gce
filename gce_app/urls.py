from django.urls import path
from django.contrib.auth.decorators import login_required
from gce_app.views import MainView, ProfileView, AnnonceView , SaisirView, NotesView, AffichageView, UsersView
## ajax only views
from gce_app.views import notification_state_changer, search_suggestion_feeder, search_result_feeder, reclamation_handler
## scheduled_operation
# from gce_app.views import scheduled_operation

app_name = 'gce_app'

urlpatterns = [
    path('', MainView.as_view(), name = 'home'),
    path('annonces/', login_required(AnnonceView.as_view()), name='annonces'),
    path('saisir/', login_required(SaisirView.as_view()), name='saisir'),
    path('notes/', login_required(NotesView.as_view()), name='notes'),
    path('affichages/', login_required(AffichageView.as_view()), name='affichage'),
    path('personnels/', login_required(UsersView.as_view()), name='personnels'),
    ## ajax only
    path('notification_state_changer_VIEW/', notification_state_changer, name='notification_state_changer'),
    path('search_suggestions_VIEW/', search_suggestion_feeder, name='search_suggestion_feeder'),
    path('search_result_VIEW/', search_result_feeder, name='search_result_feeder'),
    path('reclamation_handler_VIEW/', reclamation_handler, name='reclamation_handler'),

    ## profiles 
    path('etuds/<slug:pk>/', login_required(ProfileView.as_view()), {'profile': 'etud'}, name='student_profile'),
    path('techs/<slug:pk>/', login_required(ProfileView.as_view()), {'profile': 'tech'}, name='technicien_profile'),
    path('ensgs/<slug:pk>/', login_required(ProfileView.as_view()), {'profile': 'ensg'}, name='enseignant_profile'),
    path('chefs/<slug:pk>/', login_required(ProfileView.as_view()), {'profile': 'chef'}, name='chef_departement_profile'),

    ## scheduled_operation
    # path('scheduled_operation/', scheduled_operation, name='scheduled_operation'),
]