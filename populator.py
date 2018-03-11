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
NBTABLES = 26
SITEDOMAINS = ("dz","com","fr","net","org","info","us","it","co.jp")
PRENOMS = ("mohamed","amine","yassine","karim","fouad","wael","abdallah","othmane","abdelrahmane","abdekarim","youssra","fatima","khadidja","wafaa","radia","raya","assia")
NOMS = ("belhadj kacem","benkedadra","henni","benkourreche","belkaid","benguetate","khelil","belhadj","benahmed","youcefi","zendagi","khouja","abbas","naffousi")
MAILS = ("hotmail","gmail","outlook","yahoo","aol","live","mail")
CITIES = ("Mostaganem",)
FACULTIES = ('FSEI','FDSP','FMED','FST')
DOMAINS = (('Math Info','Science Matiere'),('Droit','Sciences Politiques'))
BRANCHES = (('Math','Informatique','Math Info Tronc Commun'),('Physique','Chemie','Science Matiere Tronc Commun'))
PARCOURS = ('L1','L2','L3','M1','M2')
SPECIALTIES = ('Math Info Tronc Commun','Systeme Information','Systeme Information Geographique','Ingenierie Systeme Information')
IDS = ('etud','ensg','tech','chef','univ','fclt','domn','filr','prcr','spec','sect','grop','modl','crct','annc','copy','notf','dadm','rclm','drcl','cnsl','madm','mrcl')
######   0      1      2      3      4       5      6     7      8       9     10     11     12     13     14     15     16     17     18     19     20     21     22


#######################################
## Defining randomizers and generators
def GenerateId(id_value, id_number):
    return str(id_value) + str(id_number)

def CreateUtilisateur(user_type, counter):
    if user_type == "etudiant":
        gen_id = GenerateId(IDS[0],counter)

    elif user_type == "enseignant":
        gen_id = GenerateId(IDS[1],counter)

    elif user_type == "technicien":
        gen_id = GenerateId(IDS[2],counter)

    else: #user_type == "chef departement"
        gen_id = GenerateId(IDS[3],counter)

    gen_lastName = random.choice(NOMS)
    gen_firstName = random.choice(PRENOMS)
    gen_email = gen_firstName + gen_lastName + "@" + random.choice(MAILS) + "." + random.choice(SITEDOMAINS)
    gen_userId = user_type + str(counter)
    gen_userPassword = "password" + str(random.randint(0,500))

    return Utilisateur(id_utilisateur = gen_id,\
     nom_utilisateur = gen_lastName, prenom_utilisateur = gen_firstName,\
     identifiant_utilisateur = gen_userId, password_utilisateur = gen_userPassword,\
     email_utilisateur = gen_email)


########################
## defining Populators
def PopulateUtilisateur(nbEtud = 200, nbEnsen = 10, nbTech = 5, nbChef = 6): # i use try and except to solve the unique fields issue 
    nbOfUsersToCreate = nbEtud + nbEnsen + nbTech + nbChef
    nbOfUsers = 0
    sys.stdout.write('[01/{}]Utilisateur : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
    for counter in range (0, nbEtud):
        while True:
            try:
                obj = CreateUtilisateur("etudiant",counter)
                obj.save()
            except: 
                continue
            nbOfUsers += 1
            sys.stdout.write('\r[01/{}]Utilisateur : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
            break

    for counter in range (0, nbEnsen):
        while True:
            try:
                obj = CreateUtilisateur("enseignant",counter)
                obj.save()
            except: 
                continue
            nbOfUsers += 1
            sys.stdout.write('\r[01/{}]Utilisateur : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
            break

    for counter in range (0, nbTech):
        while True:
            try:
                obj = CreateUtilisateur("technicien",counter)
                obj.save()
            except: 
                continue
            nbOfUsers += 1
            sys.stdout.write('\r[01/{}]Utilisateur : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
            break

    for counter in range (0, nbChef):
        while True:
            try:
                obj = CreateUtilisateur("chef departement",counter)
                obj.save()
            except: 
                continue
            nbOfUsers += 1
            sys.stdout.write('\r[01/{}]Utilisateur : {}/{}'.format(NBTABLES,nbOfUsers,nbOfUsersToCreate))
            break

def PopulateNotification():
    allUsers = Utilisateur.objects.filter(Q(id_utilisateur__contains = IDS[0]) | Q(id_utilisateur__contains = IDS[1]) | Q(id_utilisateur__contains = IDS[3]))
    nbOfEntriesToCreate = len(allUsers) * 2
    nbOfEntries = 0
    sys.stdout.write('\n[02/{}]Notification : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for user in allUsers:
        for i in range(0,2):
            gen_id = IDS[16] + str(nbOfEntries)
            gen_sujet = fake.text(30)
            gen_description = fake.text(120)
            obj = Notification(id_notification = gen_id, sujet_notification = gen_sujet, description_notification = gen_description, vue_notification = False, id_utilisateur = user)
            obj.save()
            nbOfEntries += 1 
            sys.stdout.write('\r[02/{}]Notification : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateChefDepartement(nbChef = 6):
    allUsers = Utilisateur.objects.all()
    nbOfEntriesToCreate = nbChef
    nbOfEntries = 0
    sys.stdout.write('\n[03/{}]ChefDepatement : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for user in allUsers:
        if IDS[3] in user.id_utilisateur:
            obj = ChefDepartement(id_chef_departement = user)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[03/{}]ChefDepatement : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateUniversite():
    nbOfEntriesToCreate = len(CITIES)
    nbOfEntries = 0
    sys.stdout.write('\n[04/{}]Universite : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for i in range(0,len(CITIES)):
        gen_id = IDS[4] + str(i)
        gen_nom = "University Of " + CITIES[i]
        obj = Universite(id_universite = gen_id, nom = gen_nom) 
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[04/{}]Universite : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateFaculte():
    allUniversities = Universite.objects.all()
    nbOfEntriesToCreate = len(allUniversities) * len(FACULTIES)
    nbOfEntries = 0
    sys.stdout.write('\n[05/{}]Faculte : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for university in allUniversities:
        for faculte in FACULTIES:
            gen_id = IDS[5] + str(nbOfEntries)
            gen_nom = faculte
            obj = Faculte(id_faculte = gen_id, nom = gen_nom, id_universite = university)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[05/{}]Faculte : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateDomaine(facultiesToPopulate):
    nbOfEntriesToCreate = 0
    for facultyToPopulate in facultiesToPopulate:
        allFaculties = Faculte.objects.filter(nom = FACULTIES[facultyToPopulate])
        nbOfEntriesToCreate += len(allFaculties) * len(DOMAINS[facultyToPopulate])
    nbOfEntries = 0
    sys.stdout.write('\n[06/{}]Domaine : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for facultyToPopulate in facultiesToPopulate:
        allFaculties = Faculte.objects.filter(nom = FACULTIES[facultyToPopulate])
        for faculty in allFaculties:
            for domain in DOMAINS[facultyToPopulate]:
                gen_id = IDS[6] + str(nbOfEntries)
                gen_nom = domain
                obj = Domaine(id_domaine = gen_id, nom = gen_nom, id_faculte = faculty)
                obj.save()
                nbOfEntries += 1
                sys.stdout.write('\r[06/{}]Domaine : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateFiliere():
    allDomains = (Domaine.objects.filter(nom = "Math Info"),Domaine.objects.filter(nom = "Science Matiere"))
    allChefDepartement = ChefDepartement.objects.all()
    nbOfEntriesToCreate = len(allDomains[0]) * len(BRANCHES[0]) + len(allDomains[1]) * len(BRANCHES[1])
    nbOfEntries = 0 
    sys.stdout.write('\n[07/{}]Filiere : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for i in range(0,len(allDomains)):
            for domain in allDomains[i]:
                for branch in BRANCHES[i]:
                    gen_id = IDS[7] + str(nbOfEntries) 
                    gen_nom = branch
                    obj = Filiere(id_filiere = gen_id, nom = gen_nom, id_domaine = domain, id_chef_departement = allChefDepartement[nbOfEntries])
                    obj.save()
                    nbOfEntries += 1
                    sys.stdout.write('\r[07/{}]Filiere : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateParcours():
    allBranchs = Filiere.objects.all()
    troncBranchs = set()
    otherBranchs = set()
    for branch in allBranchs:
        if 'Commun'in branch.nom:
            troncBranchs.add(branch)
        else:
            otherBranchs.add(branch)

    nbOfEntriesToCreate = len(troncBranchs) + len (otherBranchs) * 4
    nbOfEntries = 0 
    sys.stdout.write('\n[08/{}]Parcours : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

    for branch in troncBranchs:
        gen_id = IDS[8] + str(nbOfEntries)
        gen_nom = PARCOURS[0]
        obj = Parcours(id_parcours = gen_id, nom = gen_nom,id_filiere = branch)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[08/{}]Parcours : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

    for branch in otherBranchs:
        for parcour in PARCOURS[1:]:
            gen_id = IDS[8] + str(nbOfEntries)
            gen_nom = parcour
            obj = Parcours(id_parcours = gen_id, nom = gen_nom,id_filiere = branch)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[08/{}]Parcours : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateSpecialite():
    L1MI = Parcours.objects.filter(id_filiere = (Filiere.objects.filter(nom = "Math Info Tronc Commun"))[0].id_filiere)[0]
    L3INFO = Parcours.objects.filter(nom = "L3", id_filiere = (Filiere.objects.filter(nom = "Informatique"))[0].id_filiere)[0]
    M1INFO = Parcours.objects.filter(nom = "M1", id_filiere = (Filiere.objects.filter(nom = "Informatique"))[0].id_filiere)[0]
    Parcs = [L1MI,L3INFO,M1INFO,M1INFO]
    nbOfEntriesToCreate = len(Parcs)
    nbOfEntries = 0
    sys.stdout.write('\n[09/{}]Specialite : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate)) 
    for i in range(0, len(SPECIALTIES)):
        gen_id = IDS[9] + str(nbOfEntries)
        gen_nom = SPECIALTIES[i]
        obj = Specialite(id_specialite = gen_id, nom = gen_nom,id_parcours = Parcs[i])
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[09/{}]Specialite : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate)) 

def PopulateSection():
    allSpecialties = Specialite.objects.all()
    nbOfEntriesToCreate = 0
    for specialty in allSpecialties:
        if 'Commun' in specialty.nom:
            nbOfEntriesToCreate += 2
        else:
            nbOfEntriesToCreate += 1
    nbOfEntries = 0
    sys.stdout.write('\n[10/{}]Section : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for specialty in allSpecialties:
        if 'Commun' in specialty.nom:
            x = 2
        else:
            x = 1
        for i in range(0,x):
            gen_id = IDS[10] + str(nbOfEntries)
            obj = Section(id_section = gen_id, numero = i + 1, id_specialite = specialty)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[10/{}]Section : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate)) 

def PopulateGroupe():
    v = 0
    w = 0
    nbOfEntries = 0
    nbOfEntriesToCreate = 0
    doubleSection = set()
    singleSpecial = set()
    allSpecialties = Specialite.objects.all()
    for specialty in allSpecialties:
        if 'Tronc' in specialty.nom:
            doubleSection.add(specialty)
        else:
            singleSpecial.add(specialty)
    allSections = Section.objects.all()
    for section in allSections:
        if section.id_specialite in doubleSection:
            nbOfEntriesToCreate += 3 + v
            v -= 1
        else:
            nbOfEntriesToCreate += 2 + w
            w -= 1
    sys.stdout.write('\n[11/{}]Groupe : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    v = 0
    w = 0
    for section in allSections:
        if section.id_specialite in doubleSection:
            x = 3 + v
            v -= 1
        else:
            x = 2 + w
            w -= 1
        for i in range (0,x):
            gen_id = IDS[11] + str(nbOfEntries)
            obj = Groupe(id_groupe = gen_id, numero = i + 1, id_section = section)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[11/{}]Groupe : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate)) 

def PopulateTechnicien():
    FSEI = Faculte.objects.filter(nom = FACULTIES[0], id_universite = Universite.objects.filter(nom__contains = CITIES[0])[0])[0]
    allUsers = Utilisateur.objects.all()
    nbOfEntriesToCreate = 5
    nbOfEntries = 0
    sys.stdout.write('\n[12/{}]Technicien : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for user in allUsers:
        if IDS[2] in user.id_utilisateur:
            obj = Technicien(id_technicien = user, id_faculte = FSEI)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[12/{}]Technicien : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateEnseignant(nbEnsen = 10):
    allTeachers = Utilisateur.objects.filter(id_utilisateur__contains = IDS[1])
    nbOfEntriesToCreate = nbEnsen
    nbOfEntries = 0
    sys.stdout.write('\n[13/{}]Enseignant : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for teacher in allTeachers:
        obj = Enseignant(id_enseignant = teacher)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[13/{}]Enseignant : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateEtudiant(nbEtud = 200):
    i = 0
    allStudents = Utilisateur.objects.filter(id_utilisateur__contains = IDS[0])
    allGroups = Groupe.objects.all()
    nbOfEntriesToCreate = nbEtud
    nbOfEntries = 0
    sys.stdout.write('\n[14/{}]Etudiant : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for group in allGroups:
        for student in allStudents[i:i+25]:
            obj = Etudiant(id_etudiant = student, id_groupe = group)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[14/{}]Etudiant : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
        i = i +25

def PopulateModule(nbMod = 20):
    allSpecialties = Specialite.objects.all()
    nbOfEntriesToCreate = nbMod
    nbOfEntries = 0
    sys.stdout.write('\n[15/{}]Module : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate)) 
    for speciality in allSpecialties:
        for _ in range (0,nbMod//len(allSpecialties)):
            gen_id = IDS[12] + str(nbOfEntries)
            gen_titre = "module no " + str(nbOfEntries)
            obj = Module(id_module = gen_id, titre_module = gen_titre, finsaisie_module = False, id_specialite = speciality)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[15/{}]Module : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate)) 

def PopulateAnnonce():
    allModules = Module.objects.all()
    nbOfEntriesToCreate = len(allModules) * 2
    nbOfEntries = 0
    sys.stdout.write('\n[16/{}]Annonce : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for module in allModules:
        for i in range(0,2):
            gen_id = IDS[14] + str(nbOfEntries)
            gen_sujet = fake.text(30)
            gen_description = fake.text(120)
            gen_date = dt.strptime(fake.date(),'%Y-%M-%d').date()
            gen_time = dt.strptime(fake.time(),'%H:%M:%S').time()
            obj = Annonce(id_annonce = gen_id, sujet_annonce = gen_sujet, description_annonce = gen_description, date_annonce = gen_date, heure_annonce = gen_time, afficher_annonce = False, id_module = module)
            obj.save()
            nbOfEntries += 1 
            sys.stdout.write('\r[16/{}]Annonce : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def RelationEnseignantFiliere():
    x = 0
    allTeachers = Enseignant.objects.all()
    allFiliere = Filiere.objects.filter(id_domaine = Domaine.objects.filter(nom__contains = "Info")[0]).exclude(nom__contains = "Tronc")
    troncCommunFiliere = Filiere.objects.filter(Q(nom__contains = "Tronc") & Q(nom__contains = "Info"))[0]
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allTeachers)
    sys.stdout.write('\n[17/{}]Relation ENSEIGNANT FILIERE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for teacher in allTeachers:
        if x == 0:
            filiere = allFiliere[0]
            x = 1
        else:
            filiere = allFiliere[1]
            x = 0
        teacher.filieres.add(filiere)
        teacher.filieres.add(troncCommunFiliere)
        nbOfEntries += 1
        sys.stdout.write('\r[17/{}]Relation ENSEIGNANT FILIERE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def RelationEnseignantModule():
    allTeachers = Enseignant.objects.all()
    allModules = Module.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allModules)
    sys.stdout.write('\n[18/{}]Relation ENSEIGNANT MODULE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for module in allModules:
        allTeachers = Enseignant.objects.filter(filieres__in = [module.id_specialite.id_parcours.id_filiere])
        random.choice(allTeachers).modules.add(module)
        nbOfEntries += 1
        sys.stdout.write('\r[18/{}]Relation ENSEIGNANT MODULE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def RelationChefDepartementModule():
    allModules = Module.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allModules)
    sys.stdout.write('\n[19/{}]Relation CHEF MODULE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for module in allModules:
        (module.id_specialite.id_parcours.id_filiere.id_chef_departement).modules.add(module)
        nbOfEntries += 1
        sys.stdout.write('\r[19/{}]Relation CHEF MODULE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def RelationEtudiantModule():
    allModules = Module.objects.all()
    allStudents  = Etudiant.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = 0
    sys.stdout.write('\n[20/{}]Relation ETUDIANT MODULE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for student in allStudents:
        for module in allModules:
            if student.id_groupe.id_section.id_specialite == module.id_specialite:
                nbOfEntriesToCreate += 1
    for student in allStudents:
        for module in allModules:
            if student.id_groupe.id_section.id_specialite == module.id_specialite:
                student.modules.add(module)
                nbOfEntries += 1
                sys.stdout.write('\r[20/{}]Relation ETUDIANT MODULE : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
        
def PopulateCopie2():
    student_module_relations = Etudiant.modules.through.objects.all()
    nbOfEntries = 0
    x = 0
    nbOfEntriesToCreate = 0
    sys.stdout.write('\n[21/{}]Copie : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for relation in student_module_relations:
        if x == 0: ### 80% entries creation
            x += 1
            continue
        elif x < 4:
            x += 1
        else:
            x = 0
        nbOfEntriesToCreate += 1
    for relation in student_module_relations:
        if x == 0:
            x += 1
            continue
        elif x < 4:
            x += 1
        else:
            x = 0
        gen_id = IDS[15] + str(nbOfEntries)
        note_copie = str(random.randint(0,20))
        gen_emplacement_copie = "/media/copies/" + gen_id
        gen_id_module = relation.module
        gen_id_etudiant = relation.etudiant
        obj = Copie(id_copie = gen_id, note_copie = note_copie, emplacement_copie = gen_emplacement_copie, id_module = gen_id_module, id_etudiant = gen_id_etudiant)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[21/{}]Copie : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateCopie():
    allStudents = Etudiant.objects.all()
    nbOfEntries = 0
    x = 0
    nbOfEntriesToCreate = 0
    for student in allStudents:
        allModules = Module.objects.filter(id_specialite = Specialite.objects.filter(id_specialite = (Section.objects.filter(id_section = Groupe.objects.filter(id_groupe = student.id_groupe.id_groupe)[0].id_section.id_section)[0].id_specialite.id_specialite))[0])
        for module in allModules:
            if x == 0: ### 80% entries creation
                x += 1
                continue
            elif x < 4:
                x += 1
            else:
                x = 0
            nbOfEntriesToCreate += 1
    sys.stdout.write('\n[21/{}]Copie : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for student in allStudents:
        allModules = Module.objects.filter(id_specialite = Specialite.objects.filter(id_specialite = (Section.objects.filter(id_section = Groupe.objects.filter(id_groupe = student.id_groupe.id_groupe)[0].id_section.id_section)[0].id_specialite.id_specialite))[0])
        for module in allModules:
            if x == 0: ### 80% entries creation
                x += 1
                continue
            elif x < 4:
                x += 1
            else:
                x = 0
            gen_id = IDS[15] + str(nbOfEntries)
            note_copie = str(random.randint(0,20))
            gen_emplacement_copie = "/media/copies/" + gen_id
            gen_id_module = module
            gen_id_etudiant = student
            obj = Copie(id_copie = gen_id, note_copie = note_copie, emplacement_copie = gen_emplacement_copie, id_module = gen_id_module, id_etudiant = gen_id_etudiant)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[21/{}]Copie : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateCorrection():
    teacher_module_relations = Enseignant.modules.through.objects.all()
    nbOfEntries = 0
    x = 0
    nbOfEntriesToCreate = 0
    sys.stdout.write('\n[20/{}]Correction : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for relation in teacher_module_relations:
        if x == 0:
            x += 1
            continue
        elif x < 4:
            x += 1
        else:
            x = 0
        nbOfEntriesToCreate += 1
    for relation in teacher_module_relations:
        if x == 0: 
            x += 1
            continue
        elif x < 4:
            x += 1
        else:
            x = 0
        gen_id = IDS[13] + str(nbOfEntries)
        gen_emplacement_correction = "/media/copies/" + gen_id
        gen_id_module = relation.module
        gen_id_enseignant = relation.enseignant
        obj = Correction(id_correction = gen_id, emplacement_correction = gen_emplacement_correction, id_module = gen_id_module, id_enseignant = gen_id_enseignant)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[20/{}]Correction : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateReclamation2():
    student_module_relations = Etudiant.modules.through.objects.all()
    nbOfEntries = 0
    x = 0
    nbOfEntriesToCreate = len(student_module_relations) // 10
    sys.stdout.write('\n[21/{}]Reclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for i in range(0,nbOfEntriesToCreate):
        gen_id = IDS[18] + str(nbOfEntries)
        gen_sujet_reclamation = fake.text(30)
        gen_description_reclamation = fake.text(300)
        gen_id_etudiant = random.choice(student_module_relations).etudiant
        gen_id_module = random.choice(student_module_relations).module
        obj = Reclamation(id_reclamation = gen_id, sujet_reclamation = gen_sujet_reclamation, description_reclamation = gen_description_reclamation, id_etudiant = gen_id_etudiant, id_module = gen_id_module)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[21/{}]Reclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateReclamation():
    allStudents = Etudiant.objects.all()
    nbOfEntriesToCreate = 0
    for student in allStudents:
        allModules = Module.objects.filter(id_specialite = Specialite.objects.filter(id_specialite = (Section.objects.filter(id_section = Groupe.objects.filter(id_groupe = student.id_groupe.id_groupe)[0].id_section.id_section)[0].id_specialite.id_specialite))[0])
        for module in allModules:
            nbOfEntriesToCreate += 1
    nbOfEntries = 0
    nbOfEntriesToCreate = nbOfEntriesToCreate // 10
    sys.stdout.write('\n[21/{}]Reclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for i in range(0,nbOfEntriesToCreate):
        gen_id = IDS[18] + str(nbOfEntries)
        gen_sujet_reclamation = fake.text(30)
        gen_description_reclamation = fake.text(300)
        gen_id_etudiant = random.choice(allStudents)
        gen_id_module = random.choice(Module.objects.filter(id_specialite = Specialite.objects.filter(id_specialite = (Section.objects.filter(id_section = Groupe.objects.filter(id_groupe = gen_id_etudiant.id_groupe.id_groupe)[0].id_section.id_section)[0].id_specialite.id_specialite))[0]))
        obj = Reclamation(id_reclamation = gen_id, sujet_reclamation = gen_sujet_reclamation, description_reclamation = gen_description_reclamation, id_etudiant = gen_id_etudiant, id_module = gen_id_module)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[21/{}]Reclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateConsultation():
    teacher_module_relations = Enseignant.modules.through.objects.all()
    nbOfEntries = 0
    x = 0
    nbOfEntriesToCreate = 0
    sys.stdout.write('\n[22/{}]Consultation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for relation in teacher_module_relations:
        if x == 0 or x <3: ### 25% entries creation
            x += 1
            continue
        else:
            x = 0
        nbOfEntriesToCreate += 1
    for relation in teacher_module_relations:
        if x == 0 or x <3: ### 25% entries creation
            x += 1
            continue
        else:
            x = 0
        gen_id = IDS[20] + str(nbOfEntries)
        gen_sale = random.choice([ "Sale" + str(random.randint(1,23)) , "Amphi" + str(random.randint(1,4)) ])
        gen_date = dt.strptime(fake.date(),'%Y-%M-%d').date()
        gen_time = dt.strptime(fake.time(),'%H:%M:%S').time()
        gen_id_enseignant = relation.enseignant
        gen_id_module = relation.module
        obj = Consultation(id_consultation = gen_id, sale_consultation = gen_sale, date_consultation = gen_date, heure_consultation = gen_time, afficher_consultation = False, id_enseignant = gen_id_enseignant, id_module = gen_id_module)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[22/{}]Consultation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateDiscussionAdministrative():
    allConsultations = Consultation.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allConsultations)
    sys.stdout.write('\n[23/{}]DiscussionAdministrative : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for consult in allConsultations:
        gen_id = IDS[17] + str(nbOfEntries)
        gen_id_enseignant = consult.id_enseignant
        gen_id_chef_departement = consult.id_module.id_specialite.id_parcours.id_filiere.id_chef_departement
        obj = DiscussionAdministrative(id_discussion = gen_id, id_chef_departement = gen_id_chef_departement, id_enseignant = gen_id_enseignant)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[23/{}]DiscussionAdministrative : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateDiscussionReclamation():
    allReclamations = Reclamation.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allReclamations)
    sys.stdout.write('\n[24/{}]DiscussionReclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for reclam in allReclamations:
        gen_id = IDS[19] + str(nbOfEntries)
        gen_id_reclamation = reclam
        gen_id_enseignant = Enseignant.modules.through.objects.filter(module__in = [reclam.id_module])[0].enseignant
        obj = DiscussionReclamation(id_discussion = gen_id, id_reclamation = gen_id_reclamation, id_enseignant = gen_id_enseignant)
        obj.save()
        nbOfEntries += 1
        sys.stdout.write('\r[24/{}]DiscussionReclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateMessagesAdministrative(nbMess = 10):
    allDiscussions = DiscussionAdministrative.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allDiscussions) * nbMess
    sys.stdout.write('\n[25/{}]MessagesAdministrative : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for discu in allDiscussions:    
        members_discu = [discu.id_chef_departement.id_chef_departement.id_utilisateur,\
         discu.id_enseignant.id_enseignant.id_utilisateur]
        for _ in range(0, nbMess):
            gen_id = IDS[21] + str(nbOfEntries)
            gen_content = fake.text(random.randint(30,250))
            gen_date = dt.strptime(fake.date(),'%Y-%M-%d').date()
            gen_time = dt.strptime(fake.time(),'%H:%M:%S').time()
            gen_emeteur = random.choice(members_discu)
            if gen_emeteur == members_discu[0]:
                gen_recepteur = members_discu[1]
            elif gen_emeteur == members_discu[1]:
                gen_recepteur = members_discu[0]
            obj = MessagesAdministrative(id_message = gen_id, contenu_message = gen_content, date_message = gen_date,\
             heure_message = gen_time, id_emetteur = gen_emeteur, id_recepteur = gen_recepteur, id_discussion = discu)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[25/{}]MessagesAdministrative : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))

def PopulateMessagesReclamation(nbMess = 10):
    allDiscussions = DiscussionReclamation.objects.all()
    nbOfEntries = 0
    nbOfEntriesToCreate = len(allDiscussions) * nbMess
    sys.stdout.write('\n[26/{}]MessagesReclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
    for discu in allDiscussions:    
        members_discu = [discu.id_enseignant.id_enseignant.id_utilisateur,\
         discu.id_reclamation.id_etudiant.id_etudiant.id_utilisateur]
        for _ in range(0, nbMess):
            gen_id = IDS[22] + str(nbOfEntries)
            gen_content = fake.text(random.randint(30,250))
            gen_date = dt.strptime(fake.date(),'%Y-%M-%d').date()
            gen_time = dt.strptime(fake.time(),'%H:%M:%S').time()
            gen_emeteur = random.choice(members_discu)
            if gen_emeteur == members_discu[0]:
                gen_recepteur = members_discu[1]
            elif gen_emeteur == members_discu[1]:
                gen_recepteur = members_discu[0]
            obj = MessagesReclamation(id_message = gen_id, contenu_message = gen_content, date_message = gen_date,\
             heure_message = gen_time, id_emetteur = gen_emeteur, id_recepteur = gen_recepteur, id_discussion = discu)
            obj.save()
            nbOfEntries += 1
            sys.stdout.write('\r[26/{}]MessagesReclamation : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))


def Populate():
    PopulateUtilisateur()
    PopulateNotification()
    PopulateChefDepartement()
    PopulateUniversite()
    PopulateFaculte()
    PopulateDomaine([0,1]) #indexs of faculties to populate in FACULTIES 
    PopulateFiliere()
    PopulateParcours()
    PopulateSpecialite()
    PopulateSection()
    PopulateGroupe()
    PopulateTechnicien()
    PopulateEnseignant()
    PopulateEtudiant()
    PopulateModule()
    PopulateAnnonce()
    RelationEnseignantFiliere()
    RelationEnseignantModule()
    ####RelationChefDepartementModule()
    ####RelationEtudiantModule()
    PopulateCopie()
    PopulateCorrection()
    PopulateReclamation()
    PopulateConsultation()
    PopulateDiscussionAdministrative()
    PopulateDiscussionReclamation()
    PopulateMessagesAdministrative()
    PopulateMessagesReclamation()


if __name__ == '__main__':
    print('populating...')
    Populate()
    print('\ndone !')


# allStudents = Etudiant.objects.filter(id_groupe = Groupe.objects.filter(id_section = Section.objects.filter(id_specialite = Specialite.objects.filter(nom = 'Systeme Information')[0])[0])[0])
# for module in allModules:
#     x += ((module.id_specialite).id_parcours).id_filiere




# def PopulateEnseignant(nbEnsen = 10):
#     allTeachers = Utilisateur.objects.filter(id_utilisateur__contains = IDS[1])
#     allBranches = list(Filiere.objects.filter(id_domaine__nom = 'Math Info'))
#     used = []
#     for branch in allBranches:
#         used += [0]
#     nbOfEntriesToCreate = nbEnsen
#     nbOfEntries = 0
#     sys.stdout.write('\n[/{}]Enseignant : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))
#     for teacher in allTeachers:
#         while True:
#             chosenBranch = random.choice(allBranches)
#             if used[allBranches.index(chosenBranch)] < 4:
#                 break
#         used[allBranches.index(chosenBranch)] += 1
#         obj = Enseignant(id_enseignant = teacher, id_filiere = chosenBranch)
#         obj.save()
#         nbOfEntries += 1
#         sys.stdout.write('\r[/{}]Enseignant : {}/{}'.format(NBTABLES,nbOfEntries,nbOfEntriesToCreate))