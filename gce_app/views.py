from django.shortcuts import render
from gce_app.models import FichierCopie, FichierCorrection
from django.views.generic import TemplateView

#importing authentification modules
from django.contrib.auth import login, logout, authenticate 
from django.http import HttpResponse

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
                return render(req, 'gce_app/login.html', context = None) # return login page after logging out
        return render(req, 'gce_app/index.html', context = None) # return home page in case of login

    def get(self,req):
        if req.user.is_anonymous: # if user is not logged in return login page
            return render(req, 'gce_app/login.html', context = None)
        else: # if user is logged in return home page
            return render(req, 'gce_app/index.html', context = None)