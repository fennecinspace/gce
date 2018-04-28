from django.contrib import admin
from gce_app.models import *

# Register your models here.

class UniversiteAdmin(admin.ModelAdmin):
    list_display = ('nom')
admin.site.register(Universite)

class FaculteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_universite')
admin.site.register(Faculte)

class DomaineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_faculte')
admin.site.register(Domaine)

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user_choices', 'info_utilisateur' , 'type_utilisateur', 'id_utilisateur', 'avatar_utilisateur')
admin.site.register(Utilisateur)

class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_domaine', 'id_chef_departement')
admin.site.register(Filiere)

class ParcoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_filiere')
admin.site.register(Parcours)

class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_parcours')
admin.site.register(Specialite)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'id_specialite')
admin.site.register(Section)

class GroupeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'id_section')
admin.site.register(Groupe)

class ChefDepartementAdmin(admin.ModelAdmin):
    list_display = ('id_chef_departement')
admin.site.register(ChefDepartement)

class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('id_enseignant', 'filieres', 'modules')
admin.site.register(Enseignant)

class TechnicienAdmin(admin.ModelAdmin):
    list_display = ('id_technicien', 'id_faculte')
admin.site.register(Technicien)

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id_etudiant', 'id_groupe')
admin.site.register(Etudiant)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titre_module', 'finsaisie_module', 'id_specialite')
admin.site.register(Module)

class CorrectionAdmin(admin.ModelAdmin):
    list_display = ('id_module', 'id_enseignant', 'annee_correction')
admin.site.register(Correction)

class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('sujet_annonce', 'description_annonce', 'date_annonce', 'heure_annonce', 'afficher_annonce', 'id_module', 'id_parcours', 'id_filiere')
admin.site.register(Annonce)

class CopieAdmin(admin.ModelAdmin):
    list_display = ('annee_copie', 'afficher_copie', 'modifiable', 'id_module', 'id_etudiant')
admin.site.register(Copie)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sujet_notification', 'description_notification', 'vue_notification', 'date_notification', 'heure_notification', 'icon_notification', 'id_utilisateur')
admin.site.register(Notification)

class DiscussionAdministrativeAdmin(admin.ModelAdmin):
    list_display = ('id_chef_departement', 'id_enseignant')
admin.site.register(DiscussionAdministrative)

class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('sujet_reclamation', 'regler_reclamation', 'description_reclamation', 'id_etudiant', 'id_module')
admin.site.register(Reclamation)

class DiscussionReclamationAdmin(admin.ModelAdmin):
    list_display = ('id_reclamation', 'id_enseignant')
admin.site.register(DiscussionReclamation)

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('sale_consultation', 'date_consultation', 'heure_consultation', 'afficher_consultation', 'approve_consultation', 'id_enseignant', 'id_module')
admin.site.register(Consultation)

class MessagesAdministrativeAdmin(admin.ModelAdmin):
    list_display = ('contenu_message', 'date_message', 'heure_message', 'id_emetteur', 'id_recepteur', 'id_discussion')
admin.site.register(MessagesAdministrative)

class VersionCopieAdmin(admin.ModelAdmin):
    list_display = ('numero_version', 'note_version', 'id_copie')
admin.site.register(VersionCopie)

class FichierCopieAdmin(admin.ModelAdmin):
    list_display = ('emplacement_fichier', 'id_version', 'id_module')
admin.site.register(FichierCopie)

class FichierCorrectionAdmin(admin.ModelAdmin):
    list_display = ('emplacement_fichier', 'id_correction')
admin.site.register(FichierCorrection)

class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('annee_scolaire', 'active')
admin.site.register(AnneeScolaire, AnneeScolaireAdmin)

#admin.site.register(Appartientfiliere)
# admin.site.register(Appartientfaculte)
# admin.site.register(Etudier)
# admin.site.register(Gerermod)
# admin.site.register(Enseigne)
