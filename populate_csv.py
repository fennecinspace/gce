import xlrd, sys, django, os, re
from django.db.models import Q


## Setting up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gce.settings")
django.setup()

## import models
from gce_app.models import *
print ('models imported')


FILIERES = {
    'MI': ['MI'],
    'INFO': ['INFO','SIG', 'ISI','RESYS',],
    'MATH': ['MATH','MCO','AF'],
    'SM': ['SM'],
    'CHIMIE': ['CHIMIE','Ch-App'],
    'PHYSIQUE': ['PHYSIQUE','Ph-M'],
}

data = {
    'Université Abdelhamid ibn Badis Mostaganem' : {
        'FSEI': {
            'Mathematique et Informatique' : {
                'chef1mi': {
                    'Math Info Tronc Commun': {
                        'L1': ['MI'],
                    },
                },
                'chef2mi': {
                    'Informatique': {
                        'L2': ['INFO'],
                        'L3': ['INFO'],
                        'M1': ['ISI','RESYS'],
                        'M2': ['SIG'],

                    },
                },
                'chef3mi': {
                    'Mathematique': {
                        'L2': ['MATH'],
                        'L3': ['MATH'],
                        'M1': ['MCO','AF'],
                        'M2': ['MCO','AF'],

                    },
                },    
            },
            'Science de Matiere': {
                'chef1sm': {
                    'Science de Matiere Tronc Commun': {
                        'L1': ['SM'],
                    },
                },
                'chef2sm': {
                    'Chimie': {
                        'L2': ['CHIMIE'],
                        'L3': ['CHIMIE'],
                        'M1': ['Ch-App'],
                        'M2': ['Ch-App'],
                    },
                },
                'chef3sm': {
                    'Physique': {
                        'L2': ['PHYSIQUE'],
                        'L3': ['PHYSIQUE'],
                        'M1': ['Ph-M'],
                        'M2': ['Ph-M'],
                    },
                },
            },
        },
    },
}


def open_xlsl(path):
    '''
        opens an xlsl file and returns its sheets
    '''
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheets()
    return sheets


def read_sheet(sheet):
    col_names, data = [], []
    sheet_name = sheet.name
    
    # getting col names
    for col in range(sheet.ncols):
        col_names += [sheet.cell_value(0,col)]
    
    # getting data
    for row in range(1, sheet.nrows):
        entry = {}
        for col in range(sheet.ncols):
            entry[col_names[col]]= sheet.cell_value(row,col)
        data += [entry]
    
    return sheet_name, col_names, data


def get_affiliation(name):
    '''
        takes string of from "level specilaty .... " 
        returns level and specilaty
    '''
    l = name.strip().split(" ")
    level = l[0].strip()
    speciality = (" ".join(l[1:])).strip()
    return level, speciality



if __name__ == '__main__':
    # if sys.argv.__len__() < 2:
    #     print('NOT ENOUGH ARGUMENTS')
    #     exit()
    
    sheets = open_xlsl(sys.argv[1])

    for univ, data1 in data.items():
        univ_obj = Universite(nom = univ)
        univ_obj.save()

        for faculte, data2 in data1.items():
            faculte_obj = Faculte(nom = faculte, id_universite = univ_obj )
            faculte_obj.save()
            
            for domaine, data3 in data2.items():
                domaine_obj = Domaine(nom = domaine, id_faculte = faculte_obj)
                domaine_obj.save()
                
                for chef, data4 in data3.items():
                    user_obj = User(username = chef,last_name = 'test', first_name = 'test', email = 'test@gce.dz')
                    user_obj.set_password('chef')
                    user_obj.save()

                    util_obj = Utilisateur(info_utilisateur = user_obj, type_utilisateur = 'chef')
                    util_obj.save()

                    chef_obj = ChefDepartement(id_chef_departement = util_obj)
                    chef_obj.save()
                
                    for filiere, data5 in data4.items():
                        filiere_obj = Filiere(nom = filiere, id_domaine = domaine_obj, id_chef_departement = chef_obj)
                        filiere_obj.save()

                        for parcour, data6 in data5.items():
                            parcour_obj = Parcours(nom = parcour, id_filiere = filiere_obj)
                            parcour_obj.save()
                            
                            for specialite in data6:
                                spec_obj = Specialite(nom = specialite, id_parcours = parcour_obj)
                                spec_obj.save()
                                
                                sec_obj = Section(numero = 1, id_specialite = spec_obj)
                                sec_obj.save()

                                grp_obj = Groupe(numero = 1, id_section = sec_obj)
                                grp_obj.save()

                                pass


                                for sheet in sheets:
                                    sheet_name, col_names, data = read_sheet(sheet)
                                    level, speciality = get_affiliation(sheet_name)

                                    if speciality == specialite:
                                        print('Creating Users For {} {}'.format(level, speciality))
                                        # creating USER
                                        for entry in data:
                                            usr_full_name = ("-".join(entry['nom'].split(' ') + entry['prenom'].split(' '))).lower().strip()
                                            usr_full_name = re.sub(r'-$', '', usr_full_name)
                                            usr_full_name = re.sub(r'[-]{2,}', '-', usr_full_name)

                                            usr_username = ("{}-{}".format(usr_full_name, entry['matricule'])).lower().strip()

                                            usr_mail = ('{}@gce-mosta.dz'.format(usr_full_name)).lower().strip()

                                            if User.objects.filter(username = usr_username).__len__() == 0:
                                                etud_usr_obj = User(username = usr_username, last_name = entry['nom'].title(), first_name = entry['prenom'].title(), email = usr_mail)

                                                etud_usr_obj.set_password(entry['matricule'])
                                                etud_usr_obj.save()

                                                ## creating UTILISATEUR
                                                etud_util_obj = Utilisateur(info_utilisateur = etud_usr_obj, type_utilisateur = 'etud')
                                                etud_util_obj.save()

                                                ## creating Etudiant
                                                etud_etud_obj = Etudiant(id_etudiant = etud_util_obj, id_groupe = grp_obj)
                                                etud_etud_obj.save()
                                                print('    User {} created'.format(usr_username))
                                            else:
                                                print('    User {} already exists'.format(usr_username))