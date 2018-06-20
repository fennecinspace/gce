#####################
## necessary imports
import os, random, sys, django, faker, datetime
from django.db.models import Q


#################################
## Setting up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gce.settings")
django.setup()
fake = faker.Faker()
dt = datetime.datetime


####################
## Importing models 
from gce_app.models import *
print ('models imported')


#########################
## Predifining Constants
NBTABLES = 30
SITEDOMAINS = ("dz","com","fr","net","org","info","us","it","co.jp")
PRENOMS = ("mohamed","amine","yassine","karim","fouad","wael","abdallah","othmane","abdelrahmane","abdekarim","youssra","fatima","khadidja","wafaa","radia","raya","assia")
NOMS = ("belhadj kacem","benkedadra","henni","benkourreche","belkaid","benguetate","khelil","belhadj","benahmed","youcefi","zendagi","khouja","abbas","naffousi")
MAILS = ("hotmail","gmail","outlook","yahoo","aol","live","mail")
CITIES = ("Mostaganem",)
FACULTIES = ('FSEI','FDSP','FMED','FST')
DOMAINS = ('Mathématique Informatique','Science Matiere')
BRANCHES = (('Mathématique','Informatique','Mathématique Informatique Tronc Commun'),('Physique','Chemie','Science Matiere Tronc Commun'))
PARCOURS = ('L1','L2','L3','M1','M2')
SPECIALTIES = ('Math Info Tronc Commun','Systeme Information','Systeme Information Geographique','Ingenierie Systeme Information')
IDS = ('etud','ensg','tech','chef','univ','fclt','domn','filr','prcr','spec','sect','grop','modl','crct','annc','copy','notf','dadm','rclm','drcl','cnsl','madm','mrcl','vers','fich')
######   0      1      2      3      4       5      6     7      8       9     10     11     12     13     14     15     16     17     18     19     20     21     22     23     24


#######################################
## Defining randomizers and generators
def GenerateId(id_value, id_number):
    return str(id_value) + str(id_number)

def CreateUtilisateur(user_type, counter, gen_avatar):
    allUsers = Utilisateur.objects.all()
    gen_lastName = random.choice(NOMS)
    gen_firstName = random.choice(PRENOMS)
    gen_email = user_type + str(counter+1) + "@" + random.choice(MAILS) + "." + random.choice(SITEDOMAINS)       
    gen_userId = user_type + str(counter+1)
    gen_userPassword = "password" + str(10) #str(random.randint(0,500))
    # Saving User Objects
    obj = User(username = gen_userId,last_name = gen_lastName, first_name = gen_firstName, email = gen_email)
    obj.set_password(gen_userPassword)
    obj.save()
    if user_type == "etudiant":
        gen_type = IDS[0]
    elif user_type == "enseignant":
        gen_type = IDS[1]
    elif user_type == "technicien":
        gen_type = IDS[2]
    else: #user_type == "chef departement"
        gen_type = IDS[3] 
    return Utilisateur(info_utilisateur = obj, type_utilisateur = gen_type)
    # , avatar_utilisateur = gen_avatar)

########################
## defining Populators
def PopulateUtilisateur(nbEtud = 200, nbEnsen = 6, nbTech = 2, nbChef = 1): # i use try and except to solve the unique fields issue 
    default_avatar = os.path.join('default','default_avatar.png')
    nbOfUsersToCreate = nbEtud + nbEnsen + nbTech + nbChef
    nbOfUsers = 0
    sys.stdout.write('[01/{}]Utilisateur-User : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
    for counter in range (0, nbEtud):
        obj = CreateUtilisateur("etudiant",counter,default_avatar)
        obj.save()
        nbOfUsers += 1
        sys.stdout.write('\r[01/{}]Utilisateur-User : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
    for counter in range (0, nbEnsen):
        obj = CreateUtilisateur("enseignant",counter,default_avatar)
        obj.save()
        nbOfUsers += 1
        sys.stdout.write('\r[01/{}]Utilisateur-User : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
    for counter in range (0, nbTech):
        obj = CreateUtilisateur("technicien",counter,default_avatar)
        obj.save()
        nbOfUsers += 1
        sys.stdout.write('\r[01/{}]Utilisateur-User : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
    for counter in range (0, nbChef):
        obj = CreateUtilisateur("chef_departement",counter,default_avatar)
        obj.save()
        nbOfUsers += 1
        sys.stdout.write('\r[01/{}]Utilisateur-User : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))


def PopulateStruct():
    usr = Utilisateur.objects.filter(type_utilisateur = IDS[3])[0]
    chef = ChefDepartement(id_chef_departement = usr)
    chef.save()

    anneee = AnneeUniv(active = True, annee_univ = "2017-2018")
    anneee.save()

    print("\nStarted Populating Structure...", end = "")
    #UNIVERSITE
    uni = Universite(nom = "Université de Mostaganem")
    uni.save()

    #FACULTE
    fac = Faculte(nom = "Faculté des Sciences Exactes et Informatique", id_universite = uni)
    fac.save()

    #DOMAINE
    mathinfo = Domaine(nom = DOMAINS[0], id_faculte = fac)
    mathinfo.save()

    #FILIERE
    infofil = Filiere(nom = BRANCHES[1], id_domaine = mathinfo, id_chef_departement = chef)
    infofil.save()

    #PARCOURS
    Parcours(nom = PARCOURS[1], id_filiere = infofil).save()
    Parcours(nom = PARCOURS[3], id_filiere = infofil).save()
    Parcours(nom = PARCOURS[4], id_filiere = infofil).save()
    l3parc = Parcours(nom = PARCOURS[2], id_filiere = infofil)
    l3parc.save()

    #SPECIALITE
    sispec = Specialite(nom = SPECIALTIES[1], id_parcours = l3parc)
    sispec.save()

    #SECTION
    sec1 = Section(numero = 1, id_specialite = sispec)
    sec1.save()
    sec2 = Section(numero = 2, id_specialite = sispec)
    sec2.save()

    #GROUPE
    groups = []
    for i in range(7):
        grp = Groupe(numero = i+1, id_section = random.choice([sec1, sec2]))
        grp.save()
        groups += [grp]
    print("\rFinished Populating Structure !", end = "")
    
    ##### USERS
    print("\nStarted Populating Users !", end = "")
    for tech in Utilisateur.objects.filter(type_utilisateur = IDS[2]):
        Technicien(id_technicien = tech, id_faculte = fac).save()
    
    ensges = []
    for index, ensg in enumerate(Utilisateur.objects.filter(type_utilisateur = IDS[1])):
        en_sg = Enseignant(id_enseignant = ensg)
        en_sg.save()
        en_sg.filieres.add(infofil)
        if index == 0 or index == 1:
            ensges += [en_sg]
    
    for etud in Utilisateur.objects.filter(type_utilisateur = IDS[0]):
        Etudiant(id_etudiant = etud, id_groupe = random.choice(groups)).save()
    print("\rFinished Populating Users !", end = "")

    ##### MODULES
    print("\nStarted Populating Modules !", end = "")
    mods = []
    mod1 = Module(titre_module = "Programmation Orienté Objet", id_specialite = sispec)
    mod1.save()
    mods += [mod1]

    mod2 = Module(titre_module = "Intelligence Artificielle", id_specialite = sispec)
    mod2.save()
    mods += [mod2]

    mod3 = Module(titre_module = "Algorithmique et Structure de Données", id_specialite = sispec)
    mod3.save()
    mods += [mod3]

    mod4 = Module(titre_module = "Cryptographie", id_specialite = sispec)
    mod4.save()
    mods += [mod4]

    mod5 = Module(titre_module = "Recherche Opérationnelle", id_specialite = sispec)
    mod5.save()
    mods += [mod5]

    mod6 = Module(titre_module = "Sécurité Informatique", id_specialite = sispec)
    mod6.save()
    mods += [mod6]
    print("\rFinished Populating Modules !", end = "")

    ##### RELATIONS 
    print("\nStarted Populating Relations !", end = "")
    ensges[0].modules.add(*[mod1, mod2, mod3])
    ensges[1].modules.add(*[mod4, mod5, mod6])
    # for index, module in enumerate(mods):
    #     if index % 2 == 0:
    #         ensges[0].modules.add(module)
    #     else:
    #         ensges[1].modules.add(module)
    print("\rFinished Populating Relations !", end = "")
            

    

def Populate():
    nbetud = input('nombre d\'étudiants : ')
    nbetud = int(nbetud)
    PopulateUtilisateur(nbEtud = nbetud)
    PopulateStruct()

if __name__ == '__main__':
    print('populating...')
    Populate()
    print('\ndone !')
