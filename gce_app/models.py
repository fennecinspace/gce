import os, uuid
from django.db import models
from django.contrib.auth.models import User

########################################################################
#######  Modifications : 
##   1 - added OneToOneFields
##   2 - Ordered Tables
##   3 - Added Validators
##   4 - Changed Fields Labels
##   5 - Replaced Relation Tables with ManyToManyFields
########################################################################

## FUNCTIONS
def copies_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('copies', filename)

def corrections_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('corrections', filename)

def avatars_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars', filename)


## MODELS
class Utilisateur(models.Model):
    user_choices = (('etud','Etudiant'),('ensg','Enseignant'),('tech','Technicien'),('chef','Chef Departement'))
    info_utilisateur = models.OneToOneField(User,models.CASCADE)
    type_utilisateur = models.CharField(db_column='type_Utilisateur', max_length=255, null=True, choices = user_choices)
    id_utilisateur = models.CharField(db_column='id_Utilisateur', primary_key=True, max_length=100, unique=True, blank=True, editable=False)
    avatar_utilisateur = models.FileField(db_column='Avatar', blank=True, null=True, upload_to = avatars_file_path)
    #nom_utilisateur = models.CharField(db_column='nom_Utilisateur', max_length=255, blank=True, null=True)
    #prenom_utilisateur = models.CharField(db_column='prenom_Utilisateur', max_length=255, blank=True, null=True)
    #identifiant_utilisateur = models.CharField(db_column='identifiant_Utilisateur', max_length=255, blank=True, null=True,unique=True)
    #password_utilisateur = models.CharField(db_column='password_Utilisateur', max_length=100, blank=True, null=True)
    #email_utilisateur = models.EmailField(db_column='email_Utilisateur', max_length=255, blank=True, null=True, unique=True)

    def save(self,*args, **kwargs):
        self.id_utilisateur = self.type_utilisateur + str(self.info_utilisateur.id)
        super().save(*args, **kwargs)
    

    class Meta:
        db_table = 'Utilisateur'


class Notification(models.Model):
    id_notification = models.CharField(db_column='id_Notification', primary_key=True, max_length=100)  # Field name made lowercase.
    sujet_notification = models.CharField(db_column='sujet_Notification', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description_notification = models.CharField(db_column='description_Notification', max_length=250, blank=True, null=True)  # Field name made lowercase.
    vue_notification = models.BooleanField(db_column='vue_Notification',default = False)  # Field name made lowercase.
    id_utilisateur = models.ForeignKey('Utilisateur', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Notification'


class ChefDepartement(models.Model):
    id_chef_departement = models.OneToOneField('Utilisateur', models.CASCADE, db_column='id_Utilisateur', primary_key=True)  # Field name made lowercase.
    #modules = models.ManyToManyField('Module', blank = False)
    
    class Meta:
        db_table = 'Chef_Departement'


class Universite(models.Model):
    id_universite = models.CharField(db_column='id_Universite', primary_key=True, max_length=100)  # Field name made lowercase.
    nom = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'Universite'


class Faculte(models.Model):
    id_faculte = models.CharField(db_column='id_Faculte', primary_key=True, max_length=100)  # Field name made lowercase.
    nom = models.CharField(max_length=1000, blank=True, null=True)
    id_universite = models.ForeignKey('Universite', models.CASCADE, db_column='id_Universite', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Faculte'


class Domaine(models.Model):
    id_domaine = models.CharField(db_column='id_Domaine', primary_key=True, max_length=100)  # Field name made lowercase.
    nom = models.CharField(max_length=1000)
    id_faculte = models.ForeignKey('Faculte', models.CASCADE, db_column='id_Faculte', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Domaine'


class Filiere(models.Model):
    id_filiere = models.CharField(db_column='id_Filiere', primary_key=True, max_length=100)  # Field name made lowercase.
    nom = models.CharField(max_length=1000)
    id_domaine = models.ForeignKey(Domaine, models.CASCADE, db_column='id_Domaine')  # Field name made lowercase.
    id_chef_departement = models.ForeignKey('ChefDepartement', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Filiere'


class Parcours(models.Model):
    id_parcours = models.CharField(db_column='id_Parcours', primary_key=True, max_length=100)  # Field name made lowercase.
    nom = models.CharField(max_length=100)
    id_filiere = models.ForeignKey('Filiere', models.CASCADE, db_column='id_Filiere')  # Field name made lowercase.

    class Meta:
        db_table = 'Parcours'


class Specialite(models.Model):
    id_specialite = models.CharField(db_column='id_Specialite', primary_key=True, max_length=100)  # Field name made lowercase.
    nom = models.CharField(max_length=1000)
    id_parcours = models.ForeignKey('Parcours', models.CASCADE, db_column='id_Parcours')  # Field name made lowercase.

    class Meta:
        db_table = 'Specialite'


class Section(models.Model):
    id_section = models.CharField(db_column='id_Section', primary_key=True, max_length=100)  # Field name made lowercase.
    numero = models.IntegerField()
    id_specialite = models.ForeignKey('Specialite', models.CASCADE, db_column='id_Specialite')  # Field name made lowercase.

    class Meta:
        db_table = 'Section'


class Groupe(models.Model):
    id_groupe = models.CharField(db_column='id_Groupe', primary_key=True, max_length=100)  # Field name made lowercase.
    numero = models.IntegerField()
    id_section = models.ForeignKey('Section', models.CASCADE, db_column='id_Section')  # Field name made lowercase.

    class Meta:
        db_table = 'Groupe'


class Technicien(models.Model):
    id_technicien = models.OneToOneField('Utilisateur', models.CASCADE, db_column='id_Utilisateur', primary_key=True)  # Field name made lowercase.
    id_faculte = models.ForeignKey('Faculte', models.CASCADE, db_column='id_Faculte', unique=False, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Technicien'


class Enseignant(models.Model):
    id_enseignant = models.OneToOneField('Utilisateur', models.CASCADE, db_column='id_Utilisateur', primary_key=True)  # Field name made lowercase.
    #id_filiere = models.ForeignKey('Filiere', models.CASCADE, db_column='id_Filiere')  # Field name made lowercase.
    filieres = models.ManyToManyField('Filiere', blank = True)
    modules = models.ManyToManyField('Module', blank = True)
    
    class Meta:
        db_table = 'Enseignant'


class Etudiant(models.Model):
    id_etudiant = models.OneToOneField('Utilisateur', models.CASCADE, db_column='id_Utilisateur', primary_key=True)  # Field name made lowercase.
    id_groupe = models.ForeignKey('Groupe', models.CASCADE, db_column='id_Groupe')  # Field name made lowercase.
    #modules = models.ManyToManyField('Module', blank=True)
    
    class Meta:
        db_table = 'Etudiant'


class Module(models.Model):
    id_module = models.CharField(db_column='id_Module', primary_key=True, max_length=100)  # Field name made lowercase.
    titre_module = models.CharField(db_column='titre_Module', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    #uniteenseignement_module = models.CharField(db_column='uniteEnseignement_Module', max_length=100, blank=True, null=True)  # Field name made lowercase.
    finsaisie_module = models.BooleanField(db_column='FinSaisie_Module', blank=True, default=False)  # Field name made lowercase.
    id_specialite = models.ForeignKey('Specialite', models.CASCADE , blank = True, null = True, unique = False)

    class Meta:
        db_table = 'Module'


class Annonce(models.Model):
    id_annonce = models.CharField(db_column='id_Annonce', primary_key=True, max_length=100)  # Field name made lowercase.
    sujet_annonce = models.CharField(db_column='sujet_Annonce', max_length=500, blank=True, null=True)  # Field name made lowercase.
    description_annonce = models.CharField(db_column='description_Annonce', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    date_annonce = models.DateField(db_column='date_Annonce', blank=True, null=True)  # Field name made lowercase.
    heure_annonce = models.TimeField(db_column='heure_Annonce', blank=True, null=True)  # Field name made lowercase.
    afficher_annonce = models.BooleanField(db_column='afficher_Annonce', default=False)  # Field name made lowercase.
    id_module = models.ForeignKey('Module', models.CASCADE, db_column='id_Module', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Annonce'


class Copie(models.Model):
    id_copie = models.CharField(db_column='id_Copie', primary_key=True, max_length=100)  # Field name made lowercase.
    id_module = models.ForeignKey('Module', models.CASCADE, db_column='id_Module', blank=True, null=True)  # Field name made lowercase.
    id_etudiant = models.ForeignKey('Etudiant', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Copie'


class VersionCopie(models.Model):
    id_version = models.CharField(db_column='id_Version', primary_key=True, max_length=100)  # Field name made lowercase.
    numero_version = models.IntegerField(db_column='numero_Version', blank=True, null=True)
    note_copie = models.FloatField(db_column='note_Copie', blank=True, null=True)  # Field name made lowercase.
    #emplacement_copie = models.CharField(db_column='emplacement_Copie', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    id_copie = models.ForeignKey('Copie', models.CASCADE, db_column='id_Copie', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'VersionCopie'


class FichierCopie(models.Model):
    id_fichier = models.CharField(db_column='id_Fichier', primary_key=True, max_length=100)
    emplacement_fichier = models.FileField(db_column='emplacement_Fichier', blank=True, null=True, upload_to = copies_file_path)
    id_version = models.ForeignKey('VersionCopie', models.CASCADE, db_column='id_Version', blank=True, null=True)

    class Meta:
        db_table = 'FichierCopie'


class Correction(models.Model):
    id_correction = models.CharField(db_column='id_Correction', primary_key=True, max_length=100)  # Field name made lowercase.
    #emplacement_correction = models.CharField(db_column='emplacement_Correction', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    id_module = models.ForeignKey('Module', models.CASCADE, db_column='id_Module', blank=True, null=True)  # Field name made lowercase.
    id_enseignant = models.ForeignKey('Enseignant', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Correction'


class FichierCorrection(models.Model):
    id_fichier = models.CharField(db_column='id_Fichier', primary_key=True, max_length=100)
    emplacement_fichier = models.FileField(db_column='emplacement_Fichier', blank=True, null=True, upload_to=corrections_file_path)
    id_correction = models.ForeignKey('Correction', models.CASCADE, db_column='id_Correction', blank=True, null=True)

    class Meta:
        db_table = 'FichierCorrection'


class Reclamation(models.Model):
    id_reclamation = models.CharField(db_column='id_Reclamation', primary_key=True, max_length=100)  # Field name made lowercase.
    sujet_reclamation = models.CharField(db_column='Sujet_Reclamation', max_length=500, blank=True, null=True)  # Field name made lowercase.
    description_reclamation = models.CharField(db_column='Description_Reclamation', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    id_etudiant = models.ForeignKey('Etudiant', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.
    id_module = models.ForeignKey('Module', models.CASCADE, db_column='id_Module', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Reclamation'


class Consultation(models.Model):
    id_consultation = models.CharField(db_column='id_Consultation', primary_key=True, max_length=100)  # Field name made lowercase.
    sale_consultation = models.CharField(db_column='sale_Consultation', max_length=250, blank=True, null=True)  # Field name made lowercase.
    date_consultation = models.DateField(db_column='date_Consultation', blank=True, null=True)  # Field name made lowercase.
    heure_consultation = models.TimeField(db_column='heure_Consultation', blank=True, null=True)  # Field name made lowercase.
    afficher_consultation = models.BooleanField(db_column='afficher_Consultation', default=False)  # Field name made lowercase.
    id_enseignant = models.ForeignKey('Enseignant', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.
    id_module = models.ForeignKey('Module', models.CASCADE, db_column='id_Module', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Consultation'


class DiscussionAdministrative(models.Model):
    id_discussion = models.CharField(db_column='id_Discussion', primary_key=True, max_length=100)  # Field name made lowercase.
    id_chef_departement = models.ForeignKey('ChefDepartement', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.
    id_enseignant = models.ForeignKey('Enseignant', models.CASCADE, db_column='id_Utilisateur_1', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Discussion_Administrative'


class DiscussionReclamation(models.Model):
    id_discussion = models.CharField(db_column='id_Discussion', primary_key=True, max_length=100)  # Field name made lowercase.
    id_reclamation = models.ForeignKey('Reclamation', models.CASCADE, db_column='id_Reclamation', blank=True, null=True)  # Field name made lowercase.
    id_enseignant = models.ForeignKey('Enseignant', models.CASCADE, db_column='id_Utilisateur', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Discussion_Reclamation'


class MessagesAdministrative(models.Model):
    id_message = models.CharField(db_column='id_Message', primary_key=True, max_length=100)  # Field name made lowercase.
    contenu_message = models.CharField(db_column='contenu_Message', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    date_message = models.DateField(db_column='date_Message', blank=True, null=True)  # Field name made lowercase.
    heure_message = models.TimeField(db_column='heure_Message', blank=True, null=True)  # Field name made lowercase.
    id_emetteur = models.CharField(db_column='id_Emetteur', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id_recepteur = models.CharField(db_column='id_Recepteur', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id_discussion = models.ForeignKey('DiscussionAdministrative', models.CASCADE, db_column='id_Discussion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Messages_Administrative'


class MessagesReclamation(models.Model):
    id_message = models.CharField(db_column='id_Message', primary_key=True, max_length=100)  # Field name made lowercase.
    contenu_message = models.CharField(db_column='contenu_Message', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    date_message = models.DateField(db_column='date_Message', blank=True, null=True)  # Field name made lowercase.
    heure_message = models.TimeField(db_column='heure_Message', blank=True, null=True)  # Field name made lowercase.
    id_emetteur = models.CharField(db_column='id_Emetteur', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id_recepteur = models.CharField(db_column='id_Recepteur', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id_discussion = models.ForeignKey('DiscussionReclamation', models.CASCADE, db_column='id_Discussion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Messages_Reclamation'


# class Appartientfiliere(models.Model):
#     id_enseignant = models.ForeignKey('Enseignant', models.CASCADE, db_column='id_Utilisateur')  # Field name made lowercase.
#     id_filiere = models.ForeignKey('Filiere', models.CASCADE, db_column='id_Filiere')  # Field name made lowercase.

#     class Meta:
#         db_table = 'appartientFiliere'
#         unique_together = (('id_filiere', 'id_enseignant'),)


# class Etudier(models.Model):
#     id_etudiant = models.ForeignKey('Etudiant', models.CASCADE, db_column='id_Utilisateur', unique=False)  # Field name made lowercase.
#     id_module = models.ForeignKey('Module', models.CASCADE, db_column='id_Module', primary_key=True, unique=False)  # Field name made lowercase.

#     class Meta:
#         db_table = 'etudier'
#         unique_together = (('id_module', 'id_etudiant'),)


# class Gerermod(models.Model):
#     id_chef_departement = models.ForeignKey('ChefDepartement', models.CASCADE, db_column='id_Utilisateur', primary_key=True, unique=False)  # Field name made lowercase.
#     id_module = models.OneToOneField('Module', models.CASCADE, db_column='id_Module')  # Field name made lowercase.

#     class Meta:
#         db_table = 'gererMod'
#         unique_together = (('id_chef_departement', 'id_module'),)


# class Enseigne(models.Model):
#     id_enseignant = models.ForeignKey('Enseignant', models.CASCADE, db_column='id_Utilisateur', primary_key=True, unique=False)  # Field name made lowercase.
#     id_module = models.OneToOneField    ('Module', models.CASCADE, db_column='id_Module')  # Field name made lowercase.

#     class Meta:
#         db_table = 'Enseigne'
#         unique_together = (('id_enseignant', 'id_module'),)
