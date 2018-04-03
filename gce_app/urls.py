from django.urls import path
from gce_app.views import mainView, testpage, notification_state_changer, search_suggestion_feeder, search_result_feeder

app_name = 'gce_app'

urlpatterns = [
    path('testpage/', testpage, name = 'testpage'),
    path('', mainView.as_view(), name = 'home'),
    path('notification_state_changer_VIEW', notification_state_changer, name='notification_state_changer'),
    path('search_suggestions_VIEW', search_suggestion_feeder, name='search_suggestion_feeder'),
    path('search_result_VIEW', search_result_feeder, name='search_result_feeder'),
]