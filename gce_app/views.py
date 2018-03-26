from django.shortcuts import render
from gce_app.models import FichierCopie, FichierCorrection
from django.views.generic import TemplateView

#importing needed models
from gce_app.models import Utilisateur

#importing authentification modules
from django.contrib.auth import login, logout, authenticate 
from django.http import HttpResponse
from django.contrib import messages

def testpage(req):
    copie = FichierCopie.objects.all()[0].emplacement_fichier
    correction = FichierCorrection.objects.all()[0].emplacement_fichier
    myDict = {
        'testing' : 'TESTING STATIC/MEDIA/TEMPLATES',
        'copySample': copie,
        'correctionSample': correction,
    }
    
    return render(req, 'gce_app/testpage.html', context = myDict)


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

        loggedin_user = Utilisateur.objects.all().filter(info_utilisateur__in = [req.user])[0]
        if loggedin_user.type_utilisateur == 'etud':
            return render(req, 'gce_app/etud/etud_index.html', context = None)
        if loggedin_user.type_utilisateur == 'tech':
            return render(req, 'gce_app/tech/tech_index.html', context = None)
        if loggedin_user.type_utilisateur == 'ensg':
            return render(req, 'gce_app/ensg/ensg_index.html', context = None)
        if loggedin_user.type_utilisateur == 'chef':
            return render(req, 'gce_app/chef/chef_index.html', context = None)

    def get(self,req):
        if req.user.is_anonymous: # if user is not logged in return login page
            return render(req, 'gce_app/common/login.html', context = None)
        loggedin_user = Utilisateur.objects.all().filter(info_utilisateur__in = [req.user])[0]
        if loggedin_user.type_utilisateur == 'etud':
            return render(req, 'gce_app/etud/etud_index.html', context = None)
        if loggedin_user.type_utilisateur == 'tech':
            return render(req, 'gce_app/tech/tech_index.html', context = None)
        if loggedin_user.type_utilisateur == 'ensg':
            return render(req, 'gce_app/ensg/ensg_index.html', context = None)
        if loggedin_user.type_utilisateur == 'chef':
            return render(req, 'gce_app/chef/chef_index.html', context = None)