from django.contrib import admin
from gce_app.models import *

# Register your models here.

admin.site.register(Universite)
admin.site.register(Faculte)
admin.site.register(Domaine)
admin.site.register(Utilisateur)
admin.site.register(Filiere)
admin.site.register(Parcours)
admin.site.register(Specialite)
admin.site.register(Section)
admin.site.register(Groupe)
admin.site.register(ChefDepartement)
admin.site.register(Enseignant)
admin.site.register(Technicien)
admin.site.register(Etudiant)
admin.site.register(Module)
admin.site.register(Correction)
admin.site.register(Annonce)
admin.site.register(Copie)
admin.site.register(Notification)
admin.site.register(DiscussionAdministrative)
admin.site.register(Reclamation)
admin.site.register(DiscussionReclamation)
admin.site.register(Consultation)
admin.site.register(MessagesAdministrative)
admin.site.register(VersionCopie)
admin.site.register(FichierCopie)
admin.site.register(FichierCorrection)

class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('annee_scolaire', 'active')
admin.site.register(AnneeScolaire, AnneeScolaireAdmin)

#admin.site.register(Appartientfiliere)
# admin.site.register(Appartientfaculte)
# admin.site.register(Etudier)
# admin.site.register(Gerermod)
# admin.site.register(Enseigne)
