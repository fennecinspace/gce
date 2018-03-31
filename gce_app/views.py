## importing page rendering and views modules
from django.shortcuts import render
from django.views.generic import TemplateView
## importing authentification modules
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
## importing json for ajax
from django.http.response import JsonResponse
import json
## importing needed models
from gce_app.models import Utilisateur, Notification, Parcours, Specialite, Section, Groupe, Etudiant, FichierCopie, FichierCorrection

## returns the user's data
def get_user_data(u_obj):
    user_avatar = u_obj.avatar_utilisateur
    user_username = u_obj.info_utilisateur.username
    user_email = u_obj.info_utilisateur.email
    user_password = u_obj.info_utilisateur.password
    user_type = u_obj.type_utilisateur
    return {
        'user_avatar' : user_avatar,
        'user_username' : user_username,
        'user_email' : user_email,
        'user_password' : user_password,
        'user_type' : user_type,
    }

## returns the user's querylist of notifications in a dictionary
def get_user_notifications(u_obj):
    notifications = []
    allNotifications = Notification.objects.filter(id_utilisateur__in = [u_obj])
    for notification in allNotifications:
        if notification.vue_notification == False:
            notifications += [notification]

    return {
        'notifications_list': notifications,
    }

import random
## returns data for suggested users if exist
def get_search_suggestions(search_entry):
    x = list(Utilisateur.objects.all()[random.randint(1,20):random.randint(25,40)])
    if len(x) >= 5:
        return x[:5]
    else:
        return x

## returns the template based on the signed in user's type
def get_base_template(req):
    loggedin_user = Utilisateur.objects.all().filter(info_utilisateur__in = [req.user])[0]
    user_data = get_user_data(loggedin_user)
    notifications = get_user_notifications(loggedin_user)
    data = user_data
    data.update(notifications) ##merging the 2 dicts in one
    if user_data['user_type'] == 'etud':
        return render(req, 'gce_app/etud/etud_index.html', context = data)
    if user_data['user_type'] == 'tech':
        return render(req, 'gce_app/tech/tech_index.html', context = data)
    if user_data['user_type'] == 'ensg':
        return render(req, 'gce_app/ensg/ensg_index.html', context = data)
    if user_data['user_type'] == 'chef':
        return render(req, 'gce_app/chef/chef_index.html', context = data)

## Main View
class mainView(TemplateView):
    def post(self,req):
        if req.user.is_anonymous:
            username = req.POST.get('username')
            password = req.POST.get('password')

            user = authenticate(username = username, password = password)
            if user:
                login(req,user)
            else:
                return HttpResponse('Wrong Info')
        else:
            if req.POST.get('logout'):
                logout(req)
                return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        return get_base_template(req)

    def get(self,req):
        if req.user.is_anonymous: # if user is not logged in return login page
            return render(req, 'gce_app/common/login.html', context = None)
        
        return get_base_template(req)

## AJAX NOTIFICATION HANDLER VIEW
@login_required
def notification_state_changer(req):
    if req.method == 'POST':
        if req.is_ajax():
            notification_id = req.POST.get('notif_id')
            Notification.objects.filter(id_notification = notification_id).delete()

    return HttpResponse(req)

## AJAX SEARCH SUGGESTIONS HANDLER VIEW
@login_required
def search_suggestion_feeder(req):
    data = {'success': False}
    if req.method == 'POST':
        if req.is_ajax():
            search_entry = req.POST.get('search_entry')
            all_user_data = get_search_suggestions(search_entry)
            if all_user_data:
                data = {'success': True, 'users_data': [],}
                for user_data in all_user_data:
                    data['users_data'] += [{
                        'id': user_data.id_utilisateur,
                        'first_name': user_data.info_utilisateur.first_name,
                        'last_name': user_data.info_utilisateur.last_name,
                        'avatar': user_data.avatar_utilisateur.url,
                        'level': Groupe.objects.filter(id_groupe = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.all()[0])[0].id_groupe.id_groupe)[0].id_section.id_specialite.id_parcours.nom,
                        'branch': Groupe.objects.filter(id_groupe = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.all()[0])[0].id_groupe.id_groupe)[0].id_section.id_specialite.id_parcours.id_filiere.nom,
                    }]
    stringfied_data = json.dumps(data)
    return JsonResponse(stringfied_data, safe = False)



#### INITIAL TEST PAGE
def testpage(req):
    copie = FichierCopie.objects.all()[0].emplacement_fichier
    correction = FichierCorrection.objects.all()[0].emplacement_fichier
    myDict = {
        'testing' : 'TESTING STATIC/MEDIA/TEMPLATES',
        'copySample': copie,
        'correctionSample': correction,
    }
    
    return render(req, 'gce_app/testpage.html', context = myDict)