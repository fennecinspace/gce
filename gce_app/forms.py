from django import forms
from gce_app.models import Utilisateur

class avatar_upload_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar_utilisateur'].widget.attrs.update({'onchange': 'avatar_uploader(event)', 'accept': 'image/*', 'id': 'avatar_upload'})
    
    class Meta():
        model = Utilisateur
        fields = ['avatar_utilisateur']