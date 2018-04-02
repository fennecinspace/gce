## page rendering and views modules
from django.shortcuts import render
from django.views.generic import TemplateView
## authentification modules
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
## json modules for ajax
from django.http.response import JsonResponse
import json
## user search modules
from difflib import SequenceMatcher # to get ratio of similarity between 2 strings
from django.db.models import Q # to make complex queries
import re # to use regex
## needed models
from gce_app.models import User, Utilisateur, Notification, Parcours, Specialite, Section, Groupe, Etudiant, FichierCopie, FichierCorrection

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
    return {'notifications_list': notifications,}

## returns data for suggested users if exist
def get_student_search_suggestions(search_entry):
    ### processing user search entry
    suggestions = []
    search_entry = search_entry.lower()
    search_entry = re.sub(r'[^a-zA-Z ]', '', search_entry) # stripping entry from non latin letters
    search_entry = re.sub(r' +', ' ', search_entry) # turning multiple whitespaces to one
    ## finding possible suggestions
    # first try : trying to march based similarity ratio between the first and last names and the search entry
    all_Students = Utilisateur.objects.filter(id_utilisateur__regex = r"etud")
    for user in all_Students:
        # matching first name
        if SequenceMatcher(None, user.info_utilisateur.first_name, search_entry).ratio() > 0.9:
            suggestions += [user]
        # matching last name
        if SequenceMatcher(None, user.info_utilisateur.last_name, search_entry).ratio() > 0.9:
            suggestions += [user]
        # matching last name + first name
        user_full_name = user.info_utilisateur.last_name + ' ' + user.info_utilisateur.first_name
        if SequenceMatcher(None, user_full_name, search_entry).ratio() > 0.9:
            suggestions += [user]
        # matching first name + last name
        user_full_name = user.info_utilisateur.first_name + ' ' + user.info_utilisateur.last_name
        if SequenceMatcher(None, user_full_name, search_entry).ratio() > 0.9:
            suggestions += [user]
    # return suggestions[:5] # allow a max of 5 suggestions
    if len(suggestions) >= 5:
            print('done 1')
            return suggestions[:5] #5 suggestions found -> return them
    # second try : trying to match charachter by character with the first and last names
    split_search_entry = search_entry.split()
    for search_word in split_search_entry:
        suggestions += list(Utilisateur.objects.filter(Q(info_utilisateur__in = User.objects.filter(Q(first_name__regex = search_word) | Q(last_name__regex = search_word))) & Q(id_utilisateur__regex = r"etud")))
        if len(suggestions) >= 5:
            print('done 2')
            return suggestions[:5] #5 suggestions found -> return them

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


#######################################################
###################### VIEWS ##########################
#######################################################

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
            all_user_data = get_student_search_suggestions(search_entry)
            if all_user_data:
                data = {'success': True, 'users_data': [],}
                for user_data in all_user_data:
                    data['users_data'] += [{
                        'id': user_data.id_utilisateur,
                        'first_name': user_data.info_utilisateur.first_name,
                        'last_name': user_data.info_utilisateur.last_name,
                        'avatar': user_data.avatar_utilisateur.url,
                        'level': Groupe.objects.filter(id_groupe = Etudiant.objects.filter(id_etudiant = user_data)[0].id_groupe.id_groupe)[0].id_section.id_specialite.id_parcours.nom,
                        'branch': Groupe.objects.filter(id_groupe = Etudiant.objects.filter(id_etudiant = user_data)[0].id_groupe.id_groupe)[0].id_section.id_specialite.id_parcours.id_filiere.nom,
                    }]
    stringfied_data = json.dumps(data)
    return JsonResponse(stringfied_data, safe = False)


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