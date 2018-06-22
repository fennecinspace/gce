## page rendering and views modules
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin
## authentification modules
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
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
from gce_app.forms import avatar_upload_form, copies_file_upload_form, correction_file_upload_form, rect_file_upload_form
## extra 
from django.conf import settings
from datetime import datetime
import os


### Notify User - Create Notification  
def create_notification(user, title, content, type):
    if type == "save":
        icon = 'images/notifications/save_notification.svg'
    if type == "mail":
        icon = 'images/notifications/email_notification.svg'

    notif = Notification (
        sujet_notification = title,
        description_notification = content,
        icon_notification = icon,
        id_utilisateur = user
    )
    notif.save()


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
    allNotifications = Notification.objects.filter(Q(id_utilisateur__in = [u_obj]) & Q(vue_notification = False)).order_by('-id')
    return {'notifications_list': allNotifications,}


## chages user avatar
def change_user_avatar(req, form):
    user_acct = Utilisateur.objects.filter(info_utilisateur = req.user)[0]
    if user_acct.avatar_utilisateur.url[-18:] != 'default_avatar.png':
        user_acct.avatar_utilisateur.delete(False)
    obj = form.save(commit=False)
    obj.info_utilisateur = req.user
    obj.type_utilisateur = Utilisateur.objects.filter(info_utilisateur = req.user)[0].type_utilisateur
    obj.id_utilisateur = Utilisateur.objects.filter(info_utilisateur = req.user)[0].id_utilisateur
    obj.save()
    return obj


## returns student data
def get_final_versions(all_copies, for_rect = False): # do for rect default false to make student not see new version until copy in uploaded and ensg see version only in reclamations and not in notes
    if for_rect:
        all_versions = [list(VersionCopie.objects.filter(id_copie = copie).order_by('-id')) for copie in all_copies]
    else:
        all_versions = [list(VersionCopie.objects.filter(Q(id_copie = copie) & Q(temp_version = False)).order_by('-id')) for copie in all_copies]
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
    teachers = Enseignant.objects.filter(modules__in = modules).distinct()
    notes = get_student_notes(student) # gettings final versions of copies categorized by school year
    marks = {k: notes[k] for k in sorted(notes,reverse=True)} # sorting from newest school year to oldest
    return {
        'modules': modules,
        'teachers': teachers,
        'marks': marks,
    }


def get_technicien_data(technicien):
    return {
        'modules': Module.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_domaine__in = Domaine.objects.filter(id_faculte = technicien.id_faculte))))),
    }

def get_teacher_data(teacher):
    return {
        'chefs': ChefDepartement.objects.filter(id_chef_departement__in = Utilisateur.objects.filter(id_utilisateur__in =  teacher.filieres.all().values_list('id_chef_departement',flat = True))),
    }

def get_chef_data(chef):
    return {
        'filiere': Filiere.objects.filter(id_chef_departement = chef)[0],
        'modules': Module.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere = Filiere.objects.filter(id_chef_departement = chef)[0]))),
        'teachers': Enseignant.objects.filter(filieres__in = [Filiere.objects.filter(id_chef_departement = chef)[0]]),
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
    search_entry = re.sub(r'[^a-zA-Z0-9 ]', '', search_entry) # stripping entry from non latin letters
    search_entry = re.sub(r' +', ' ', search_entry) # turning multiple whitespaces to one
    user_type = Utilisateur.objects.filter(info_utilisateur = req.user)[0].type_utilisateur
    all_Students = get_permitted_search_group(req, user_type)

    ## searching by id
    if re.match('etud[0-9]+$',search_entry) is not None:
        for user in all_Students:
            if user.id_utilisateur == search_entry:
                return [user]

    # first try : trying to march based similarity ratio between the first and last names and the search entry
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
        etud_modules = Module.objects.filter(id_specialite = Specialite.objects.filter(id = (Section.objects.filter(id = Groupe.objects.filter(id = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].id_groupe.id)[0].id_section.id)[0].id_specialite.id))[0])
        etud_parcours = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].id_groupe.id_section.id_specialite.id_parcours
        etud_filiere = etud_parcours.id_filiere
        annonces = Annonce.objects.filter(Q(Q(id_module__in = etud_modules) | Q(id_parcours = etud_parcours) | Q(id_filiere = etud_filiere)) & Q(afficher_annonce = True)).distinct().order_by('-id')
        print(annonces)
    elif user_type == 'ensg':
        ensg_filieres = Enseignant.objects.filter(id_enseignant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].filieres.all()
        ensg_parcours = Parcours.objects.filter(id_filiere__in = ensg_filieres)
        ensg_modules = Enseignant.objects.filter(id_enseignant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0].modules.all()
        annonces = Annonce.objects.filter(Q(Q(id_module__in = ensg_modules ) | Q(id_parcours__in = ensg_parcours ) | Q(id_filiere__in = ensg_filieres )) & Q(afficher_annonce = True)).distinct().order_by('-id')
    elif user_type == 'chef':
        chef_filiere = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0])[0]
        chef_parcours = Parcours.objects.filter(id_filiere = chef_filiere)
        chef_modules = Module.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0])[0])))
        annonces = Annonce.objects.filter(Q(id_module__in = chef_modules) | Q(id_parcours__in = chef_parcours) | Q(id_filiere = chef_filiere)).distinct().order_by('-id')
    return annonces

def create_new_annonce(req):
    title_annonce = req.POST.get('title')
    content_annonce = req.POST.get('content')
    date_annonce = datetime.now().date()
    time_annonce = datetime.now().time()
    show_annonce = json.loads(req.POST.get('show'))
    data = json.loads(req.POST.get('create_group'))
    data_type = data['type']
    data_list = data['data']
    annonce = Annonce(sujet_annonce = title_annonce, description_annonce = content_annonce, date_annonce = date_annonce, heure_annonce = time_annonce, afficher_annonce = show_annonce)
    if data_type == 'filiere':
            annonce.id_filiere = Filiere.objects.filter(id = data_list[0])[0]
            annonce.save()
    if data_type == 'parcours':
        annonce.save()
        for elem in data_list:
            print('here')
            annonce.id_parcours.add(Parcours.objects.filter(id = elem)[0])
    if data_type == 'module':
        annonce.save()
        for elem in data_list:
            annonce.id_module.add(Module.objects.filter(id = elem)[0])
    # annonce_info = {
    #     'annonce': {
    #         'id': annonce.id,
    #         'title': annonce.sujet_annonce,
    #         'content': annonce.description_annonce,
    #         'date': str(annonce.date_annonce),
    #         'time': str(annonce.heure_annonce),
    #         'show': annonce.afficher_annonce,
    #         'user_type': Utilisateur.objects.filter(info_utilisateur = req.user)[0].type_utilisateur,
    #     }    
    # }
    # print('helo')
    # if annonce.id_filiere:
    #     annonce_info['filiere'] = annonce.id_filiere.nom;
    # elif annonce.id_parcours:
    #     annonce_info['parcours'] = []
    #     for parcours in annonce.id_parcours.all():
    #         annonce_info['parcours'] += [parcours.nom];
    # elif annonce.id_module:
    #     annonce_info['module'] = []
    #     for module in annonce.id_module.all():
    #         annonce_info['module'] += [module.titre_module];

    # return annonce_info

## returns the template based on the signed in user's type
def get_home_template(req):
    if req.user.is_superuser or req.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    loggedin_user = Utilisateur.objects.all().filter(info_utilisateur__in = [req.user])[0]
    user_data = get_user_data(loggedin_user)
    notifications = get_user_notifications(loggedin_user)
    data = user_data
    data.update(notifications) ##merging the 2 dicts in one
    return render(req, 'gce_app/common/home.html', context = data)


## returns entries not yet subbmited
def get_copy_entries(module_title, fin_saisie = False):
    all_copies = Copie.objects.filter(Q(id_module__in = Module.objects.filter(Q(titre_module = module_title) & Q(finsaisie_module = fin_saisie))) & Q(annee_copie = ANNEE_UNIV) ).order_by('id')
    final_versions = get_final_versions(all_copies)
    return {'entries': get_version_entries(final_versions)}
    

## returns list contains lists of files for lists of versions
def get_version_entries(versions):
    entries = []
    for version in versions:
        entries = [list(FichierCopie.objects.filter(id_version = version).order_by('id'))] + entries 
    return entries

## return students for saisir datalist
def get_saisir_students(module_name, have_copies = True):
    all_students_assisting = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite = Module.objects.filter(titre_module = module_name)[0].id_specialite)))

    if not have_copies:
        return {'assigned_students' : all_students_assisting}
    else:
        return {'unassigned_students' : all_students_assisting}

## deletes entries
def delete_saisir_entry(req):
    data_to_delete = json.loads(req.POST.get('data_to_delete'))
    if req.POST.get('delete_type') == 'copy':
        for id_to_delete in data_to_delete:
            VersionCopie.objects.filter(id = id_to_delete)[0].id_copie.delete()
    if req.POST.get('delete_type') == 'file':
        for id_to_delete in data_to_delete:
            file_to_delete = FichierCopie.objects.filter(id = id_to_delete)[0]
            file_to_delete.emplacement_fichier.delete()
            file_to_delete.delete()
    if req.POST.get('delete_type') == 'both':
        data_to_delete = json.loads(data_to_delete)
        if 'copies' in data_to_delete:
            for id_to_delete in data_to_delete['copies']:
                VersionCopie.objects.filter(id = id_to_delete)[0].id_copie.delete()
        if 'files' in data_to_delete:
            for id_to_delete in data_to_delete['files']:
                file_to_delete = FichierCopie.objects.filter(id = id_to_delete)[0]
                file_to_delete.emplacement_fichier.delete()
                file_to_delete.delete()


## creating copie entries
def create_new_copie_files(req,module_name): ## gets all uploaded files and saves them one by
    files = req.FILES.getlist('emplacement_fichier')
    for file_to_save in files:
        req.FILES['emplacement_fichier'] = file_to_save
        form = copies_file_upload_form(req.POST, req.FILES)
        if form.is_valid():
            obj = form.save(commit= False)
            obj.id_module = Module.objects.filter(titre_module = module_name)[0]
            obj.save()


## create new copie entry
def create_new_copie_entry(module_name, student_id, files_ids):
    try:
        #create Copie
        gen_module = Module.objects.filter(titre_module = module_name)[0]
        gen_etudiant = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.filter(id_utilisateur = student_id)[0])[0]
        copie = Copie(annee_copie = ANNEE_UNIV, id_module = gen_module, id_etudiant = gen_etudiant)
        copie.save()
       
        #create first version     
        version = VersionCopie(numero_version = 1, id_copie = copie)
        version.save()

        #asigning files
        for file_id in files_ids:
            file_to_asign = FichierCopie.objects.filter(id = file_id)[0]
            file_to_asign.id_version = version
            file_to_asign.save()
        
        return {
            'student_id': student_id,
            'version_id': version.id,
            'version_note': '',
        }

    except Exception as e:
        print(e)
        copie.delete()

### save button backend
def save_saisir_data(req, module_name):
    data = json.loads(req.POST.get('data'))
    completed = data['completed']
    uncompleted = data['uncompleted']
    new_completed = [] ## will be used for the copie + file grouping

    if completed:
        ######## grouping copies with same name ########
        similar_elems = {} # used for copie + copie grouping
        for i in range(len(completed)):
            tmp = completed[:i] + completed[i+1:]
            for tmp_entry in tmp:
                if completed[i]['student_id'] == tmp_entry['student_id']:
                    if completed[i]['student_id'] in similar_elems:
                        similar_elems[completed[i]['student_id']] += [completed[i]['version_id']]
                    else:
                        similar_elems[completed[i]['student_id']] = [completed[i]['version_id']]


        # leaving only normal copies in completed (removing entries about to be grouped)
        for i in range(len(completed)): 
            if completed[i]['student_id'] not in similar_elems:
                new_completed += [completed[i]]
        

        # creating new grouped copies and deleting seperate copies
        for student_id, versions in similar_elems.items():
            versions_objs = VersionCopie.objects.filter(id__in = versions)
            files_to_group = list(FichierCopie.objects.filter(id_version__in = versions_objs).values_list('id',flat = True)) # getting files of the copies to groupe
            Copie.objects.filter(id__in = versions_objs.values_list("id_copie", flat = True)).delete() #deleting copies to be grouped
            ## creating copy and adding it for the case where we have copie +copie + file 
            new_completed += [create_new_copie_entry(module_name, student_id, files_to_group)]
            

        ######## changing info for normal copies ########
        for entry in new_completed:
            try:
                # modifying student note
                version_to_modify = VersionCopie.objects.filter(id = entry['version_id'])[0]
                old_note = version_to_modify.note_version
                if (entry['version_note'] != ""):
                    if float(entry['version_note']) >= 0 and float(entry['version_note']) <= 20:
                        version_to_modify.note_version = float(entry['version_note'])
                else:
                    version_to_modify.note_version = None
                version_to_modify.save()
                
                # modifying student name
                copy_to_modify = version_to_modify.id_copie
                old_student = copy_to_modify.id_etudiant
                copy_to_modify.id_etudiant = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.filter(id_utilisateur = entry['student_id'])[0])[0]
                copy_to_modify.save()

            except Exception as e:
                print(e)
                # restoring data
                version_to_modify.note_version = old_note
                version_to_modify.save()
                copy_to_modify.id_etudiant = old_student
                copy_to_modify.save()

    if uncompleted:
        ######## grouping normal files by student id ########
        entries = {}
        for entry in uncompleted:
            if entry['student_id'] in entries:
                entries[entry['student_id']] += [ entry['file_id']]
            else:
                entries.update({ entry['student_id'] : [entry['file_id']]})
        
        if new_completed:
            ######## mergin files with copies of student ids who already have one ########
            for entry in new_completed:
                if entry['student_id'] in entries:
                    for file_id in entries[entry['student_id']]:
                        file_to_asign = FichierCopie.objects.filter(id = file_id)[0]
                        file_to_asign.id_version = VersionCopie.objects.filter(id = entry['version_id'])[0]
                        file_to_asign.save()
                    del entries[entry['student_id']]
        
        ######## creating a copy per student id ########
        for student_id, files_ids in entries.items():
            create_new_copie_entry(module_name, student_id, files_ids)


def submit_saisir_data(req, module_name):
    data = json.loads(req.POST.get('data'))
    completed = data['completed']
    version_ids = []
    for entry in completed:
        version_ids += [entry['version_id']]
    entries_to_check = VersionCopie.objects.filter(id__in = version_ids)
    for saved in entries_to_check:
        if saved.note_version == None:
            return 'copies not saved'
    all_students_assisting = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite = Module.objects.filter(titre_module = module_name)[0].id_specialite)))
    module_to_submit = Module.objects.filter(titre_module = module_name)[0]
    module_to_submit.finsaisie_module = True
    module_to_submit.save() ## will not be able to see module in saisir after this !



def get_saisir_stats(context):
    noted = 0
    if context['entries']:
        for entry in context['entries']:
            if len(entry) > 0 and entry[0].id_version.note_version:
                noted += 1
    return {
        'Fichiers': len(context['new_files']),
        'Copies': len(context['entries']),
        'Copies Notés': noted,
    }


## creating correction 
def create_module_correction(req,module_name): ## gets all uploaded files and saves them one by
    try:
        # create correction
        user_obj = Enseignant.objects.filter(id_enseignant = Utilisateur.objects.filter(info_utilisateur = req.user)[0])[0]
        module_obj = Module.objects.filter(titre_module = module_name)[0]
        correction_obj = Correction(id_module = module_obj, id_enseignant = user_obj, annee_correction = ANNEE_UNIV)
        correction_obj.save()

        # attach uploaded files
        files = req.FILES.getlist('emplacement_fichier')
        for file_to_save in files:
            req.FILES['emplacement_fichier'] = file_to_save
            form = correction_file_upload_form(req.POST, req.FILES)
            if form.is_valid():
                obj = form.save(commit= False)
                obj.id_module = Module.objects.filter(titre_module = module_name)[0]
                obj.id_correction = correction_obj
                obj.save()
    except Exception as e:
        print(e)
        correction_obj.delete()

def delete_module_correction(req):
    correction_to_delete = Correction.objects.filter(id = req.POST.get('data_to_delete'))[0]
    correction_files = FichierCorrection.objects.filter(id_correction = correction_to_delete)
    for file in correction_files:
        file.emplacement_fichier.delete()
    correction_to_delete.delete()

def get_module_correction(module_name):
    module_obj = Module.objects.filter(titre_module = module_name)[0]
    corrections = Correction.objects.filter(Q(id_module = module_obj) & Q(annee_correction = ANNEE_UNIV)).order_by('-id')
    if (len(corrections) > 0):
        return FichierCorrection.objects.filter(id_correction = corrections[0].id)

def check_if_modifiable(all_notes):
    nb_of_modifibale = 0
    for entry in all_notes:
        if entry[0].id_version.id_copie.modifiable == True:
            nb_of_modifibale += 1

    if len(all_notes) == nb_of_modifibale:
        return True;
    else: 
        return False;

def save_notes_module(req, module_name):
    data = json.loads(req.POST.get('data_to_send'))
    if data:
        for entry in data:
            try:
                if float(entry['mark']) >= 0 and float(entry['mark']) <= 20:
                    version_to_modify = VersionCopie.objects.filter(id = entry['version_id'])[0]
                    old_note = version_to_modify.note_version
                    version_to_modify.note_version = float(entry['mark'])
                    version_to_modify.save()
            except Exception as e:
                print(e)
                version_to_modify.note_version = old_note
                version_to_modify.save()

def submit_notes_module(req, module_name):
    correction = json.loads(req.POST.get('correction'))
    if correction:
        all_copy_files = get_copy_entries(module_name, True)['entries']
        for files in all_copy_files:
            try:
                files[0].id_version.id_copie.modifiable = False
                files[0].id_version.id_copie.save()
            except Exception as e:
                print(e)
                files[0].id_version.id_copie.modifiable = True
                files[0].id_version.id_copie.save()


def get_affichable_modules(logged_in_user):
    ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
    all_user_modules = Module.objects.filter(Q(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = logged_in_user)[0])))) & Q(finsaisie_module = True))
    affichable_modules = []
    for module in all_user_modules:
        module_copies = Copie.objects.filter(Q(id_module = module) & Q(annee_copie = ANNEE_UNIV) & Q(afficher_copie = False))
        module_final_copies = Copie.objects.filter(Q(id_module = module) & Q(annee_copie = ANNEE_UNIV) & Q(modifiable = False))
        if len(module_final_copies) == len(module_copies) and len(module_copies) > 0: ## use != to get copies done in tech but still awaiting aproval from ensg
            affichable_modules += [module]

    return affichable_modules


def get_ensg_reclamations(ensg):
    ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
    user_modules = Enseignant.objects.filter(id_enseignant = ensg)[0].modules.all()
    reclamations_done = Reclamation.objects.filter(Q(annee_reclamation = ANNEE_UNIV) & Q(id_module__in = user_modules) & Q(regler_reclamation = True)).order_by('-id')
    reclamations_waiting = Reclamation.objects.filter(Q(annee_reclamation = ANNEE_UNIV) & Q(id_module__in = user_modules) & Q(regler_reclamation = False)).order_by('id')

    return {
        'entries_waiting': reclamations_waiting,
        'entries_done': reclamations_done,
    }


#######################################################
###################### VIEWS ##########################
#######################################################
## AJAX RECLAMATION ENSG HANDLER 
@login_required
def ensg_reclamation_handler(req):
    ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
    if req.method == 'POST' and req.is_ajax():
        try:
            reclamation = Reclamation.objects.filter(id = req.POST.get('reclam_id'))[0]
            copie_to_modify = Copie.objects.filter(id = req.POST.get('copie_id'))[0]
            old_version = get_final_versions([copie_to_modify])[0]

            if req.POST.get('type') == 'accept':
                reclamation.approuver_reclamation = True
                
                new_version = VersionCopie(numero_version = old_version.numero_version + 1, note_version = float(req.POST.get('note')), id_copie = copie_to_modify, temp_version = True)
                new_version.save()
                filler_file = FichierCopie(id_version = new_version, id_module = reclamation.id_module, emplacement_fichier = "default/file_filler.png")
                filler_file.save()
                copie_to_modify.rectifier = True
                copie_to_modify.save()
                reclamation.new_files.add(filler_file)
                
            if req.POST.get('type') == 'refuse':
                reclamation.approuver_reclamation = False
            
            reclamation.regler_reclamation = True
            reclamation.save()
            data = {'success': True}

        except Exception as e:
            print(e)
            data = {'success': False}
            
    stringfied_data = json.dumps(data)
    return JsonResponse(stringfied_data, safe = False)     



## AJAX RECLAMATION STUDENT HANDLER 
@login_required
def etud_reclamation_handler(req):
    ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]

    if req.method == 'POST' and req.is_ajax():
        try:
            if req.POST.get('type') == 'create':
                module = Module.objects.filter(id = req.POST.get('module_id'))[0]
                student = Etudiant.objects.filter(id_etudiant = Utilisateur.objects.filter(id_utilisateur = req.POST.get('student_id'))[0])[0]
                nb_unprocessed_reclams = len(Reclamation.objects.filter(Q(id_etudiant = student) & Q(id_module = module) & Q(regler_reclamation = False)))
                current_version = VersionCopie.objects.filter(id = req.POST.get('version_id'))[0]
                if nb_unprocessed_reclams == 0:
                    sujet = req.POST.get('title')
                    content = req.POST.get('content')
                    new_reclamation = Reclamation(sujet_reclamation = sujet, description_reclamation = content, id_etudiant = student, id_module = module, annee_reclamation = ANNEE_UNIV)
                    new_reclamation.save()
                    new_reclamation.old_files.add(*list(FichierCopie.objects.filter(id_version = current_version)))
                    context_to_use = {'entry': {
                        'reclamations': [new_reclamation],
                        'year':{'active':True},
                    }}
                    html_to_use = render_to_string('gce_app/etud/reclam_content.html', context = context_to_use)
                else:
                    return JsonResponse(json.dumps({'success': True, 'error' : True}), safe = False)  
            
            if req.POST.get('type') == 'delete':
                Reclamation.objects.filter(id = req.POST.get('reclam_id')).delete()
                html_to_use = render_to_string('gce_app/etud/reclam_form.html', context = None)
            
            data = {'success': True, 'html': html_to_use}
        
        except Exception as e:
            print(e)
            data = {'success': False}
            
    stringfied_data = json.dumps(data)
    return JsonResponse(stringfied_data, safe = False)        



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

#### Main View

class BaseContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loggedin_user'] = Utilisateur.objects.all().filter(info_utilisateur__in = [self.request.user])[0]
        context.update(get_user_data(context['loggedin_user']))
        context.update(get_user_notifications(context['loggedin_user']))
        return context
    
class MainView(TemplateView):
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


#### PROFILES VIEWS
class ProfileView(DetailView, BaseContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs['profile'] == 'etud':
            context.update(get_student_data(kwargs['object']))
        if kwargs['profile'] == 'tech':
            context['allowed_types'] = ['chef','tech']
            context.update(get_technicien_data(kwargs['object']))
        if kwargs['profile'] == 'ensg':
            context['allowed_types'] = ['chef','ensg']
            context.update(get_teacher_data(kwargs['object']))
        if kwargs['profile'] == 'chef':
            context['allowed_types'] = ['chef']
            context.update(get_chef_data(kwargs['object']))
        context.update({'form': avatar_upload_form })
        return context

    def post(self, req, *args, **kwargs):
        form = avatar_upload_form(req.POST, req.FILES)
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        if form.is_valid(): ## changing user avatar
            try:
                obj = change_user_avatar(req, form)
                data = {'success': True, 'new_avatar':obj.avatar_utilisateur.url}
            except Exception as e:
                print(e)
                data = {'success': False}
            serialized_data = json.dumps(data)
            return JsonResponse(serialized_data, safe = False)
        return HttpResponse(req)


    def get (self,req,*args,**kwargs):
        ## etudiant profile
        if kwargs['profile'] == 'etud':
            self.model = Etudiant
            self.template_name = 'gce_app/etud/etud_profile.html'
            self.context_object_name = 'student'
            self.object = self.get_object() 
            context = self.get_context_data(object=self.object,**kwargs)
            profile_to_access = context['student'].id_etudiant
            logged_in_user_type = context['loggedin_user'].type_utilisateur
            allowed_profiles = get_permitted_search_group(req, logged_in_user_type)
            if profile_to_access in allowed_profiles:
                return self.render_to_response(context)
            else:
                return HttpResponse("<h2>404</h2>")
        
        ## other users profiles
        if kwargs['profile'] == 'tech':
            self.model = Technicien
            self.template_name = 'gce_app/tech/tech_profile.html'
            self.context_object_name = 'technicien'
        if kwargs['profile'] == 'ensg':
            self.model = Enseignant
            self.template_name = 'gce_app/ensg/ensg_profile.html'
            self.context_object_name = 'teacher'
        if kwargs['profile'] == 'chef':
            self.model = ChefDepartement
            self.template_name = 'gce_app/chef/chef_profile.html'
            self.context_object_name = 'chef'

        self.object = self.get_object() 
        context = self.get_context_data(object=self.object,**kwargs)
        if context['loggedin_user'].type_utilisateur in context['allowed_types']:
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")


#### SHARED : ANNONCE VIEW 
class AnnonceView(TemplateView, BaseContextMixin):
    template_name = 'gce_app/common/annonces.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annonces'] = get_user_annonce(self.request, context['loggedin_user'].type_utilisateur)
        if context['loggedin_user'].type_utilisateur == 'chef':
            context['modules'] = Module.objects.all().filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = context['loggedin_user'])[0]))))
            context['filiere'] = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = context['loggedin_user'])[0])[0]
            context['parcours'] = Parcours.objects.filter(id_filiere = context['filiere'])
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
                except Exception as e:
                    print(e)
                    data = {'success': False}
                serialized_data = json.dumps(data)
                return JsonResponse(serialized_data, safe = False)
            if req_type == 'create':
                try:
                    # annonce_info = create_new_annonce(req)
                    create_new_annonce(req)
                    data = {'success': True}
                    # data.update(annonce_info)
                except Exception as e:
                    print(e)
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
                except Exception as e:
                    print(e)
                    data = {'success': False}
                serialized_data = json.dumps(data)
                return JsonResponse(serialized_data, safe = False)
        return HttpResponse(req)

    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur in ['etud','ensg','chef']:
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")        


### TECH : SAISIR VIEW
class SaisirView(TemplateView, BaseContextMixin):
    template_name = 'gce_app/tech/tech_saisir.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = Module.objects.filter(Q(id_specialite__in = Specialite.objects.filter(id__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_domaine__in = Domaine.objects.filter(id_faculte = Technicien.objects.filter(Q(id_technicien = context['loggedin_user']))[0].id_faculte)))))) & Q(finsaisie_module = False))
        context['upload_form'] = copies_file_upload_form
        return context

    def post(self, req, *args, **kwargs):
        global ANNEE_UNIV
        ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        if req.is_ajax():
            try:
                module_name = req.POST.get('module_name')
                if req.POST.get('type') == 'upload':
                    create_new_copie_files(req, module_name)
                if req.POST.get('type') == 'delete':
                    delete_saisir_entry(req)
                if req.POST.get('type') == 'save':
                    save_saisir_data(req, module_name)
                if req.POST.get('type') == 'submit':
                    res = submit_saisir_data(req, module_name)
                    if res == 'copies not saved': ## in case a copîe doesn't have a saved note
                        return JsonResponse(json.dumps({ 'success': False, 'error' : 'Sauvgarder avant d\'envoyer !'}), safe = False)      

                context = get_copy_entries(module_name, False)
                context.update(get_saisir_students(module_name, True))
                context.update(get_saisir_students(module_name, False))
               
                ## get new files not yet asigned
                context['new_files'] = FichierCopie.objects.filter(Q(id_version = None) & Q(id_module = Module.objects.filter(titre_module = module_name)[0])).order_by('-id')
                context['stats'] = get_saisir_stats(context)
                
                html = render_to_string('gce_app/tech/unfinished_entries.html', context = context)
                data = {'success': True, 'html': html, 'type': req.POST.get('type')}
            
            except Exception as e:
                print(e)
                data = {'success': False}
            
            serialized_data = json.dumps(data)
            return JsonResponse(serialized_data, safe = False)     
        return HttpResponse(req)

    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur == 'tech':
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")



## ENSG : NOTES VIEW
class NotesView(TemplateView, BaseContextMixin):
    
    def get_context_data(self, **kwargs):
        global ANNEE_UNIV 
        ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
        context = super().get_context_data(**kwargs)
        
        if context['loggedin_user'].type_utilisateur == 'ensg':
            context['modules'] = []
            user_modules = Enseignant.objects.filter(id_enseignant = context['loggedin_user'])[0].modules.filter(finsaisie_module = True)
            
            for module in user_modules:
                if len(Copie.objects.filter(Q(id_module = module) & Q(annee_copie = ANNEE_UNIV))) > 0:
                    context['modules'] += [module]

            context['upload_form'] = correction_file_upload_form
        
        elif context['loggedin_user'].type_utilisateur == 'etud':
            student = Etudiant.objects.filter(id_etudiant = context['loggedin_user'])[0]
            notes = get_student_notes(student) # gettings final versions of copies categorized by school year
            marks = {k: notes[k] for k in sorted(notes,reverse=True)} # sorting from newest school year to oldest
            results = {}
            
            for year, versions in marks.items():
                modules_data = []
                for version in versions:
                    copy_files = FichierCopie.objects.filter(id_version = version)
                    module_correction = Correction.objects.filter(Q(annee_correction = year) & Q(id_module = version.id_copie.id_module))[0]
                    module_reclamation = Reclamation.objects.filter(Q(id_etudiant = student) & Q(id_module = version.id_copie.id_module)).order_by('-id')
                    nb_unprocessed_reclams = len(Reclamation.objects.filter(Q(id_etudiant = student) & Q(id_module = version.id_copie.id_module) & Q(regler_reclamation = False) ))
                    # if len(module_reclamation) <= 0:
                    #     module_reclamation = module_reclamation
                    # else:
                    #     module_reclamation = None
                    modules_data += [{
                        'files':list(copy_files),
                        'correction': list(FichierCorrection.objects.filter(id_correction = module_correction).order_by('-id')),
                        'reclamations': module_reclamation,
                        'nb_unprocessed_reclams': nb_unprocessed_reclams,
                    }]
                results[year] = modules_data
            context['results'] = results
            
            ## checking if unupdated copies with updated notes exist
            copies = Copie.objects.filter(id_etudiant = student)
            copy_files = get_final_versions(copies)
            all_copy_files = get_final_versions(copies, True)
            if all_copy_files == copy_files:
                context['exists_unupdated_copies'] = True
            else:
                context['exists_unupdated_copies'] = False
        
        return context

    def post(self, req, *args, **kwargs):
        ## added order by -id to fix stupid admin fault in case he/she leaves 2 active years /last entry created will be taken
        global ANNEE_UNIV 
        ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
        
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        
        if req.is_ajax():
            try:
                module_name = req.POST.get('module_name')
                if req.POST.get('type') == 'upload':
                    create_module_correction(req, module_name)
                if req.POST.get('type') == 'delete':
                    delete_module_correction(req)
                if req.POST.get('type') == 'save':
                    save_notes_module(req, module_name)
                if req.POST.get('type') == 'submit':
                    submit_notes_module(req, module_name)
                if req.POST.get('type') == 'access_right':
                    demande_access_right_ensg_notes(module_name)
                context = get_copy_entries(module_name, True)
                context['correction'] = get_module_correction(module_name)
                context['modifiable_enabled'] = check_if_modifiable(context['entries'])
                context['can_ask_for_right'] = get_can_ask_for_right(context['entries'])
                html = render_to_string('gce_app/ensg/module_notes.html', context = context)
                data = {'success': True, 'html': html, 'type': req.POST.get('type')}
            except Exception as e:
                print(e)
                data = {'success': False}
            serialized_data = json.dumps(data)
            return JsonResponse(serialized_data, safe = False) 
        return HttpResponse(req)


    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur == 'ensg':
            self.template_name = 'gce_app/ensg/ensg_notes.html'
        elif context['loggedin_user'].type_utilisateur == 'etud':
            self.template_name = 'gce_app/etud/etud_notes.html'
        else:
            return HttpResponse("<h2>404</h2>")
        return self.render_to_response(context)

def demande_access_right_ensg_notes(module_name):
    create_notification (
        user = Module.objects.filter(titre_module = module_name)[0].id_specialite.id_parcours.id_filiere.id_chef_departement.id_chef_departement,
        title = 'Demande de Droit de Modification',
        content = 'l\'enseignant du module ' + module_name +' demande le droit de modification avant l\'affichage', 
        type = "save"
    )


def get_can_ask_for_right(versions):
    for files in versions:
        for file in files:
            if file.id_version.id_copie.afficher_copie == True:
                return False
    return True
    

class AffichageView(TemplateView, BaseContextMixin):
    template_name = 'gce_app/chef/chef_affichage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = get_affichable_modules(context['loggedin_user'])
        return context

    def post(self, req, *args, **kwargs):
        global ANNEE_UNIV
        ANNEE_UNIV = AnneeUniv.objects.filter(active = True).order_by('-id')[0]
        
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        
        if req.is_ajax():
            try:
                module = Module.objects.filter(id = req.POST.get('data'))[0]
                module_copies = Copie.objects.filter(Q(id_module = module) & Q(annee_copie = ANNEE_UNIV))
                if req.POST.get('type') == 'show':
                    for copy in module_copies:
                        copy.afficher_copie = True
                        copy.save()
                if req.POST.get('type') == 'grant_access':
                    for copy in module_copies:
                        copy.modifiable = True
                        copy.save()
                data = {'success': True, 'module': module.titre_module}
            except Exception as e:
                print(e)
                data = {'success': False}
            serialized_data = json.dumps(data)
            return JsonResponse(serialized_data, safe = False) 
        return HttpResponse(req)


    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur == 'chef':
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")


class UsersView(TemplateView, BaseContextMixin):
    template_name = 'gce_app/chef/chef_personnels.html'

    def post(self, req, *args, **kwargs):
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        return HttpResponse(req)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filiere = Filiere.objects.filter(id_chef_departement = ChefDepartement.objects.filter(id_chef_departement = context['loggedin_user'])[0])[0]
        context['teachers'] = Utilisateur.objects.filter(id_utilisateur__in = Enseignant.objects.filter(filieres__in = [filiere]).values_list('id_enseignant', flat=True))
        context['students'] = Utilisateur.objects.filter(id_utilisateur__in = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere = filiere))))))
        return context

    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur == 'chef':
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")

class ReclamationView(TemplateView, BaseContextMixin):
    template_name = 'gce_app/ensg/ensg_reclam.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_ensg_reclamations(context['loggedin_user']))
        return context

    def post(self, req, *args, **kwargs):
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        return HttpResponse(req)

    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur == 'ensg':
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")


class RectificationsView(TemplateView, BaseContextMixin):
    template_name = 'gce_app/tech/tech_rect.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # getting allowed students
        faculte_tech = Technicien.objects.filter(id_technicien = context['loggedin_user'] )[0].id_faculte
        all_Students = Etudiant.objects.filter(id_groupe__in = Groupe.objects.filter(id_section__in = Section.objects.filter(id_specialite__in = Specialite.objects.filter(id_parcours__in = Parcours.objects.filter(id_filiere__in = Filiere.objects.filter(id_domaine__in = Domaine.objects.filter(id_faculte = faculte_tech)))))))
        # getting copies needed for rect
        copies_to_rect = Copie.objects.filter(Q(rectifier = True) & Q(id_etudiant__in = all_Students))
        final_versions = get_final_versions(copies_to_rect, True)
        context['entries'] = get_version_entries(final_versions)
        context['upload_form'] = rect_file_upload_form
        return context

    def post(self, req, *args, **kwargs):
        if self.request.POST.get('logout'):
            logout(req)
            return render(req, 'gce_app/common/login.html', context = None) # return login page after logging out
        
        if req.is_ajax():
            try:
                current_version = VersionCopie.objects.filter(id = req.POST.get('version_id'))[0]
                current_files = FichierCopie.objects.filter(id_version = current_version)
                reclamation = Reclamation.objects.filter(new_files__in = current_files)[0]

                if req.POST.get('type') == 'upload':
                    ## removing filler file
                    current_files.delete()
                    ## saving new files
                    files = req.FILES.getlist('emplacement_fichier')
                    accepted_files = []
                    for file_to_save in files:
                        req.FILES['emplacement_fichier'] = file_to_save
                        form = rect_file_upload_form(req.POST, req.FILES)
                        if form.is_valid():
                            obj = form.save(commit= False)
                            obj.id_module = Module.objects.filter(id = req.POST.get('module_id'))[0]
                            obj.id_version = current_version
                            obj.save()
                            accepted_files += [obj]
                    ## archiving new files in reclamation
                    reclamation.new_files.clear()
                    reclamation.new_files.add(*accepted_files)

                if req.POST.get('type') == 'reset':
                    ## removing temp files
                    for file in current_files:
                        if "default/" not in file.emplacement_fichier.url:
                            file.emplacement_fichier.delete()
                    current_files.delete()
                    ## creating filler file
                    filler_file = FichierCopie(id_version = current_version, id_module = current_version.id_copie.id_module, emplacement_fichier = "default/file_filler.png")
                    filler_file.save()
                    ## archiving new files in reclamation
                    reclamation.new_files.clear()
                    reclamation.new_files.add(filler_file)


                if req.POST.get('type') == 'accept':
                    current_version.temp_version = False
                    current_version.save()
                    current_version.id_copie.rectifier = False
                    current_version.id_copie.save()
                    
                data = {'success': True}
                
            except Exception as e:
                print(e)
                data = {'success': False}
            serialized_data = json.dumps(data)
            return JsonResponse(serialized_data, safe = False) 
        return HttpResponse(req)



    def get(self, req, *args, **kwargs):
        context = self.get_context_data()
        if context['loggedin_user'].type_utilisateur == 'tech':
            return self.render_to_response(context)
        else:
            return HttpResponse("<h2>404</h2>")

