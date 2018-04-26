from django import forms
from gce_app.models import Utilisateur, FichierCopie, FichierCorrection

class avatar_upload_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar_utilisateur'].widget.attrs.update({'onchange': 'avatar_uploader(event)', 'accept': 'image/x-png,image/jpeg', 'id': 'avatar_upload'})
    
    class Meta():
        model = Utilisateur
        fields = ['avatar_utilisateur']


class copies_file_upload_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emplacement_fichier'].widget.attrs.update({'onchange': 'upload_copies(this,event);', 'id': 'upload_input', 'multiple': 'true', 'accept': 'image/jpeg'})
    
    class Meta():
        model = FichierCopie
        fields = ['emplacement_fichier']

class correction_file_upload_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emplacement_fichier'].widget.attrs.update({'onchange': 'upload_correction(this,event);', 'id': 'upload_input', 'multiple': 'true', 'accept': 'image/jpeg'})
    
    class Meta():
        model = FichierCorrection
        fields = ['emplacement_fichier']