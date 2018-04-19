## page rendering and views modules
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, DetailView
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
## models
from gce_app.models import *
## forms
from gce_app.forms import avatar_upload_form
## extra 
from django.conf import settings
from datetime import datetime
import os


## returns the user's data
def get_user_data(u_obj):
    user_id = u_obj.pk
    user_avatar = u_obj.avatar_utilisateur
    user_username = u_obj.info_utilisateur.username
    user_email = u_obj.info_utilisateur.email
    user_password = u_obj.info_utilisateur.password
    user_type = u_obj.type_utilisateur
    return {
        'user_id' : user_id,
        'user_avatar' : user_avatar,
        'user_username' : user_username,
        'user_email' : user_email,
        'user_password' : user_password,
        'user_type' : user_type,
    }


## returns the user's querylist of notifications in a dictionary
def get_user_notifications(u_obj):
    notifications = []
    allNotifications = Notification.objects.filter(Q(id_utilisateur__in = [u_obj]) & Q(vue_notification = False))
    for notification in allNotifications:
        if notification.vue_notification == False:
            notifications += [notification]
    return {'notifications_list': notifications,}


## returns student data
def get_final_versions(all_copies):
    all_versions = [list(VersionCopie.objects.filter(id_copie = copie)) for copie in all_copies]
    final_versions = []
    for version in all_versions:
        version.sort(key=lambda x : x.id , reverse=False) # sorting the copie version from oldest to newest
        final_versions += [version[len(version)-1]] # grabing the latest version
    return final_versions

def get_student_copies(student):
    all_copies = Copie.objects.filter(Q(id_etudiant = student) & Q(afficher_copie = True))
    return get_final_versions(all_copies)


def get_student_notes(student):
    final_versions = get_student_copies(student)
    notes = {}
    [notes.update({version.id_copie.annee_copie:[]}) for version in final_versions]
    for version in final_versions:
        notes[version.id_copie.annee_copie] += [version]
    return notes


def get_student_data(student):
    modules = Module.objects.filter(id_specialite = Specialite.objects.filter(id = (Section.objects.filter(id = Groupe.objects.filter(id = student.id_groupe.id)[0].id_section.id)[0].id_specialite.id))[0])
    teachers = Enseignant.objects.filter(modules__in = modules)
    notes = get_student_notes(student) # gettings final versions of copies categorized by school year
    marks = {k: notes[k] for k in sorted(notes,reverse=True)} # sorting from newest school year to oldest
    return {
        'modules': modules,
        'teachers': teachers,
        'marks': marks,
    }


def get_permitted_search_group(req, user_type):
    search_group = []
    if user_type == 'etud': # students of same parcours
        parcours_etud = Groupe.objects.filter(id = Etudiant.objects.filter (id_etudiant__in = Utilisateur.objects.filter(info_utilisateur = req.user))[0].id_groupe.id)[0].id_section.id_specialite.id_parcours
        all_Students = Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id = parcours_etud.id))))))
    elif user_type == 'ensg':
        specialite_ensg = Enseignant.objects.filter(id_enseignant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].modules.values_list('id_specialite',flat = True)
        all_Students = Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id__in = specialite_ensg)))))
    elif user_type == 'chef':
        filiere_chef = Filiere.objects.filter(id_chef_departement = ChefDepartement(id_chef_departement = Utilisateur.objects.filter(info_utilisateur = req.user)[0]))[0]
        all_Students = Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere = filiere_chef))))))
    elif user_type == 'tech':
        faculte_tech = Technicien.objects.filter(id_technicien = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].id_faculte
        all_Students = Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_domaine__in = Domaine.objects.filter(id_faculte = faculte_tech))))))))

    return all_Students


## returns data for suggested users if exist
def get_search_data(search_entry, req, req_type):
    ### processing user search entry
    search_data = [] ## will store results
    search_entry = search_entry.lower()
    search_entry = re.sub(r'[^a-zA-Z ]', '', search_entry) # stripping entry from non latin letters
    search_entry = re.sub(r' +', ' ', search_entry) # turning multiple whitespaces to one
    user_type = Utilisateur.objects.filter(info_utilisateur = req.user)[0].type_utilisateur
    # first try : trying to march based similarity ratio between the first and last names and the search entry
    all_Students = get_permitted_search_group(req, user_type)
    for user in all_Students:
        # matching first name
        if SequenceMatcher(None, user.info_utilisateur.first_name, search_entry).ratio() > 0.9:
            search_data += [user]
        # matching last name
        if SequenceMatcher(None, user.info_utilisateur.last_name, search_entry).ratio() > 0.9:
            search_data += [user]
        # matching last name + first name
        user_full_name = user.info_utilisateur.last_name + ' ' + user.info_utilisateur.first_name
        if SequenceMatcher(None, user_full_name, search_entry).ratio() > 0.9:
            search_data += [user]
        # matching first name + last name
        user_full_name = user.info_utilisateur.first_name + ' ' + user.info_utilisateur.last_name
        if SequenceMatcher(None, user_full_name, search_entry).ratio() > 0.9:
            search_data += [user]
        if (req_type == 'suggestions' and len(search_data) >= 5):
            return search_data[:5]
        if len(search_data) > 50:
            return search_data
    # second try : trying to match character by character with the first and last names
    split_search_entry = search_entry.split()
    for search_word in split_search_entry:
        if user_type == 'etud':
            parcours_etud = Groupe.objects.filter(id = Etudiant.objects.filter (id_etudiant__in = Utilisateur.objects.filter(info_utilisateur = req.user))[0].id_groupe.id)[0].id_section.id_specialite.id_parcours
            search_data += list(Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter( Q(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id = parcours_etud.id))))) & Q(id_etudiant__in = Utilisateur.objects.filter(Q(info_utilisateur__in = User.objects.filter(Q(first_name__regex = search_word) | Q(last_name__regex = search_word))))) ) ) )
        elif user_type == 'ensg':
            specialite_ensg = Enseignant.objects.filter(id_enseignant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].modules.values_list('id_specialite',flat = True)
            search_data += list(Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter( Q(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id__in = specialite_ensg)))) & Q(id_etudiant__in = Utilisateur.objects.filter(Q(info_utilisateur__in = User.objects.filter(Q(first_name__regex = search_word) | Q(last_name__regex = search_word))))) )))
        elif user_type == 'chef':
            filiere_chef = Filiere.objects.filter(id_chef_departement = ChefDepartement(id_chef_departement = Utilisateur.objects.filter(info_utilisateur = req.user)[0]))[0]
            search_data += list(Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter( Q(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere = filiere_chef))))) & Q(id_etudiant__in = Utilisateur.objects.filter(Q(info_utilisateur__in = User.objects.filter(Q(first_name__regex = search_word) | Q(last_name__regex = search_word))))) )))
        elif user_type == 'tech':
            faculte_tech = Technicien.objects.filter(id_technicien = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].id_faculte
            search_data += list(Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter( Q(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_domaine__in = Domaine.objects.filter(id_faculte = faculte_tech))))))) & Q(id_etudiant__in = Utilisateur.objects.filter(Q(info_utilisateur__in = User.objects.filter(Q(first_name__regex = search_word) | Q(last_name__regex = search_word))))) )))
    return search_data 


### annonce
def get_user_annonce(req, user_type):
    if user_type == 'etud':
        annonces = Annonce.objects.filter(Q(id_module__in = Module.objects.filter(id_specialite = Specialite.objects.filter(id = (Section.objects.filter(id = Groupe.objects.filter(id = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].id_groupe.id)[0].id_section.id)[0].id_specialite.id))[0])) & Q(afficher_annonce = True)).order_by('-id')
    elif user_type == 'ensg':
        annonces = Annonce.objects.filter(Q(id_module__in = Enseignant.objects.filter(id_enseignant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].modules.all()) & Q(afficher_annonce = True)).order_by('-id')
    elif user_type == 'chef':
        annonces = Annonce.objects.filter(id_module__in = Module.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0])[0])))).order_by('-id')
    return annonces

def create_new_annonce(req):
    title_annonce = req.POST.get('title')
    content_annonce = req.POST.get('content')
    module_annonce = req.POST.get('module')
    date_annonce = datetime.now().date()
    time_annonce = datetime.now().time()
    if req.POST.get('show') == 'false':
        show_annonce = False
    else:
        show_annonce = True
    annonce = Annonce(sujet_annonce = title_annonce, description_annonce = content_annonce, date_annonce = date_annonce, heure_annonce = time_annonce, afficher_annonce = show_annonce, id_module = Module.objects.filter(titre_module = module_annonce)[0])
    annonce.save()
    return annonce


## returns the template based on the signed in user's type
def get_home_template(req):
    loggedin_user = Utilisateur.objects.all().filter(info_utilisateur__in = [req.user])[0]
    user_data = get_user_data(loggedin_user)
    notifications = get_user_notifications(loggedin_user)
    data = user_data
    data.update(notifications) ##merging the 2 dicts in one
    return render(req, 'gce_app/common/home.html', context = data)


## returns entries not yet subbmited
def get_saisir_entries(module_title):
    all_copies = Copie.objects.filter(Q(id_module = Module.objects.filter(titre_module = module_title)[0]) & Q(modifiable = True))
    final_versions = get_final_versions(all_copies)
    entries = []
    for version in final_versions:
        entries += [FichierCopie.objects.filter(id_version = version)]
    return {'entries': entries}
    

#######################################################
###################### VIEWS ##########################
#######################################################

## AJAX NOTIFICATION HANDLER VIEW
@login_required
def notification_state_changer(req):
    if req.method == 'POST':
        if req.is_ajax():
            notification_id = req.POST.get('notif_id')
            notification_obj = Notification.objects.filter(id = notification_id)[0]
            notification_obj.vue_notification = True
            notification_obj.save()

    return HttpResponse(req)


## AJAX SEARCH SUGGESTIONS HANDLER VIEW
@login_required
def search_suggestion_feeder(req):
    data = {'success': False}
    if req.method == 'POST':
        if req.is_ajax():
            search_entry = req.POST.get('search_entry')
            all_user_data = get_search_data(search_entry, req, 'suggestions')
            if all_user_data:
                data = {'success': True, 'users_data': [],}
                for user_data in all_user_data:
                    user_parcours = Groupe.objects.filter(id = Etudiant.objects.filter(id_etudiant = user_data)[0].id_groupe.id)[0].id_section.id_specialite.id_parcours
                    data['users_data'] += [{
                        'id': user_data.id_utilisateur,
                        'first_name': user_data.info_utilisateur.first_name,
                        'last_name': user_data.info_utilisateur.last_name,
                        'avatar': user_data.avatar_utilisateur.url,
                        'level': user_parcours.nom,
                        'branch': user_parcours.id_filiere.nom,
                    }]
    stringfied_data = json.dumps(data)
    return JsonResponse(stringfied_data, safe = False)

## AJAX SEARCH RESULTS HANDLER VIEW
@login_required
def search_result_feeder(req):
    data = {'success': False}
    if req.method == 'POST':
        if req.is_ajax():
            search_entry = req.POST.get('search_entry')
            all_user_data = get_search_data(search_entry, req, 'search')
            if all_user_data:
                data = {'success': True, 'users_data': [],}
                for user_data in all_user_data:
                    user_group = Groupe.objects.filter(id = Etudiant.objects.filter(id_etudiant = user_data)[0].id_groupe.id)[0]
                    data['users_data'] += [{
                        'id': user_data.id_utilisateur,
                        'first_name': user_data.info_utilisateur.first_name,
                        'last_name': user_data.info_utilisateur.last_name,
                        'avatar': user_data.avatar_utilisateur.url,
                        'level': user_group.id_section.id_specialite.id_parcours.nom,
                        'branch': user_group.id_section.id_specialite.id_parcours.id_filiere.nom,
                        'group_num' : user_group.numero,
                        'section_num' : user_group.id_section.numero,
                        'speciality' : user_group.id_section.id_specialite.nom,
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
                if req.is_ajax():
                    return JsonResponse(json.dumps({'success':True}), safe = False) # else will return base template
            else:
                if req.is_ajax():
                    return JsonResponse(json.dumps({'success':False}), safe = False)
                else:
                    return render(req, 'gce_app/common/login.html', context = None)

        else:   
            if req.POST.get('logout'):
                logout(req)
                return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out

        return get_home_template(req)

    def get(self,req):
        if req.user.is_anonymous: # if user is not logged in return login page
            return render(req, 'gce_app/common/login.html', context = None)
        return get_home_template(req)


#### STUDENT PROFILE VIEW
class profileView(DetailView):
    model = Etudiant
    template_name = 'gce_app/etud/etud_profile.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loggedin_user = Utilisateur.objects.all().filter(info_utilisateur__in = [self.request.user])[0]
        context.update(get_user_data(loggedin_user))
        context.update(get_student_data(kwargs['object']))
        context.update(get_user_notifications(loggedin_user))
        context.update({'form': avatar_upload_form })
        return context

    def post(self, req, *args, **kwargs):
        form = avatar_upload_form(req.POST, req.FILES)
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        if form.is_valid(): ## changing user avatar
            try:
                user_acct = Utilisateur.objects.filter(info_utilisateur = req.user)[0]
                if user_acct.avatar_utilisateur.url[-18:] != 'default_avatar.png':
                    user_acct.avatar_utilisateur.delete(False)
                obj = form.save(commit=False)
                obj.info_utilisateur = req.user
                obj.type_utilisateur = Utilisateur.objects.filter(info_utilisateur = req.user)[0].type_utilisateur
                obj.id_utilisateur = Utilisateur.objects.filter(info_utilisateur = req.user)[0].id_utilisateur
                obj.save()
                data = {'success': True, 'new_avatar':obj.avatar_utilisateur.url}
            except:
                data = {'success': False}
            serialized_data = json.dumps(data)
            return JsonResponse(serialized_data, safe = False)
        return HttpResponse(req)


    def get (self,req,*args,**kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        profile_to_access = context['student'].id_etudiant
        logged_in_user_type = context['user_id'][:4]
        allowed_profiles = get_permitted_search_group(req, logged_in_user_type)
        if profile_to_access in allowed_profiles:
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")

#### ANNONCE VIEW 
class annonceView(TemplateView):
    template_name = 'gce_app/common/annonces.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user = Utilisateur.objects.filter(info_utilisateur = self.request.user)[0]
        context.update(get_user_data(logged_in_user))
        context.update(get_user_notifications(logged_in_user))
        context['annonces'] = get_user_annonce(self.request, logged_in_user.type_utilisateur)
        if logged_in_user.type_utilisateur == 'chef':
            context['modules'] = Module.objects.all().filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = logged_in_user)[0]))))
        return context

    def post(self, req, *args, **kwargs):
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        if req.is_ajax():
            req_type = req.POST.get('type');
            if req_type == 'delete':
                try:
                    Annonce.objects.filter(id = req.POST.get('annonce_id'))[0].delete()
                    data = {'success': True}
                except:
                    data = {'success': False}
                serialized_data = json.dumps(data)
                return JsonResponse(serialized_data, safe = False)
            if req_type == 'create':
                try:
                    annonce = create_new_annonce(req)
                    data = {'success': True, 'annonce': {
                        'id': annonce.id,
                        'title': annonce.sujet_annonce,
                        'content': annonce.description_annonce,
                        'date': str(annonce.date_annonce),
                        'time': str(annonce.heure_annonce),
                        'show': annonce.afficher_annonce,
                        'module': annonce.id_module.titre_module,
                        'user_type': Utilisateur.objects.filter(info_utilisateur = req.user)[0].type_utilisateur,
                    }}
                except:
                    data = {'success': False}
                serialized_data = json.dumps(data)
                return JsonResponse(serialized_data, safe = False)
            if req_type == 'show_hide':
                try:
                    annonce_to_change = Annonce.objects.filter(id = req.POST.get('annonce_id'))[0]
                    if annonce_to_change.afficher_annonce == False:
                        annonce_to_change.afficher_annonce = True
                        annonce_to_change.save()
                        data = {'success': True, 'hideCross': True}
                    else:
                        annonce_to_change.afficher_annonce = False
                        annonce_to_change.save()
                        data = {'success': True, 'hideCross': False}
                except:
                    data = {'success': False}
                serialized_data = json.dumps(data)
                return JsonResponse(serialized_data, safe = False)
        return HttpResponse(req)

    def get(self, req, *args, **kwargs):
        logged_in_user = Utilisateur.objects.filter(info_utilisateur = req.user)[0]
        if logged_in_user.type_utilisateur != 'tech':
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")        


class saisirView(TemplateView):
    template_name = 'gce_app/tech/tech_saisir.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_user = Utilisateur.objects.filter(info_utilisateur = self.request.user)[0]
        context.update(get_user_data(logged_in_user))
        context.update(get_user_notifications(logged_in_user))
        context['modules'] = Module.objects.filter(Q(id_specialite__in = Specialite.objects.filter(id__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_domaine__in = Domaine.objects.filter(id_faculte = Technicien.objects.filter(Q(id_technicien = logged_in_user))[0].id_faculte)))))) & Q(finsaisie_module = False))
        return context

    def post(self, req, *args, **kwargs):
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        if req.is_ajax():
            pass; 
        return HttpResponse(req)

    def get(self, req, *args, **kwargs):
        logged_in_user = Utilisateur.objects.filter(info_utilisateur = req.user)[0]
        if logged_in_user.type_utilisateur == 'tech':
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")

## ajax copies entries
def get_unfinished_saisir_entries(req):
    if req.method == 'POST':
        if req.is_ajax():
            module_name = req.POST.get('module_name')
            context = get_saisir_entries(module_name)
            data = render_to_string('gce_app/tech/unfinished_entries.html', context = context)
            return HttpResponse(data)