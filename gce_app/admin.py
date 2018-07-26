from django.contrib import admin
from gce_app.models import *

# Register your models here.

class UniversiteAdmin(admin.ModelAdmin):
    list_display = ('nom',)
admin.site.register(Universite, UniversiteAdmin)

class FaculteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_universite',)
admin.site.register(Faculte, FaculteAdmin)

class DomaineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_faculte',)
admin.site.register(Domaine, DomaineAdmin)

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user_choices', 'info_utilisateur' , 'type_utilisateur', 'id_utilisateur', 'avatar_utilisateur')
admin.site.register(Utilisateur, UtilisateurAdmin)

class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_domaine', 'id_chef_departement',)
admin.site.register(Filiere, FiliereAdmin)

class ParcoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_filiere',)
admin.site.register(Parcours, ParcoursAdmin)

class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_parcours',)
admin.site.register(Specialite, SpecialiteAdmin)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'id_specialite',)
admin.site.register(Section, SectionAdmin)

class GroupeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'id_section',)
admin.site.register(Groupe, GroupeAdmin)

class ChefDepartementAdmin(admin.ModelAdmin):
    list_display = ('id_chef_departement',)
admin.site.register(ChefDepartement, ChefDepartementAdmin)

class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('id_enseignant',)
admin.site.register(Enseignant, EnseignantAdmin)

class TechnicienAdmin(admin.ModelAdmin):
    list_display = ('id_technicien', 'id_faculte',)
admin.site.register(Technicien, TechnicienAdmin)

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id_etudiant', 'id_groupe',)
admin.site.register(Etudiant, EtudiantAdmin)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titre_module', 'finsaisie_module', 'id_specialite',)
admin.site.register(Module, ModuleAdmin)

class CorrectionAdmin(admin.ModelAdmin):
    list_display = ('id_module', 'id_enseignant', 'annee_correction',)
admin.site.register(Correction, CorrectionAdmin)

class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('sujet_annonce', 'description_annonce', 'date_annonce', 'heure_annonce', 'afficher_annonce',)
admin.site.register(Annonce, AnnonceAdmin)

class CopieAdmin(admin.ModelAdmin):
    list_display = ('annee_copie', 'afficher_copie', 'date_affichage', 'modifiable', 'id_module', 'id_etudiant', 'rectifier',)
admin.site.register(Copie, CopieAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sujet_notification', 'description_notification', 'vue_notification', 'date_notification', 'heure_notification', 'icon_notification', 'id_utilisateur',)
admin.site.register(Notification, NotificationAdmin)

class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('sujet_reclamation', 'description_reclamation', 'id_etudiant', 'id_module', 'regler_reclamation', 'approuver_reclamation', 'annee_reclamation',)
admin.site.register(Reclamation, ReclamationAdmin)

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('sale_consultation', 'date_consultation', 'heure_consultation', 'afficher_consultation', 'approve_consultation', 'id_enseignant', 'id_module',)
admin.site.register(Consultation, ConsultationAdmin)

class VersionCopieAdmin(admin.ModelAdmin):
    list_display = ('numero_version', 'note_version', 'id_copie',)
admin.site.register(VersionCopie, VersionCopieAdmin)

class FichierCopieAdmin(admin.ModelAdmin):
    list_display = ('emplacement_fichier', 'id_version', 'id_module',)
admin.site.register(FichierCopie, FichierCopieAdmin)

class FichierCorrectionAdmin(admin.ModelAdmin):
    list_display = ('emplacement_fichier', 'id_correction',)
admin.site.register(FichierCorrection, FichierCorrectionAdmin)

class AnneeUnivAdmin(admin.ModelAdmin):
    list_display = ('annee_univ', 'active',)
admin.site.register(AnneeUniv, AnneeUnivAdmin)

class AffichageAdmin(admin.ModelAdmin):
    list_display = ('id_module',)
admin.site.register(Affichage, AffichageAdmin)




# class DiscussionAdministrativeAdmin(admin.ModelAdmin):
#     list_display = ('id_chef_departement', 'id_enseignant',)
# admin.site.register(DiscussionAdministrative, DiscussionAdministrativeAdmin)

# class DiscussionReclamationAdmin(admin.ModelAdmin):
#     list_display = ('id_reclamation', 'id_enseignant',)
# admin.site.register(DiscussionReclamation, DiscussionReclamationAdmin)

# class MessagesAdministrativeAdmin(admin.ModelAdmin):
#     list_display = ('contenu_message', 'date_message', 'heure_message', 'id_emetteur', 'id_recepteur', 'id_discussion',)
# admin.site.register(MessagesAdministrative, MessagesAdministrativeAdmin)

#admin.site.register(Appartientfiliere)
# admin.site.register(Appartientfaculte)
# admin.site.register(Etudier)
# admin.site.register(Gerermod)
# admin.site.register(Enseigne)
