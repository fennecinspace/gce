from django.shortcuts import render

# Create your views here.

def index(req):
    return render (req,'gce_app/index.html',context = {'testing' : 'TESTING STATIC/MEDIA/TEMPLATES'})